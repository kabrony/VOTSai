import unittest
from unittest.mock import patch, MagicMock
import asyncio
from core.models import ModelFactory

class TestModelFactory(unittest.TestCase):
    
    def setUp(self):
        self.model_factory = ModelFactory()
        
    def test_create_model_valid_types(self):
        """Test creating models of valid types."""
        model_names = ["DeepSeek API", "Perplexity API", "Local DeepSeek"]
        
        for model_name in model_names:
            with patch.object(self.model_factory, '_create_model_instance') as mock_create:
                mock_create.return_value = MagicMock()
                model = self.model_factory.create_model(model_name)
                mock_create.assert_called_once_with(model_name)
                self.assertIsNotNone(model)
    
    def test_create_model_invalid_type(self):
        """Test creating a model of invalid type raises an error."""
        with self.assertRaises(ValueError):
            self.model_factory.create_model("NonExistentModel")
    
    @patch('core.models.ModelFactory._select_model_by_query')
    def test_select_model_auto_with_web_priority(self, mock_select):
        """Test model selection in Auto mode with web priority."""
        mock_select.return_value = "DeepSeek API"
        model_name = self.model_factory.select_model(
            "test query", 
            "Auto", 
            web_priority=True,
            intent_classifier=MagicMock()
        )
        self.assertEqual(model_name, "DeepSeek API")
        mock_select.assert_called_once()
        
    def test_select_model_specific(self):
        """Test model selection with specific model."""
        model_name = self.model_factory.select_model(
            "test query", 
            "Perplexity API", 
            web_priority=True,
            intent_classifier=MagicMock()
        )
        self.assertEqual(model_name, "Perplexity API") 