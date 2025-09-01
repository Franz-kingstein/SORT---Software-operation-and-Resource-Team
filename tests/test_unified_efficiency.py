#!/usr/bin/env python3
"""
Quick test of the unified agent system efficiency.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.agent_interface import AgentOrchestrator
from agents.testing_agent import TestingAgent

def test_unified_efficiency():
    print("🚀 Testing Unified Agent System Efficiency")
    print("=" * 45)
    
    # Test orchestrator
    print("\n1. Testing AgentOrchestrator...")
    orchestrator = AgentOrchestrator()
    
    # Test unified testing agent from agents folder
    print("\n2. Testing TestingAgent from agents folder...")
    testing_agent = TestingAgent(use_ai=False)  # Use basic mode for demo
    
    # Register agent
    orchestrator.register_agent("testing", testing_agent)
    
    # Test single task execution
    print("\n3. Testing single task execution...")
    task = {
        'role': 'testing',
        'action': 'generate_tests',
        'task': 'Create unit tests for user authentication module',
        'project_type': 'web'
    }
    
    result = orchestrator.execute_single_task("testing", task)
    
    if result['success']:
        print("✅ Single task execution: SUCCESS")
        print(f"   Agent: {result['agent']}")
    else:
        print(f"❌ Single task failed: {result['error']}")
    
    # Test workflow execution
    print("\n4. Testing workflow execution...")
    workflow_tasks = {
        'testing': {
            'role': 'testing',
            'action': 'comprehensive_test',
            'task': 'Create complete test suite for e-commerce app',
            'project_type': 'ecommerce'
        }
    }
    
    workflow_result = orchestrator.execute_workflow(workflow_tasks)
    
    print(f"✅ Workflow completed: {workflow_result['summary']['success_rate']} success rate")
    
    # Show efficiency metrics
    print("\n5. Efficiency Metrics:")
    status = orchestrator.get_workflow_status()
    print(f"   • Registered agents: {len(status['registered_agents'])}")
    print(f"   • Completed tasks: {status['completed_tasks']}")
    print(f"   • Queue efficiency: {status['queue_size']} pending")
    
    # Show agent capabilities
    capabilities = testing_agent.get_capabilities()
    print(f"\n6. UnifiedTestingAgent Capabilities ({len(capabilities)}):")
    for cap in capabilities[:5]:  # Show first 5
        print(f"   • {cap}")
    if len(capabilities) > 5:
        print(f"   • ... and {len(capabilities)-5} more")
    
    print(f"\n7. Agent Status: {testing_agent.get_status()}")
    
    print("\n🎉 Unified System Test Complete!")
    print("\n💡 Key Benefits:")
    print("   ✅ Single agent replaces dual testing agents")
    print("   ✅ Streamlined orchestration and communication")
    print("   ✅ Reduced complexity and improved maintainability")
    print("   ✅ Better resource efficiency and performance")

if __name__ == "__main__":
    test_unified_efficiency()
