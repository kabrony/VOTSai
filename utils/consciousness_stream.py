"""
Consciousness Stream for TRILOGY Brain

Maintains persistent memory and decision logs across sessions.
"""
import os
import time
import logging
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ConsciousnessStream:
    """Maintains logs of AI interactions and decisions"""
    
    def __init__(self, notes_dir: str = "data/notes"):
        self.notes_dir = notes_dir
        self.current_file = os.path.join(notes_dir, f"meeting_notes_{datetime.now().strftime('%Y-%m-%d')}.md")
        os.makedirs(notes_dir, exist_ok=True)
        
    def add_entry(self, entry_type: str, content: str, metadata: Dict[str, Any] = None) -> None:
        """
        Add an entry to the consciousness stream
        
        Args:
            entry_type: Type of entry (decision, observation, question, etc.)
            content: Main content of the entry
            metadata: Additional information
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = f"## {timestamp} - {entry_type}\n\n{content}\n\n"
        
        if metadata:
            entry += "**Metadata:**\n\n"
            for key, value in metadata.items():
                entry += f"- **{key}**: {value}\n"
        
        entry += "\n---\n\n"
        
        try:
            with open(self.current_file, 'a+') as f:
                f.write(entry)
            logger.debug(f"Added {entry_type} entry to consciousness stream")
        except Exception as e:
            logger.error(f"Error adding entry to consciousness stream: {e}")
    
    def get_recent_entries(self, limit: int = 5) -> str:
        """Get recent entries from the consciousness stream"""
        try:
            if not os.path.exists(self.current_file):
                return "No recent entries."
                
            with open(self.current_file, 'r') as f:
                content = f.read()
                
            # Split by entries and get the most recent ones
            entries = content.split("---\n\n")
            recent = entries[-limit:] if len(entries) > limit else entries
            
            return "\n---\n\n".join(recent)
        except Exception as e:
            logger.error(f"Error getting recent entries: {e}")
            return f"Error retrieving entries: {str(e)}"
    
    def summarize_notes(self) -> str:
        """Generate a summary of recent notes"""
        # This could use an AI model to summarize the notes
        recent = self.get_recent_entries(10)
        
        # Here you would call your AI to summarize
        # For now, return the recent entries
        return f"# Recent Activity Summary\n\n{recent}" 