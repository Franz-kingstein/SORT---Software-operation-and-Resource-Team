# Example usage for orchestrator
# Run this script to test the full agent pipeline
from src.sort.crew.orchestrator import CrewOrchestrator

if __name__ == "__main__":
    orchestrator = CrewOrchestrator()
    prompt = "Create a Python script that prints Fibonacci numbers up to 100."
    result = orchestrator.run_pipeline(prompt)
    print("\n--- Pipeline Result ---")
    for k, v in result.items():
        print(f"{k}:\n{v}\n")
