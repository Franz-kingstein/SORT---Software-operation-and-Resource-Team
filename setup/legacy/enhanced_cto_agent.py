#!/usr/bin/env python3
"""
Agentix DevOps Studio - LangChain + CrewAI Enhanced CTO Agent
==============================================================

This module implements an enhanced version of the CTO agent orchestrator using
LangChain for LLM interactions and CrewAI for multi-agent orchestration.

Features:
- LangChain integration for sophisticated LLM interactions
- CrewAI for agent coordination and task delegation
- Fallback to rule-based system when LLM is unavailable
- Support for multiple LLM providers (OpenAI, Anthropic, Ollama)

Author: GitHub Copilot
Date: September 1, 2025
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# LangChain imports
from langchain.llms import OpenAI, Ollama
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.callbacks.base import BaseCallbackHandler

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool

# Pydantic for structured output
from pydantic import BaseModel, Field, validator

# Local imports - fallback to rule-based system
try:
    from main_llm_agent import CTOAgent as RuleBasedCTOAgent, ProjectAnalyzer, WorkflowOrchestrator
    FALLBACK_AVAILABLE = True
except ImportError:
    FALLBACK_AVAILABLE = False


class TaskAssignmentOutput(BaseModel):
    """Structured output model for task assignments."""
    assignments: Dict[str, Dict[str, str]] = Field(
        description="Dictionary of agent assignments in format: {'agent_name': {'role': 'Role', 'action': 'Action', 'task': 'Task Description'}}"
    )
    priority_order: List[str] = Field(
        description="List of agent names in execution order"
    )
    estimated_duration: Optional[str] = Field(
        description="Estimated completion time",
        default=None
    )
    
    @validator('assignments')
    def validate_assignments(cls, v):
        """Validate that each assignment has required fields."""
        for agent_name, assignment in v.items():
            required_fields = {'role', 'action', 'task'}
            if not all(field in assignment for field in required_fields):
                raise ValueError(f"Assignment for {agent_name} missing required fields: {required_fields}")
        return v


class AgentixCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for monitoring LLM interactions."""
    
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0
        self.interactions = []
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        """Called when LLM starts running."""
        print("🤖 LLM Starting...")
    
    def on_llm_end(self, response, **kwargs) -> None:
        """Called when LLM ends running."""
        print("✅ LLM Completed")
        self.interactions.append({
            'timestamp': datetime.now().isoformat(),
            'response': str(response)
        })


class DevOpsCodeTool(BaseTool):
    """Custom tool for code generation tasks."""
    
    name: str = "DevOps Code Generator"
    description: str = "Generate code for DevOps tasks including backend APIs, frontend interfaces, and tests"
    
    def _run(self, task_description: str, agent_type: str = "coder") -> str:
        """Generate code based on task description."""
        # This would interface with the existing code generation logic
        templates = {
            "backend": "Flask/FastAPI application with database models",
            "frontend": "React/Vue components with responsive design",
            "testing": "Pytest test suites with fixtures and mocking"
        }
        
        return f"Generated {agent_type} code for: {task_description}\nTemplate: {templates.get(agent_type, 'Generic code template')}"
    
    async def _arun(self, task_description: str, agent_type: str = "coder") -> str:
        """Async version of the tool."""
        return self._run(task_description, agent_type)


