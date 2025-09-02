#!/usr/bin/env python3
"""
Agentix DevOps Studio - CTO Agent Orchestrator
==============================================

This module implements the main LLM agent that acts as the orchestrator (CTO agent)
for the Agentix DevOps Studio prototype. It analyzes user requirements, decomposes
projects into tasks, and assigns them to appropriate specialized agents.

Author: GitHub Copilot
Date: September 1, 2025
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class AgentRole(Enum):
    """Enumeration of available agent roles in the DevOps pipeline."""
    CODER1 = "coder1"
    CODER2 = "coder2"
    TESTER = "tester"
    # SECURITY = "security"  # Commented out for prototype
    # DEVOPS = "devops"      # Commented out for prototype


class ActionType(Enum):
    """Enumeration of action types that agents can perform."""
    WRITE_CODE = "Write code"
    TEST_CODE = "Test code"
    # AUDIT_CODE = "Audit code"                # Commented out for prototype
    # DEPLOY_APPLICATION = "Deploy application" # Commented out for prototype
    # REVIEW_CODE = "Review code"               # Commented out for prototype


@dataclass
class TaskAssignment:
    """Data class representing a task assignment for an agent."""
    role: str
    action: str
    task: str

    def to_dict(self) -> Dict[str, str]:
        """Convert the task assignment to a dictionary format."""
        return {
            "role": self.role,
            "action": self.action,
            "task": self.task
        }


class ProjectAnalyzer:
    """Analyzes user prompts to extract project requirements and constraints."""

    def __init__(self):
        self.keywords = {
            'authentication': ['login', 'auth', 'signin', 'signup', 'password', 'user management'],
            'database': ['database', 'db', 'sql', 'nosql', 'storage', 'persist'],
            'api': ['api', 'rest', 'endpoint', 'service', 'backend'],
            'frontend': ['frontend', 'ui', 'interface', 'web', 'react', 'vue', 'angular'],
            'security': ['security', 'secure', 'encryption', 'vulnerability', 'ssl', 'https'],
            'deployment': ['deploy', 'production', 'staging', 'docker', 'kubernetes', 'cloud'],
            'testing': ['test', 'testing', 'unit test', 'integration', 'qa'],
            'monitoring': ['monitor', 'logging', 'metrics', 'analytics', 'performance']
        }

    def analyze_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """
        Analyze the user prompt to extract project goals, features, and constraints.
        
        Args:
            user_prompt (str): The user's project requirement description
            
        Returns:
            Dict[str, Any]: Analysis results containing goals, features, and constraints
        """
        try:
            prompt_lower = user_prompt.lower()
            
            # Extract project features based on keywords
            detected_features = []
            for feature, keywords in self.keywords.items():
                if any(keyword in prompt_lower for keyword in keywords):
                    detected_features.append(feature)
            
            # Extract urgency/timeline constraints
            urgency = "normal"
            if any(word in prompt_lower for word in ['urgent', 'asap', 'immediately', 'rush']):
                urgency = "high"
            elif any(word in prompt_lower for word in ['future', 'later', 'eventually']):
                urgency = "low"
            
            # Extract scale/complexity indicators
            complexity = "medium"
            if any(word in prompt_lower for word in ['simple', 'basic', 'small', 'minimal']):
                complexity = "low"
            elif any(word in prompt_lower for word in ['complex', 'enterprise', 'large-scale', 'advanced']):
                complexity = "high"
            
            return {
                "goals": self._extract_goals(user_prompt),
                "features": detected_features,
                "constraints": {
                    "urgency": urgency,
                    "complexity": complexity
                },
                "original_prompt": user_prompt
            }
            
        except Exception as e:
            raise ValueError(f"Error analyzing prompt: {str(e)}")

    def _extract_goals(self, prompt: str) -> List[str]:
        """Extract main project goals from the prompt."""
        # Simple goal extraction - in a real implementation, this could use NLP
        goals = []
        sentences = prompt.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and (
                sentence.lower().startswith(('create', 'build', 'develop', 'implement', 'design')) or
                'need' in sentence.lower() or 'want' in sentence.lower()
            ):
                goals.append(sentence)
        
        return goals if goals else ["Develop the requested application"]


class WorkflowOrchestrator:
    """Orchestrates the workflow and enforces business rules."""

    def __init__(self):
        self.workflow_rules = {
            "testing_before_deployment": True,
            # "security_approval_required": True,  # Commented out for prototype
            # "code_review_required": True         # Commented out for prototype
        }

    def validate_workflow(self, task_assignments: Dict[str, TaskAssignment]) -> bool:
        """
        Validate that the task assignments follow workflow rules.
        
        Args:
            task_assignments (Dict[str, TaskAssignment]): The task assignments to validate
            
        Returns:
            bool: True if workflow is valid, False otherwise
        """
        try:
            # Check if testing is included when deployment is present
            has_deployment = any(
                assignment.action == "Deploy application"  # Direct string since DEPLOY_APPLICATION is commented
                for assignment in task_assignments.values()
            )
            has_testing = any(
                assignment.action == ActionType.TEST_CODE.value 
                for assignment in task_assignments.values()
            )
            
            if has_deployment and not has_testing and self.workflow_rules["testing_before_deployment"]:
                return False
            
            # Security audit check commented out for prototype
            # has_security = any(
            #     assignment.action == ActionType.AUDIT_CODE.value 
            #     for assignment in task_assignments.values()
            # )
            # 
            # if not has_security and self.workflow_rules["security_approval_required"]:
            #     return False
            
            return True
            
        except Exception:
            return False

    def get_execution_order(self, task_assignments: Dict[str, TaskAssignment]) -> List[str]:
        """
        Determine the execution order of tasks based on dependencies.
        
        Args:
            task_assignments (Dict[str, TaskAssignment]): The task assignments
            
        Returns:
            List[str]: Ordered list of agent names for execution
        """
        # Define execution priority (lower number = higher priority)
        priority_map = {
            ActionType.WRITE_CODE.value: 1,
            # ActionType.REVIEW_CODE.value: 2,          # Commented out for prototype
            ActionType.TEST_CODE.value: 3,
            # ActionType.AUDIT_CODE.value: 4,           # Commented out for prototype
            # ActionType.DEPLOY_APPLICATION.value: 5    # Commented out for prototype
        }
        
        # Sort agents by their action priority
        sorted_agents = sorted(
            task_assignments.keys(),
            key=lambda agent: priority_map.get(task_assignments[agent].action, 999)
        )
        
        return sorted_agents


class CTOAgent:
    """
    Main CTO Agent class that orchestrates the entire DevOps pipeline.
    
    This agent analyzes user requirements, decomposes projects into tasks,
    assigns them to appropriate agents, and ensures workflow compliance.
    """

    def __init__(self):
        self.analyzer = ProjectAnalyzer()
        self.orchestrator = WorkflowOrchestrator()
        self.agent_capabilities = {
            AgentRole.CODER1.value: {
                "role": "Senior Backend Developer",
                "specialties": ["backend", "api", "database", "authentication"],
                "action": ActionType.WRITE_CODE.value
            },
            AgentRole.CODER2.value: {
                "role": "Frontend Developer",
                "specialties": ["frontend", "ui", "web", "client-side"],
                "action": ActionType.WRITE_CODE.value
            },
            AgentRole.TESTER.value: {
                "role": "Software Tester",
                "specialties": ["testing", "qa", "automation", "integration"],
                "action": ActionType.TEST_CODE.value
            },
            # AgentRole.SECURITY.value: {  # Commented out for prototype
            #     "role": "Security Auditor",
            #     "specialties": ["security", "vulnerabilities", "compliance", "audit"],
            #     "action": ActionType.AUDIT_CODE.value
            # },
            # AgentRole.DEVOPS.value: {    # Commented out for prototype
            #     "role": "DevOps Engineer",
            #     "specialties": ["deployment", "infrastructure", "monitoring", "scaling"],
            #     "action": ActionType.DEPLOY_APPLICATION.value
            # }
        }

    def process_user_request(self, user_prompt: str) -> Dict[str, Dict[str, str]]:
        """
        Main entry point for processing user requests.
        
        Args:
            user_prompt (str): The user's project requirement description
            
        Returns:
            Dict[str, Dict[str, str]]: JSON-formatted task assignments
        """
        try:
            if not user_prompt or not user_prompt.strip():
                raise ValueError("User prompt cannot be empty")

            print(f"🤖 CTO Agent: Analyzing user request...")
            print(f"📝 Request: {user_prompt}\n")

            # Step 1: Analyze the user prompt
            analysis = self.analyzer.analyze_prompt(user_prompt)
            print(f"🔍 Analysis Complete:")
            print(f"   • Features detected: {', '.join(analysis['features'])}")
            print(f"   • Complexity: {analysis['constraints']['complexity']}")
            print(f"   • Urgency: {analysis['constraints']['urgency']}\n")

            # Step 2: Decompose into tasks and assign to agents
            task_assignments = self._decompose_and_assign(analysis)
            
            # Step 3: Validate workflow rules
            if not self.orchestrator.validate_workflow(task_assignments):
                print("⚠️  Workflow validation failed. Adding required tasks...")
                task_assignments = self._ensure_workflow_compliance(task_assignments, analysis)

            # Step 4: Determine execution order
            execution_order = self.orchestrator.get_execution_order(task_assignments)
            print(f"📋 Execution Order: {' → '.join(execution_order)}\n")

            # Step 5: Format output as JSON
            result = self._format_output(task_assignments)
            
            print("✅ Task assignment complete!")
            print("📊 Final Assignment Summary:")
            for agent, assignment in result.items():
                print(f"   • {agent}: {assignment['task']}")
            
            return result

        except Exception as e:
            error_msg = f"Error processing user request: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": {"role": "System", "action": "Error", "task": error_msg}}

    def _decompose_and_assign(self, analysis: Dict[str, Any]) -> Dict[str, TaskAssignment]:
        """
        Decompose the project into tasks and assign them to appropriate agents.
        
        Args:
            analysis (Dict[str, Any]): The project analysis results
            
        Returns:
            Dict[str, TaskAssignment]: Task assignments for each agent
        """
        assignments = {}
        features = analysis['features']
        complexity = analysis['constraints']['complexity']

        # Assign backend development tasks
        if any(feature in features for feature in ['authentication', 'database', 'api']):
            backend_tasks = []
            if 'authentication' in features:
                backend_tasks.append("user authentication and authorization system")
            if 'database' in features:
                backend_tasks.append("database schema and data models")
            if 'api' in features:
                backend_tasks.append("REST API endpoints and business logic")
            
            task_desc = f"Implement {', '.join(backend_tasks)}"
            assignments[AgentRole.CODER1.value] = TaskAssignment(
                role=self.agent_capabilities[AgentRole.CODER1.value]["role"],
                action=self.agent_capabilities[AgentRole.CODER1.value]["action"],
                task=task_desc
            )

        # Assign frontend development tasks
        if 'frontend' in features:
            frontend_task = "Develop responsive user interface and client-side functionality"
            if 'authentication' in features:
                frontend_task += " including login/signup forms"
            
            assignments[AgentRole.CODER2.value] = TaskAssignment(
                role=self.agent_capabilities[AgentRole.CODER2.value]["role"],
                action=self.agent_capabilities[AgentRole.CODER2.value]["action"],
                task=frontend_task
            )

        # Always assign testing (required by workflow rules)
        test_scope = "comprehensive unit and integration tests"
        if complexity == "high":
            test_scope += " with performance and load testing"
        elif complexity == "low":
            test_scope = "basic unit tests and functionality verification"
        
        assignments[AgentRole.TESTER.value] = TaskAssignment(
            role=self.agent_capabilities[AgentRole.TESTER.value]["role"],
            action=self.agent_capabilities[AgentRole.TESTER.value]["action"],
            task=f"Perform {test_scope} on all implemented components"
        )

        # Security and DevOps tasks commented out for prototype
        # Always assign security audit (required by workflow rules)
        # security_task = "Conduct security audit and vulnerability assessment"
        # if 'authentication' in features:
        #     security_task += " with focus on authentication security"
        # if 'api' in features:
        #     security_task += " and API security validation"
        # 
        # assignments[AgentRole.SECURITY.value] = TaskAssignment(
        #     role=self.agent_capabilities[AgentRole.SECURITY.value]["role"],
        #     action=self.agent_capabilities[AgentRole.SECURITY.value]["action"],
        #     task=security_task
        # )

        # Assign deployment tasks - Commented out for prototype
        # if 'deployment' in features or complexity in ['medium', 'high']:
        #     deploy_task = "Deploy application to staging environment"
        #     if complexity == "high":
        #         deploy_task += " with containerization and orchestration setup"
        #     deploy_task += " after successful testing and security approval"
        #     
        #     assignments[AgentRole.DEVOPS.value] = TaskAssignment(
        #         role=self.agent_capabilities[AgentRole.DEVOPS.value]["role"],
        #         action=self.agent_capabilities[AgentRole.DEVOPS.value]["action"],
        #         task=deploy_task
        #     )

        return assignments

    def _ensure_workflow_compliance(self, assignments: Dict[str, TaskAssignment], 
                                  analysis: Dict[str, Any]) -> Dict[str, TaskAssignment]:
        """Ensure all required workflow steps are included."""
        # Add missing testing if needed
        if AgentRole.TESTER.value not in assignments:
            assignments[AgentRole.TESTER.value] = TaskAssignment(
                role=self.agent_capabilities[AgentRole.TESTER.value]["role"],
                action=self.agent_capabilities[AgentRole.TESTER.value]["action"],
                task="Perform mandatory testing before deployment"
            )

        # Security and DevOps compliance checks commented out for prototype
        # Add missing security audit if needed
        # if AgentRole.SECURITY.value not in assignments:
        #     assignments[AgentRole.SECURITY.value] = TaskAssignment(
        #         role=self.agent_capabilities[AgentRole.SECURITY.value]["role"],
        #         action=self.agent_capabilities[AgentRole.SECURITY.value]["action"],
        #         task="Conduct mandatory security audit before deployment"
        #     )

        return assignments

    def _format_output(self, task_assignments: Dict[str, TaskAssignment]) -> Dict[str, Dict[str, str]]:
        """Format the task assignments as the required JSON structure."""
        return {
            agent_name: assignment.to_dict()
            for agent_name, assignment in task_assignments.items()
        }

    def get_example_output(self) -> Dict[str, Dict[str, str]]:
        """
        Generate an example output for demonstration purposes.
        
        Returns:
            Dict[str, Dict[str, str]]: Example task assignments in JSON format
        """
        example_prompt = "Create a web application with user authentication and secure login functionality"
        return self.process_user_request(example_prompt)


def main():
    """
    Main function demonstrating the CTO Agent functionality.
    """
    print("=" * 60)
    print("🚀 Agentix DevOps Studio - CTO Agent Orchestrator")
    print("=" * 60)
    print()

    # Initialize the CTO Agent
    cto_agent = CTOAgent()

    # Example usage scenarios
    test_scenarios = [
        "Create a web application with user authentication and secure login functionality",
        "Build a simple REST API for a todo list application with database storage",
        "Develop a complex e-commerce platform with payment processing and inventory management"
    ]

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"📋 Test Scenario {i}:")
        print(f"   User Request: {scenario}")
        print()
        
        try:
            result = cto_agent.process_user_request(scenario)
            
            print("🎯 Generated Task Assignments (JSON):")
            print(json.dumps(result, indent=2))
            print()
            print("-" * 60)
            print()
            
        except Exception as e:
            print(f"❌ Error in scenario {i}: {str(e)}")
            print()

    print("✨ CTO Agent demonstration complete!")


if __name__ == "__main__":
    main()
