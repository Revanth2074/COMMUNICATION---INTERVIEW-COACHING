"""
OmniRoute LLM Client
Wraps the OpenAI SDK to communicate with OmniRoute's OpenAI-compatible API.
Uses only FREE models to avoid any billing costs.
"""
import asyncio
import json
import re
from typing import Optional, Any
from openai import AsyncOpenAI
from config import settings

# Free model preference order - all zero-cost models
FREE_MODEL_PREFERENCE = [
    "free-stack",                           # OmniRoute combo: auto-picks best free
    "auto/best-free",                       # OmniRoute auto best-free
    "openrouter/openrouter/free",           # OpenRouter generic free
    "openrouter/google/gemma-4-31b-it:free",
    "openrouter/minimax/minimax-m3:free",
    "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
    "oc/deepseek-v4-flash-free",
    "oc/qwen3.6-plus-free",
    "oc/minimax-m3-free",
]


def extract_json(text: str) -> dict:
    """Extract and parse JSON from LLM text, handling markdown code fences and extraneous text."""
    if not text:
        return {}
    text = text.strip()
    
    # Try finding markdown code block: ```json ... ``` or ``` ... ```
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence_match:
        extracted = fence_match.group(1).strip()
        try:
            return json.loads(extracted)
        except Exception:
            pass

    # Try raw JSON decode
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try finding outer { ... } or [ ... ]
    brace_match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    if brace_match:
        try:
            return json.loads(brace_match.group(1))
        except Exception:
            pass

    raise ValueError(f"Could not parse valid JSON from text: {text[:200]}...")


class OmniRouteClient:
    """Async client for OmniRoute API using OpenAI SDK compatibility.
    
    Strictly uses free models only - no paid API calls.
    """

    def __init__(self):
        api_key = settings.OMNIROUTE_API_KEY or "sk-omniroute"
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=settings.OMNIROUTE_BASE_URL,
        )
        self._available_models: list[str] = []
        self._free_models: list[str] = []
        self._default_model: str = ""

    async def discover_models(self) -> list[str]:
        """Auto-discover available models from OmniRoute, selecting only FREE models."""
        try:
            models_response = await self.client.models.list()
            self._available_models = [m.id for m in models_response.data]
            
            # Filter to only free models
            self._free_models = [
                m for m in self._available_models
                if "free" in m.lower()
                or m == "free-stack"
                or m == "auto/best-free"
            ]
            print(f"[OmniRoute] Discovered {len(self._available_models)} total models, "
                  f"{len(self._free_models)} free models")

            # Set default model from PREFERRED_MODEL if it's free, else pick best free
            preferred = settings.PREFERRED_MODEL
            if preferred and ("free" in preferred.lower() or preferred in ("free-stack", "auto/best-free")):
                if preferred in self._available_models:
                    self._default_model = preferred
                    print(f"[OmniRoute] Using preferred FREE model: {self._default_model}")
                    return self._available_models

            # Auto-pick best free model from preference order
            for pref in FREE_MODEL_PREFERENCE:
                if pref in self._available_models:
                    self._default_model = pref
                    break

            # Last resort: any free model
            if not self._default_model and self._free_models:
                self._default_model = self._free_models[0]

            # Absolute fallback (should not normally reach here)
            if not self._default_model:
                self._default_model = "free-stack"

            print(f"[OmniRoute] Default FREE model: {self._default_model}")
            return self._available_models
        except Exception as e:
            print(f"[OmniRoute] Error discovering models: {e}")
            self._default_model = "free-stack"
            self._available_models = [self._default_model]
            self._free_models = [self._default_model]
            return self._available_models

    @property
    def default_model(self) -> str:
        return self._default_model or "free-stack"

    @property
    def available_models(self) -> list[str]:
        return self._available_models

    @property
    def free_models(self) -> list[str]:
        return self._free_models

    async def chat(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[dict] = None,
    ) -> str:
        """Send a chat completion request through OmniRoute using only free models."""
        # Always enforce free model - override any non-free model passed in
        selected_model = model or self._default_model or "free-stack"
        if selected_model and "free" not in selected_model.lower() and selected_model not in ("free-stack", "auto/best-free"):
            # Redirect to free-stack to avoid billing
            print(f"[OmniRoute] Redirecting non-free model '{selected_model}' -> 'free-stack'")
            selected_model = "free-stack"

        kwargs = {
            "model": selected_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = await self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"[OmniRoute] Chat error with model {selected_model}: {e}")
            # Try other free models as fallback
            for fallback in FREE_MODEL_PREFERENCE:
                if fallback != selected_model and fallback in self._available_models:
                    try:
                        print(f"[OmniRoute] Trying free fallback model: {fallback}")
                        kwargs["model"] = fallback
                        # Remove response_format for fallback models that may not support it
                        fallback_kwargs = {k: v for k, v in kwargs.items() if k != "response_format"}
                        response = await self.client.chat.completions.create(**fallback_kwargs)
                        return response.choices[0].message.content or ""
                    except Exception as fe:
                        print(f"[OmniRoute] Fallback {fallback} also failed: {fe}")
                        continue
            raise

    async def chat_json(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.4,
        max_tokens: int = 4096,
    ) -> str:
        """Send a chat completion expecting JSON response using free models."""
        # First attempt with json_object format
        try:
            content = await self.chat(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            return content
        except Exception:
            # Some free models don't support json_object format - retry without it
            content = await self.chat(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return content


# Global singleton
llm_client = OmniRouteClient()
