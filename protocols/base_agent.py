"""
Base Agent Protocol Definition
Defines the core interfaces and protocols for agent communication
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AgentRole(Enum):
    CTO = "cto"
    CODING = "coding"
    TESTING = "testing"
    SECURITY = "security"
    DATA = "data"
    DOCUMENTATION = "documentation"
    DEVOPS = "devops"
    FINANCE = "finance"

@dataclass
class AgentMessage:
    sender: AgentRole
    receiver: AgentRole
    message_type: str
    content: Dict[str, Any]
    priority: int = 1
    trace_id: Optional[str] = None

class BaseAgent(ABC):
    """Base class for all SORT agents."""
    
    def __init__(self, role: AgentRole):
        self.role = role
        self.is_active = True
        self.health_status = "healthy"
    
    @abstractmethod
    async def process_message(self, message: AgentMessage) -> AgentMessage:
        """Process incoming message and return response."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check and return status."""
        pass
    
    @abstractmethod
    async def self_heal(self) -> bool:
        """Attempt self-healing if issues detected."""
        pass
    
    @abstractmethod
    async def initialize_model(self) -> bool:
        """Initialize the agent's AI model."""
        pass
    
    async def send_message(self, to_role: AgentRole, message_type: str, content: Dict[str, Any]) -> AgentMessage:
        """Send message to another agent."""
        message = AgentMessage(
            sender=self.role,
            receiver=to_role,
            message_type=message_type,
            content=content
        )
        # Message sending logic to be implemented by concrete classes
        return message
