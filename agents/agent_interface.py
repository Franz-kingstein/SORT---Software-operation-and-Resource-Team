# Agentix DevOps Studio - Agent Communication Interface
# ====================================================

"""
This module defines the communication interface between the CTO Agent 
and individual worker agents (Backend, Frontend, Tester).

Team Member: [ASSIGN TO INTEGRATION DEVELOPER]
Status: TODO - Implementation needed
"""

from typing import Dict, List, Any, Optional, Protocol
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Status of task execution."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskExecution:
    """Task execution tracking."""
    task_id: str
    agent_name: str
    task_assignment: Dict[str, str]
    status: TaskStatus
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class AgentInterface(Protocol):
    """Interface that all agents must implement."""
    
    def execute_task(self, task_assignment: Dict[str, str]) -> Dict[str, Any]:
        """Execute assigned task."""
        ...
    
    def get_status(self) -> str:
        """Get current agent status."""
        ...
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        ...


class AgentOrchestrator:
    """
    Unified orchestrator that efficiently combines all agents into a single workflow.
    
    Features:
    - Single testing agent combining AI strategy + execution
    - Streamlined communication between all agents
    - Efficient task delegation and coordination
    - Real-time status tracking and progress monitoring
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentInterface] = {}
        self.task_queue: List[TaskExecution] = []
        self.completed_tasks: List[TaskExecution] = []
        self.workflow_status = {
            'active': False,
            'current_tasks': {},
            'progress': 0,
            'total_tasks': 0
        }
    
    def register_agent(self, agent_name: str, agent_instance: AgentInterface):
        """
        Register an agent with the orchestrator.
        
        Args:
            agent_name: Unique identifier for the agent
            agent_instance: Agent implementing AgentInterface
        """
        if not hasattr(agent_instance, 'execute_task'):
            raise ValueError(f"Agent {agent_name} must implement execute_task method")
        
        self.agents[agent_name] = agent_instance
        print(f"✅ Registered agent: {agent_name}")
        
        # Log agent capabilities
        if hasattr(agent_instance, 'get_capabilities'):
            capabilities = agent_instance.get_capabilities()
            print(f"   Capabilities: {', '.join(capabilities)}")
    
    def execute_workflow(self, task_assignments: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
        """
        Execute complete workflow with all agents efficiently.
        
        Args:
            task_assignments: Dict mapping agent names to their task assignments
            
        Returns:
            Dict containing workflow results and status
        """
        print(f"🚀 Starting workflow with {len(task_assignments)} tasks...")
        
        self.workflow_status['active'] = True
        self.workflow_status['total_tasks'] = len(task_assignments)
        self.workflow_status['progress'] = 0
        
        results = {}
        errors = {}
        
        # Execute tasks for each agent
        for agent_name, task_assignment in task_assignments.items():
            if agent_name not in self.agents:
                error_msg = f"Agent '{agent_name}' not registered"
                errors[agent_name] = error_msg
                print(f"❌ {error_msg}")
                continue
            
            print(f"\n🎯 Executing task for {agent_name}...")
            
            # Create task execution record
            task_execution = TaskExecution(
                task_id=f"{agent_name}_{len(self.task_queue) + 1}",
                agent_name=agent_name,
                task_assignment=task_assignment,
                status=TaskStatus.IN_PROGRESS
            )
            
            self.task_queue.append(task_execution)
            self.workflow_status['current_tasks'][agent_name] = 'executing'
            
            try:
                # Execute the task
                agent = self.agents[agent_name]
                result = agent.execute_task(task_assignment)
                
                # Update task execution record
                task_execution.status = TaskStatus.COMPLETED
                task_execution.result = result
                results[agent_name] = result
                
                print(f"✅ {agent_name} completed successfully")
                
            except Exception as e:
                # Handle task failure
                error_msg = f"Task failed: {str(e)}"
                task_execution.status = TaskStatus.FAILED
                task_execution.error_message = error_msg
                errors[agent_name] = error_msg
                
                print(f"❌ {agent_name} failed: {error_msg}")
            
            finally:
                # Move to completed tasks and update progress
                self.completed_tasks.append(task_execution)
                if agent_name in self.workflow_status['current_tasks']:
                    del self.workflow_status['current_tasks'][agent_name]
                
                self.workflow_status['progress'] += 1
        
        # Finalize workflow
        self.workflow_status['active'] = False
        success_count = len(results)
        total_count = len(task_assignments)
        
        workflow_result = {
            'success': len(errors) == 0,
            'results': results,
            'errors': errors,
            'summary': {
                'total_tasks': total_count,
                'successful': success_count,
                'failed': len(errors),
                'success_rate': f"{(success_count/total_count)*100:.1f}%" if total_count > 0 else "0%"
            }
        }
        
        print(f"\n🏁 Workflow completed: {success_count}/{total_count} tasks successful")
        return workflow_result
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """
        Get detailed status of current workflow execution.
        
        Returns:
            Dict containing current workflow status and progress
        """
        return {
            'workflow_active': self.workflow_status['active'],
            'progress': f"{self.workflow_status['progress']}/{self.workflow_status['total_tasks']}",
            'progress_percentage': (self.workflow_status['progress'] / max(1, self.workflow_status['total_tasks'])) * 100,
            'current_tasks': self.workflow_status['current_tasks'],
            'registered_agents': list(self.agents.keys()),
            'queue_size': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks)
        }
    
    def get_agent_status(self, agent_name: str) -> Optional[str]:
        """Get status of a specific agent."""
        if agent_name not in self.agents:
            return None
        
        agent = self.agents[agent_name]
        if hasattr(agent, 'get_status'):
            return agent.get_status()
        return "available"
    
    def execute_single_task(self, agent_name: str, task_assignment: Dict[str, str]) -> Dict[str, Any]:
        """
        Execute a single task efficiently without full workflow overhead.
        
        Args:
            agent_name: Name of the agent to execute the task
            task_assignment: Task details for the agent
            
        Returns:
            Dict containing task result
        """
        if agent_name not in self.agents:
            return {
                'success': False,
                'error': f"Agent '{agent_name}' not registered"
            }
        
        try:
            agent = self.agents[agent_name]
            result = agent.execute_task(task_assignment)
            return {
                'success': True,
                'result': result,
                'agent': agent_name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent': agent_name
            }



# Unified Agent Communication Utilities
# =====================================

class AgentCommunicationHub:
    """
    Centralized communication hub for efficient agent coordination.
    """
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
        self.message_history: List[Dict[str, Any]] = []
        self.shared_context: Dict[str, Any] = {}
    
    def broadcast_message(self, sender: str, message: str, data: Optional[Dict] = None):
        """Send message to all agents."""
        message_record = {
            'timestamp': self._get_timestamp(),
            'sender': sender,
            'message': message,
            'data': data or {},
            'recipients': list(self.orchestrator.agents.keys())
        }
        self.message_history.append(message_record)
        print(f"📢 [{sender}] Broadcasting: {message}")
    
    def send_direct_message(self, sender: str, recipient: str, message: str, data: Optional[Dict] = None):
        """Send direct message between agents."""
        if recipient not in self.orchestrator.agents:
            print(f"❌ Recipient '{recipient}' not found")
            return False
        
        message_record = {
            'timestamp': self._get_timestamp(),
            'sender': sender,
            'recipient': recipient,
            'message': message,
            'data': data or {}
        }
        self.message_history.append(message_record)
        print(f"💬 [{sender} → {recipient}] {message}")
        return True
    
    def update_shared_context(self, key: str, value: Any, agent_name: str):
        """Update shared context accessible to all agents."""
        self.shared_context[key] = {
            'value': value,
            'updated_by': agent_name,
            'timestamp': self._get_timestamp()
        }
        print(f"🔄 Shared context updated: {key} by {agent_name}")
    
    def get_shared_context(self, key: Optional[str] = None) -> Any:
        """Get shared context data."""
        if key:
            return self.shared_context.get(key, {}).get('value')
        return self.shared_context
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Unified Agent Communication Utilities
# =====================================

class AgentCommunicationHub:
