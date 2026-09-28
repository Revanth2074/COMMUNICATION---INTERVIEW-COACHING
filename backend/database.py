"""
Database Module for Interview Coach
Handles SQLite database operations and schema management
"""

import sqlite3
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, Any
import logging
from pathlib import Path
import os

logger = logging.getLogger(__name__)

# Database path
DB_PATH = "interview_coach.db"

# SQL schema for all tables
