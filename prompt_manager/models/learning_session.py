"""Learning session management module."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


@dataclass
class LearningSession:
    """Manages learning session configuration and state."""
    
    duration: int = 30  # Duration in minutes
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate session parameters."""
        if self.duration < 1:
            raise ValueError("Duration must be at least 1 minute")
    
    def start(self) -> None:
        """Start the learning session."""
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=self.duration)
    
    def is_active(self) -> bool:
        """Check if the session is currently active."""
        if not self.start_time or not self.end_time:
            return False
        return datetime.now() < self.end_time
    
    def time_remaining(self) -> Optional[timedelta]:
        """Get remaining time in the session."""
        if not self.start_time or not self.end_time:
            return None
        remaining = self.end_time - datetime.now()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary format."""
        return {
            'duration': self.duration,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_active': self.is_active(),
            'time_remaining': str(self.time_remaining()) if self.time_remaining() else None
        } 