"""
Text Utilities for Interview Coach
"""

import re
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max_length characters"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def sanitize_text(text: str) -> str:
    """Sanitize text by removing potentially harmful content"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    return text


def extract_keywords(text: str, min_length: int = 3, max_length: int = 20) -> List[str]:
    """Extract keywords from text"""
    if not text:
        return []
    
    # Remove punctuation and split into words
    words = re.findall(r'\b[a-zA-Z]{' + str(min_length) + r',' + str(max_length) + r'}\b', text)
    
    # Common stop words to exclude
    stop_words = {
        'the', 'and', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'that', 'this', 'it', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall',
        'should', 'can', 'could', 'may', 'might', 'must', 'i', 'you', 'he', 'she',
        'we', 'they', 'my', 'your', 'his', 'her', 'our', 'their', 'me', 'him',
        'us', 'them', 'as', 'by', 'from', 'or', 'but', 'not', 'so', 'if', 'then',
        'else', 'when', 'where', 'how', 'what', 'which', 'who', 'whom', 'there',
        'here', 'other', 'some', 'such', 'no', 'nor', 'only', 'own', 'same', 'than',
        'too', 'very', 'just', 'now', 'also', 'any', 'both', 'each', 'few', 'more',
        'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same'
    }
    
    # Filter out stop words and convert to lowercase
    keywords = [word.lower() for word in words if word.lower() not in stop_words]
    
    return keywords


def count_words(text: str) -> int:
    """Count words in text"""
    if not text:
        return 0
    
    return len(text.split())


def count_sentences(text: str) -> int:
    """Count sentences in text"""
    if not text:
        return 0
    
    # Split on sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])


def calculate_readability(text: str) -> dict:
    """Calculate text readability metrics"""
    if not text:
        return {
            'word_count': 0,
            'sentence_count': 0,
            'avg_sentence_length': 0,
            'character_count': 0
        }
    
    word_count = count_words(text)
    sentence_count = count_sentences(text)
    character_count = len(text)
    
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    return {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'avg_sentence_length': round(avg_sentence_length, 2),
        'character_count': character_count
    }


def extract_entities(text: str, entity_type: str = None) -> List[str]:
    """Extract entities from text (simplified version)"""
    if not text:
        return []
    
    # Simple pattern matching for different entity types
    patterns = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'url': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'number': r'\b\d+\b',
        'word': r'\b\w+\b'
    }
    
    if entity_type and entity_type in patterns:
        return re.findall(patterns[entity_type], text)
    
    # Return all words if no specific type
    return re.findall(r'\b\w+\b', text)


def contains_keywords(text: str, keywords: List[str], case_sensitive: bool = False) -> bool:
    """Check if text contains any of the keywords"""
    if not text or not keywords:
        return False
    
    if not case_sensitive:
        text = text.lower()
        keywords = [k.lower() for k in keywords]
    
    for keyword in keywords:
        if keyword in text:
            return True
    
    return False


def text_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity (0-1)"""
    from difflib import SequenceMatcher
    
    if not text1 or not text2:
        return 0.0
    
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def format_text_for_llm(text: str, max_length: int = 4000) -> str:
    """Format text for LLM input"""
    if not text:
        return ""
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    # Remove excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()
