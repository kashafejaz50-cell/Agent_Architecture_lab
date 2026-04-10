"""
Test script for paper buying agent
"""

from src.paper_env import TP_env
from src.simple_agent import SimplePaperAgent
from src.agents import Simulate


def test_simple_agent():
    """Run a simple test of the agent-environment interaction"""

    print("=" * 60)
    print("TESTING SIMPLE PAPER BUYING AGENT")
    print("=" * 60)

    # Create environment and agent
    env = TP_env()
    agent = SimplePaperAgent()

    # Run simulation
    sim = Simulate(agent, env)
    sim.display_level = 2  # show detailed logs

    sim.go(20)  # run for 20 steps

    # Print results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    print(f"Total money spent: ${agent.spent:.2f}")
    print(f"Average cost per step: ${agent.spent / env.time:.2f}")
    print(f"Final stock level: {env.stock} sheets")
    print(f"Final price: ${env.price}")

    return agent, env


if __name__ == "__main__":
    test_simple_agent()