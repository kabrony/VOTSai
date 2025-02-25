import unittest
import sqlite3
import os
from unittest.mock import patch
from core.memory import init_memory_db, update_memory, get_relevant_memory
from collections import deque

class TestMemory(unittest.TestCase):
    
    def setUp(self):
        """Set up test database."""
        self.test_db = "test_memory.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.conn = init_memory_db(self.test_db)
        
    def tearDown(self):
        """Clean up after tests."""
        self.conn.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
            
    def test_init_memory_db(self):
        """Test database initialization."""
        # Check if tables exist
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        self.assertIn("long_term_memory", tables)
        
    def test_update_memory(self):
        """Test adding memory to database and deque."""
        short_term = deque(maxlen=10)
        query = "Test query"
        result = {
            "answer": "Test answer",
            "model": "Test model",
            "latency": 1.0,
            "input_tokens": 10,
            "output_tokens": 20
        }
        
        update_memory(self.conn, query, result, short_term)
        
        # Check short term memory
        self.assertEqual(len(short_term), 1)
        self.assertEqual(short_term[0]["query"], query)
        self.assertEqual(short_term[0]["answer"], "Test answer")
        
        # Check long term memory
        cursor = self.conn.cursor()
        cursor.execute("SELECT query, answer, model FROM long_term_memory")
        row = cursor.fetchone()
        self.assertEqual(row[0], query)
        self.assertEqual(row[1], "Test answer")
        self.assertEqual(row[2], "Test model")
        
    def test_get_relevant_memory(self):
        """Test retrieving relevant memories."""
        # Add test memories
        queries = [
            "Python programming basics",
            "How to use asyncio in Python",
            "Best practices for Python decorators"
        ]
        
        for i, query in enumerate(queries):
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO long_term_memory (timestamp, query, answer) VALUES (?, ?, ?)",
                (f"2023-01-0{i+1}", query, f"Answer {i+1}")
            )
        self.conn.commit()
        
        # Test retrieval with relevant query
        result = get_relevant_memory(self.conn, "How to use Python asyncio for web scraping")
        self.assertIn("asyncio", result)
        
        # Test retrieval with unrelated query
        result = get_relevant_memory(self.conn, "JavaScript frontend frameworks")
        self.assertEqual(result, "No relevant memory found.") 