class EnhancedCTOAgent:
    """
    Enhanced CTO Agent using LangChain and CrewAI for sophisticated task orchestration.
    """
    
    def __init__(self, 
                 model_provider: str = "openai",
                 model_name: str = "gpt-3.5-turbo",
                 temperature: float = 0.3,
                 use_fallback: bool = True):
        """
        Initialize the enhanced CTO agent.
        
        Args:
            model_provider: LLM provider ("openai", "anthropic", "ollama")
            model_name: Specific model to use
            temperature: Creativity level (0.0 to 1.0)
            use_fallback: Whether to use rule-based fallback if LLM fails
        """
        self.model_provider = model_provider
        self.model_name = model_name
        self.temperature = temperature
        self.use_fallback = use_fallback
        self.callback_handler = AgentixCallbackHandler()
        
        # Initialize LLM
        self.llm = self._initialize_llm()
        
        # Initialize output parser
        self.output_parser = PydanticOutputParser(pydantic_object=TaskAssignmentOutput)
        self.fixing_parser = OutputFixingParser.from_llm(parser=self.output_parser, llm=self.llm)
        
        # Initialize CrewAI agents
        self.crew_agents = self._initialize_crew_agents()
        
        # Initialize fallback system
        if self.use_fallback and FALLBACK_AVAILABLE:
            self.fallback_agent = RuleBasedCTOAgent()
            print("🔄 Fallback system initialized")
        else:
            self.fallback_agent = None
    
    def _initialize_llm(self):
        """Initialize the appropriate LLM based on provider."""
        try:
            if self.model_provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable not set")
                
                if "gpt-4" in self.model_name or "gpt-3.5" in self.model_name:
                    return ChatOpenAI(
                        model_name=self.model_name,
                        temperature=self.temperature,
                        callbacks=[self.callback_handler]
                    )
                else:
                    return OpenAI(
                        model_name=self.model_name,
                        temperature=self.temperature,
                        callbacks=[self.callback_handler]
                    )
            
            elif self.model_provider == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY environment variable not set")
                
                return ChatAnthropic(
                    model=self.model_name,
                    temperature=self.temperature,
                    callbacks=[self.callback_handler]
                )
            
            elif self.model_provider == "ollama":
                return Ollama(
                    model=self.model_name,
                    temperature=self.temperature,
                    callbacks=[self.callback_handler]
                )
            
            else:
                raise ValueError(f"Unsupported model provider: {self.model_provider}")
                
        except Exception as e:
            print(f"⚠️ Failed to initialize LLM: {e}")
            if self.use_fallback:
                print("🔄 Will use fallback system")
                return None
            else:
                raise
    
    def _initialize_crew_agents(self) -> Dict[str, Agent]:
        """Initialize CrewAI agents for the development team."""
        
        # Custom tool for code generation
        code_tool = DevOpsCodeTool()
        
        agents = {}
        
        # Backend Developer Agent
        agents["backend_coder"] = Agent(
            role="Senior Backend Developer",
            goal="Develop robust, scalable backend systems with APIs, databases, and authentication",
            backstory="""You are an experienced backend developer with expertise in Python, Flask, FastAPI, 
            database design, and API development. You create production-ready backend systems with proper 
            security, error handling, and performance optimization.""",
            tools=[code_tool],
            llm=self.llm,
            verbose=True,
            memory=True,
            allow_delegation=False
        )
        
        # Frontend Developer Agent
        agents["frontend_coder"] = Agent(
            role="Senior Frontend Developer", 
            goal="Create beautiful, responsive user interfaces with modern web technologies",
            backstory="""You are a skilled frontend developer specializing in React, Vue.js, HTML5, CSS3, 
            and JavaScript. You build user-friendly interfaces with responsive design, accessibility, 
            and optimal user experience.""",
            tools=[code_tool],
            llm=self.llm,
            verbose=True,
            memory=True,
            allow_delegation=False
        )
        
        # QA/Testing Agent
        agents["tester"] = Agent(
            role="Senior QA Engineer",
            goal="Ensure code quality through comprehensive testing strategies",
            backstory="""You are an expert QA engineer with deep knowledge of testing frameworks, 
            test automation, performance testing, and quality assurance. You create thorough test 
            suites that catch bugs early and ensure system reliability.""",
            tools=[code_tool],
            llm=self.llm,
            verbose=True,
            memory=True,
            allow_delegation=False
        )
        
        return agents
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the CTO agent."""
        return """You are an expert CTO and technical leader responsible for analyzing project requirements 
        and coordinating development teams. Your role is to:

        1. Analyze user requirements thoroughly
        2. Break down projects into specific, actionable tasks
        3. Assign tasks to the most appropriate team members
        4. Ensure proper execution order and dependencies
        5. Maintain high code quality and best practices

        Available team members:
        - Backend Developer (backend_coder): APIs, databases, authentication, server-side logic
        - Frontend Developer (frontend_coder): User interfaces, client-side functionality, responsive design  
        - QA Engineer (tester): Testing strategies, test automation, quality assurance

        You must output task assignments in this exact JSON format:
        {
            "agent_name": {
                "role": "Agent Role Description",
                "action": "Action Type (Write code/Test code)",
                "task": "Specific detailed task description"
            }
        }

        Guidelines:
        - Be specific and detailed in task descriptions
        - Consider dependencies between tasks
        - Prioritize backend development before frontend when there are API dependencies
        - Always include testing after development tasks
        - Use clear, actionable language
        """
    
    async def process_user_request(self, user_prompt: str) -> Dict[str, Any]:
        """
        Process user request and generate task assignments using LangChain + CrewAI.
        
        Args:
            user_prompt: The user's project requirements
            
        Returns:
            Dict containing task assignments and metadata
        """
        print(f"🎯 Enhanced CTO Agent: Processing request...")
        print(f"📝 User Request: {user_prompt}")
        
        try:
            # Use LangChain for intelligent analysis
            if self.llm:
                result = await self._process_with_langchain(user_prompt)
                if result:
                    return result
            
            # Fallback to rule-based system
            if self.fallback_agent:
                print("🔄 Using fallback rule-based system...")
                return self.fallback_agent.process_user_request(user_prompt)
            
            # Last resort - basic response
            return {
                "error": "No LLM available and no fallback system",
                "suggestion": "Please configure API keys or enable fallback system"
            }
            
        except Exception as e:
            print(f"❌ Error in process_user_request: {e}")
            
            # Try fallback
            if self.fallback_agent:
                print("🔄 Error occurred, using fallback system...")
                return self.fallback_agent.process_user_request(user_prompt)
            
            return {"error": str(e)}
    
    async def _process_with_langchain(self, user_prompt: str) -> Optional[Dict[str, Any]]:
        """Process request using LangChain LLM."""
        try:
            # Create prompt template
            system_prompt = self._create_system_prompt()
            
            prompt_template = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_prompt),
                HumanMessagePromptTemplate.from_template("""
                Analyze this project requirement and create task assignments:
                
                Project Description: {user_request}
                
                {format_instructions}
                
                Focus on:
                1. Understanding the core requirements
                2. Identifying necessary components (backend, frontend, testing)
                3. Creating specific, actionable tasks
                4. Proper dependency ordering
                
                Output the task assignments in the required JSON format.
                """)
            ])
            
            # Format the prompt
            formatted_prompt = prompt_template.format_prompt(
                user_request=user_prompt,
                format_instructions=self.output_parser.get_format_instructions()
            )
            
            # Get LLM response
            response = await self.llm.agenerate([formatted_prompt.to_messages()])
            raw_output = response.generations[0][0].text
            
            print(f"🤖 LLM Raw Output: {raw_output}")
            
            # Parse the structured output
            try:
                parsed_output = self.fixing_parser.parse(raw_output)
                
                # Convert to the expected format
                result = {
                    "task_assignments": parsed_output.assignments,
                    "execution_order": parsed_output.priority_order,
                    "estimated_duration": parsed_output.estimated_duration,
                    "analysis_method": "langchain_llm",
                    "model_used": f"{self.model_provider}:{self.model_name}",
                    "timestamp": datetime.now().isoformat()
                }
                
                print(f"✅ LangChain processing completed successfully")
                return result
                
            except Exception as parse_error:
                print(f"⚠️ Failed to parse LLM output: {parse_error}")
                print(f"Raw output was: {raw_output}")
                
                # Try to extract JSON manually
                return self._extract_json_manually(raw_output, user_prompt)
                
        except Exception as e:
            print(f"⚠️ LangChain processing failed: {e}")
            return None
    
    def _extract_json_manually(self, raw_output: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """Manually extract JSON from LLM output as fallback."""
        try:
            import re
            
            # Look for JSON-like structures
            json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                task_assignments = json.loads(json_str)
                
                return {
                    "task_assignments": task_assignments,
                    "execution_order": list(task_assignments.keys()),
                    "analysis_method": "manual_extraction",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"⚠️ Manual JSON extraction failed: {e}")
        
        return None
    
    async def execute_with_crew(self, task_assignments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute tasks using CrewAI orchestration.
        
        Args:
            task_assignments: Task assignments from the CTO agent
            
        Returns:
            Dict containing execution results
        """
        print("🚀 Starting CrewAI execution...")
        
        try:
            tasks = []
            
            # Create CrewAI tasks from assignments
            for agent_name, assignment in task_assignments.get("task_assignments", {}).items():
                
                # Map agent names to CrewAI agents
                crew_agent = None
                if "backend" in agent_name.lower() or "coder1" in agent_name.lower():
                    crew_agent = self.crew_agents["backend_coder"]
                elif "frontend" in agent_name.lower() or "coder2" in agent_name.lower():
                    crew_agent = self.crew_agents["frontend_coder"]
                elif "test" in agent_name.lower():
                    crew_agent = self.crew_agents["tester"]
                
                if crew_agent:
                    task = Task(
                        description=assignment["task"],
                        agent=crew_agent,
                        expected_output=f"Completed {assignment['action'].lower()} for: {assignment['task']}"
                    )
                    tasks.append(task)
            
            if not tasks:
                return {"error": "No valid tasks created for CrewAI execution"}
            
            # Create and run the crew
            crew = Crew(
                agents=list(self.crew_agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the crew
            result = crew.kickoff()
            
            return {
                "success": True,
                "execution_method": "crewai",
                "result": str(result),
                "tasks_completed": len(tasks),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ CrewAI execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "execution_method": "crewai_failed"
            }
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics and costs."""
        return {
            "total_interactions": len(self.callback_handler.interactions),
            "model_provider": self.model_provider,
            "model_name": self.model_name,
            "fallback_available": self.fallback_agent is not None,
            "recent_interactions": self.callback_handler.interactions[-5:] if self.callback_handler.interactions else []
        }


def main():
    """Test the enhanced CTO agent."""
    import asyncio
    
    async def test_enhanced_agent():
        # Initialize enhanced agent
        cto_agent = EnhancedCTOAgent(
            model_provider="openai",  # Change to "ollama" for local models
            model_name="gpt-3.5-turbo",
            use_fallback=True
        )
        
        # Test scenarios
        test_scenarios = [
            "Create a user authentication system with login/signup functionality",
            "Build a task management application with CRUD operations and responsive UI",
            "Develop an e-commerce platform with shopping cart and payment integration"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n{'='*60}")
            print(f"🧪 TEST SCENARIO {i}: {scenario}")
            print(f"{'='*60}")
            
            # Process with enhanced agent
            result = await cto_agent.process_user_request(scenario)
            
            print(f"\n📊 RESULT:")
            print(json.dumps(result, indent=2))
            
            # If we got task assignments, try executing with CrewAI
            if "task_assignments" in result and cto_agent.llm:
                print(f"\n🚀 Executing with CrewAI...")
                crew_result = await cto_agent.execute_with_crew(result)
                print(f"CrewAI Result: {json.dumps(crew_result, indent=2)}")
        
        # Print usage stats
        print(f"\n📈 USAGE STATISTICS:")
        stats = cto_agent.get_usage_stats()
        print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
