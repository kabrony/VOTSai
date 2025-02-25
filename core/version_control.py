import os
import json
import time
import shutil
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VersionControl:
    """Simple version control system for TRILOGY Brain"""
    
    def __init__(self, version_dir="versions"):
        self.version_dir = version_dir
        self.current_version = self._load_current_version()
        self.versions = self._load_versions()
        
        # Create versions directory if it doesn't exist
        os.makedirs(self.version_dir, exist_ok=True)
        os.makedirs(os.path.join(self.version_dir, "backups"), exist_ok=True)
        
        logger.info(f"Version control initialized at {version_dir}, current version: {self.current_version}")
    
    def _load_current_version(self):
        """Load the current version number from file"""
        version_file = os.path.join(self.version_dir, "current_version.txt")
        if os.path.exists(version_file):
            with open(version_file, "r") as f:
                return f.read().strip()
        return "v0.1.0"  # Default initial version
    
    def _load_versions(self):
        """Load version history from file"""
        history_file = os.path.join(self.version_dir, "version_history.json")
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                return json.load(f)
        return []
    
    def _save_current_version(self):
        """Save the current version number to file"""
        version_file = os.path.join(self.version_dir, "current_version.txt")
        with open(version_file, "w") as f:
            f.write(self.current_version)
    
    def _save_versions(self):
        """Save version history to file"""
        history_file = os.path.join(self.version_dir, "version_history.json")
        with open(history_file, "w") as f:
            json.dump(self.versions, f, indent=2)
    
    def create_backup(self, files_to_backup):
        """Create a backup of the current system state"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.version_dir, "backups", f"{self.current_version}_{timestamp}")
        os.makedirs(backup_dir, exist_ok=True)
        
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                shutil.copy2(file_path, os.path.join(backup_dir, filename))
        
        return backup_dir
    
    def create_new_version(self, version_type="patch", description="", files_to_backup=None):
        """
        Create a new version
        
        Args:
            version_type: "major", "minor", or "patch"
            description: Description of the version changes
            files_to_backup: List of files to backup before updating
        
        Returns:
            New version string
        """
        if files_to_backup is None:
            files_to_backup = [
                "trilogy_app.py",
                "trilogy_integration.py",
                "core/trilogy_brain.py",
                "core/claude_api.py",
                "core/router.py"
            ]
        
        # Parse current version
        parts = self.current_version.lstrip("v").split(".")
        major, minor, patch = map(int, parts)
        
        # Update version number
        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        # Create backup
        backup_dir = self.create_backup(files_to_backup)
        
        # Create new version string
        new_version = f"v{major}.{minor}.{patch}"
        
        # Add to version history
        self.versions.append({
            "version": new_version,
            "previous_version": self.current_version,
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": description,
            "backup_dir": backup_dir
        })
        
        # Update current version
        self.current_version = new_version
        
        # Save to files
        self._save_current_version()
        self._save_versions()
        
        logger.info(f"Created new version: {new_version} - {description}")
        return new_version
    
    def rollback(self, target_version=None):
        """
        Roll back to a previous version
        
        Args:
            target_version: Version to roll back to. If None, roll back one version.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.versions:
            logger.error("No versions to roll back to")
            return False
        
        # If no target version specified, roll back one version
        if target_version is None:
            if len(self.versions) < 2:
                logger.error("Not enough versions to roll back")
                return False
            target_version = self.versions[-2]["version"]
        
        # Find the target version
        target_version_info = None
        for version in self.versions:
            if version["version"] == target_version:
                target_version_info = version
                break
        
        if target_version_info is None:
            logger.error(f"Target version {target_version} not found")
            return False
        
        # Get files from backup directory
        backup_dir = target_version_info["backup_dir"]
        if not os.path.exists(backup_dir):
            logger.error(f"Backup directory {backup_dir} not found")
            return False
        
        # Restore files from backup
        for file_name in os.listdir(backup_dir):
            source_path = os.path.join(backup_dir, file_name)
            destination_path = os.path.join(".", file_name)
            shutil.copy2(source_path, destination_path)
        
        # Update current version
        self.current_version = target_version
        self._save_current_version()
        
        logger.info(f"Rolled back to version: {target_version}")
        return True
    
    def get_version_history(self):
        """Get the version history"""
        return self.versions
    
    def get_current_version(self):
        """Get the current version"""
        return self.current_version 