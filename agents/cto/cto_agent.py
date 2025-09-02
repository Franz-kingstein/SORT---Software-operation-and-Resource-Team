"""
CTO Agent - Central Orchestrator
Manages and coordinates all other specialized agents
"""

import asyncio
from typing import Dict, Any, List
import logging
from datetime import datetime

from ..protocols.base_agent import BaseAgent, AgentRole, AgentMessage
from ..core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class CTOAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentRole.CTO)
        self.model_name = settings.CTO_MODEL
        self.subordinate_agents: Dict[AgentRole, BaseAgent] = {}
        self.task_queue: List[AgentMessage] = []
        self.last_health_check: Dict[AgentRole, datetime] = {}
    
    async def initialize_model(self) -> bool:
        """Initialize Mistral 7B model for orchestration."""
        try:
            # Model initialization logic here
            logger.info(f"Initializing {self.model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize CTO agent model: {e}")
            return False
    
    async def process_message(self, message: AgentMessage) -> AgentMessage:
        """Process incoming messages and orchestrate responses."""
        logger.info(f"CTO processing message from {message.sender}: {message.message_type}")
        
        # Route message based on type and content
        if message.message_type == "task_request":
            return await self._handle_task_request(message)
        elif message.message_type == "status_update":
            return await self._handle_status_update(message)
        elif message.message_type == "error_report":
            return await self._handle_error(message)
        
        return AgentMessage(
            sender=self.role,
            receiver=message.sender,
            message_type="error",
            content={"error": "Unknown message type"}
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all subordinate agents."""
        health_status = {
            "status": "healthy",
            "agents": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        for role, agent in self.subordinate_agents.items():
            try:
                agent_health = await agent.health_check()
                health_status["agents"][role.value] = agent_health
                self.last_health_check[role] = datetime.utcnow()
            except Exception as e:
                health_status["agents"][role.value] = {"status": "error", "error": str(e)}
                health_status["status"] = "degraded"
        
        return health_status
    
    async def self_heal(self) -> bool:
        """Attempt to recover from issues."""
        try:
            # Check for unresponsive agents
            current_time = datetime.utcnow()
            for role, last_check in self.last_health_check.items():
                if (current_time - last_check).seconds > settings.HEALTH_CHECK_INTERVAL:
                    logger.warning(f"Agent {role} unresponsive, attempting recovery")
                    await self._recover_agent(role)
            return True
        except Exception as e:
            logger.error(f"Self-healing failed: {e}")
            return False
    
    async def _handle_task_request(self, message: AgentMessage) -> AgentMessage:
        """Handle new task requests and delegate to appropriate agents."""
        task = message.content.get("task", {})
        task_type = task.get("type")
        
        if not task_type:
            return AgentMessage(
                sender=self.role,
                receiver=message.sender,
                message_type="error",
                content={"error": "Missing task type"}
            )
        
        # Delegate to appropriate agent based on task type
        target_role = self._determine_target_agent(task_type)
        if target_role in self.subordinate_agents:
            return await self.send_message(
                target_role,
                "task_assignment",
                {"task": task}
            )
        
        return AgentMessage(
            sender=self.role,
            receiver=message.sender,
            message_type="error",
            content={"error": f"No agent available for task type: {task_type}"}
        )
    
    async def _handle_status_update(self, message: AgentMessage) -> AgentMessage:
        """Process status updates from subordinate agents."""
        status = message.content.get("status", {})
        logger.info(f"Status update from {message.sender}: {status}")
        return AgentMessage(
            sender=self.role,
            receiver=message.sender,
            message_type="ack",
            content={"received": True}
        )
    
    async def _handle_error(self, message: AgentMessage) -> AgentMessage:
        """Handle error reports from agents."""
        error = message.content.get("error", "Unknown error")
        logger.error(f"Error from {message.sender}: {error}")
        
        # Trigger self-healing if needed
        if settings.ENABLE_SELF_HEALING:
            await self._recover_agent(message.sender)
        
        return AgentMessage(
            sender=self.role,
            receiver=message.sender,
            message_type="error_response",
            content={"action": "self_heal_initiated"}
        )
    
    async def _recover_agent(self, role: AgentRole) -> None:
        """Attempt to recover a failing agent."""
        if role in self.subordinate_agents:
            logger.info(f"Attempting to recover agent: {role}")
            try:
                agent = self.subordinate_agents[role]
                await agent.self_heal()
            except Exception as e:
                logger.error(f"Failed to recover agent {role}: {e}")
    
    def _determine_target_agent(self, task_type: str) -> AgentRole:
        """Map task type to appropriate agent role."""
        task_map = {
            "code": AgentRole.CODING,
            "test": AgentRole.TESTING,
            "security": AgentRole.SECURITY,
            "data": AgentRole.DATA,
            "documentation": AgentRole.DOCUMENTATION,
            "deployment": AgentRole.DEVOPS,
            "finance": AgentRole.FINANCE
        }
        return task_map.get(task_type, AgentRole.CTO)
