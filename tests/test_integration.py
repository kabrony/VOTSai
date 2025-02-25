import unittest
import os
import sys
import asyncio
from unittest.mock import patch, MagicMock
import sqlite3
import tempfile

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.models import ModelFactory
from handlers.query import orchestrate_query
from core.memory import init_memory_db
from collections import deque

class TestQueryOrchestration(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db").name
        self.conn = init_memory_db(self.temp_db)
        
        # Mock model factory
        self.model_factory = ModelFactory()
        self.mock_model = MagicMock()
        self.mock_model.query = AsyncMock(return_value={
            "answer": "Test response",
            "latency": 0.5,
            "input_tokens": 10,
            "output_tokens": 20,
            "model_name": "Test Model"
        })
        
        # Set up short-term memory
        self.short_term_memory = deque(maxlen=10)
        
    def tearDown(self):
        """Clean up after tests."""
        self.conn.close()
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)
            
    async def test_orchestrate_query_basic(self):
        """Test basic query orchestration."""
        result = await orchestrate_query(
            query="Test query",
            timeout=5,
            short_term_memory=self.short_term_memory,
            conn=self.conn,
            model=self.mock_model,
            web_priority=False,
            temperature=0.5,
            share_format="Text"
        )
        
        # Check result structure
        self.assertIn("final_answer", result)
        self.assertIn("latency", result)
        self.assertIn("model_name", result)
        self.assertIn("actions", result)
        
        # Verify model was called
        self.mock_model.query.assert_called_once()
        
        # Check memory was updated
        self.assertEqual(len(self.short_term_memory), 1)
        
    @patch("handlers.query.search_web")
    async def test_orchestrate_query_with_web(self, mock_search):
        """Test query orchestration with web search."""
        mock_search.return_value = "Web search results"
        
        result = await orchestrate_query(
            query="crawl example.com",
            timeout=5,
            short_term_memory=self.short_term_memory,
            conn=self.conn,
            model=self.mock_model,
            web_priority=True,
            temperature=0.5,
            share_format="Text"
        )
        
        # Verify web search was called
        mock_search.assert_called_once()
        
        # Check result
        self.assertIn("final_answer", result)
        self.assertIn("web_results", result)
        
    async def test_orchestrate_query_with_timeout(self):
        """Test query orchestration with timeout."""
        # Make model query take too long
        self.mock_model.query = AsyncMock(side_effect=asyncio.sleep(2))
        
        with self.assertRaises(asyncio.TimeoutError):
            await orchestrate_query(
                query="Test query",
                timeout=1,  # Short timeout
                short_term_memory=self.short_term_memory,
                conn=self.conn,
                model=self.mock_model,
                web_priority=False,
                temperature=0.5,
                share_format="Text"
            )

# Helper for async mocks
class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs) 