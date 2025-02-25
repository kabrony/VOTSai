"""
Reasoning systems for TRILOGY Brain

This package contains implementations of reasoning systems that
enhance AI models with structured reasoning capabilities.
"""
from core.reasoning.cot_processor import CoTProcessor
from core.reasoning.enhanced_cot import EnhancedCoTProcessor

__all__ = ['CoTProcessor', 'EnhancedCoTProcessor'] 