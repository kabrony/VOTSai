"""
Tests for TRILOGY Brain core components
"""
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.trilogy_brain import TrilogyBrain
from core.cot_processor import CoTProcessor

class TestTrilogyBrain(unittest.TestCase):
    """Tests for the TrilogyBrain class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.model_registry = MagicMock()
        self.router = MagicMock()
        self.memory_system = MagicMock()
        self.telemetry = MagicMock()
        self.cot_processor = MagicMock()
        
        self.brain = TrilogyBrain(
            model_registry=self.model_registry,
            router=self.router,
            memory_system=self.memory_system,
            telemetry=self.telemetry,
            cot_processor=self.cot_processor
        )
    
    def test_initialization(self):
        """Test TrilogyBrain initialization"""
        self.assertEqual(self.brain.model_registry, self.model_registry)
        self.assertEqual(self.brain.router, self.router)
        self.assertEqual(self.brain.memory_system, self.memory_system)
        self.assertEqual(self.brain.telemetry, self.telemetry)
        self.assertEqual(self.brain.cot_processor, self.cot_processor)
    
    @patch('core.trilogy_brain.time')
    def test_process_query(self, mock_time):
        """Test processing a query"""
        # Setup mocks
        mock_time.time.side_effect = [0, 1]  # Start and end times
        self.telemetry.track_query.return_value = "query-id-123"
        self.router.analyze.return_value = {"domain": "general"}
        self.memory_system.get_relevant_memories.return_value = []
        self.router.route.return_value = "test_model"
        
        model_mock = MagicMock()
        model_mock.chat.return_value = {
            "text": "Test response",
            "model": "test_model",
            "metadata": {}
        }
        self.model_registry.get_model.return_value = model_mock
        
        # Call the method
        result = self.brain.process_query("Test query")
        
        # Assertions
        self.telemetry.track_query.assert_called_once_with("Test query")
        self.router.analyze.assert_called_once()
        self.memory_system.get_relevant_memories.assert_called_once_with("Test query")
        self.router.route.assert_called_once()
        self.model_registry.get_model.assert_called_once_with("test_model")
        model_mock.chat.assert_called_once()
        self.assertEqual(result["answer"], "Test response")
        self.assertEqual(result["model"], "test_model")


class TestCoTProcessor(unittest.TestCase):
    """Tests for the CoTProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.cot = CoTProcessor()
    
    def test_initialization(self):
        """Test CoTProcessor initialization"""
        self.assertEqual(self.cot.cot_temperature, 0.7)
        self.assertEqual(self.cot.max_reasoning_steps, 10)
        self.assertTrue(self.cot.extract_reasoning)
        self.assertEqual(self.cot.reasoning_format, "markdown")
    
    def test_enhance_prompt(self):
        """Test enhancing a prompt with CoT"""
        # Simple prompt - should not be enhanced
        prompt, system_prompt = self.cot.enhance_prompt("What is 2+2?")
        self.assertEqual(prompt, "What is 2+2?")
        self.assertEqual(system_prompt, "")
        
        # Complex prompt - should be enhanced
        prompt, system_prompt = self.cot.enhance_prompt(
            "Explain the process of photosynthesis and its importance for life on Earth."
        )
        self.assertEqual(prompt, "Explain the process of photosynthesis and its importance for life on Earth.")
        self.assertTrue("chain of thought" in system_prompt.lower())
    
    def test_extract_reasoning_steps(self):
        """Test extracting reasoning steps"""
        # Test with numbered steps
        response = """
        Let me solve this step by step:
        
        1. First, I'll identify the key parts of photosynthesis
        2. Then, I'll explain each part in detail
        3. Finally, I'll discuss its importance
        
        In conclusion, photosynthesis is vital for life on Earth.
        """
        
        steps, final_answer = self.cot.extract_reasoning_steps(response)
        self.assertEqual(len(steps), 3)
        self.assertTrue("photosynthesis is vital" in final_answer)


if __name__ == '__main__':
    unittest.main() 