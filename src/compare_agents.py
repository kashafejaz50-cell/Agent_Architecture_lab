"""
Compare performance of different agent architectures
"""

from src.paper_env import TP_env
from src.simple_agent import SimplePaperAgent
from src.model_agent import ModelBasedPaperAgent
from src.enhanced_model_agent import EnhancedModelAgent
from src.agents import Simulate
from src.performance import PerformanceMetrics
import matplotlib.pyplot as plt


def run_agent_comparison(n_steps=100):

    agents = {
        'Simple Reflex': SimplePaperAgent(),
        'Model-Based': ModelBasedPaperAgent(),
        'Enhanced Model': EnhancedModelAgent()
    }

    results = {}
    histories = {}

    for name, agent in agents.items():

        print(f"\nRunning {name}...")

        env = TP_env()
        sim = Simulate(agent, env)
        sim.display_level = 1
        sim.go(n_steps)

        results[name] = {
            'avg_cost': PerformanceMetrics.average_cost(agent, env),
            'inv_adj_cost': PerformanceMetrics.inventory_adjusted_cost(agent, env),
            'service_level': PerformanceMetrics.service_level(agent, env),
            'final_stock': env.stock,
            'total_spent': agent.spent
        }

        histories[name] = {
            'price': env.price_history,
            'stock': env.stock_history,
            'purchases': agent.buy_history
        }

    return results, histories


def display_comparison(results):

    print("\n" + "=" * 80)
    print("AGENT COMPARISON RESULTS")
    print("=" * 80)

    print(f"\n{'Agent Type':<20} {'Avg Cost':>12} {'Inv-Adj':>12} {'Service':>10} {'Final Stock':>12}")
    print("-" * 70)

    for name, metrics in results.items():
        print(f"{name:<20} ${metrics['avg_cost']:>10.2f} "
              f"${metrics['inv_adj_cost']:>10.2f} "
              f"{metrics['service_level']:>9.2%} "
              f"{metrics['final_stock']:>11}")

    print("\n" + "=" * 80)

    best_cost = min(results.items(), key=lambda x: x[1]['avg_cost'])
    best_inv = min(results.items(), key=lambda x: x[1]['inv_adj_cost'])
    best_service = min(results.items(), key=lambda x: x[1]['service_level'])

    print("\n🏆 WINNERS:")
    print(f"Best Average Cost: {best_cost[0]} (${best_cost[1]['avg_cost']:.2f})")
    print(f"Best Inventory-Adjusted: {best_inv[0]} (${best_inv[1]['inv_adj_cost']:.2f})")
    print(f"Best Service Level: {best_service[0]} ({best_service[1]['service_level']:.2%})")


def plot_comparison(histories):

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    colors = {
        'Simple Reflex': 'blue',
        'Model-Based': 'green',
        'Enhanced Model': 'red'
    }

    # Price history
    ax = axes[0, 0]
    for name, history in histories.items():
        ax.plot(history['price'], label=name, color=colors[name], alpha=0.7)
    ax.set_title('Price History')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Price')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Stock levels
    ax = axes[0, 1]
    for name, history in histories.items():
        ax.plot(history['stock'], label=name, color=colors[name], alpha=0.7)
    ax.set_title('Inventory Levels')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Stock')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)

    # Purchases
    ax = axes[1, 0]
    for name, history in histories.items():
        ax.plot(history['purchases'], label=name, color=colors[name], alpha=0.7)
    ax.set_title('Purchase Behavior')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Quantity')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Cumulative spending
    ax = axes[1, 1]
    for name, history in histories.items():
        cumulative = []
        total = 0

        for i, buy in enumerate(history['purchases']):
            price = history['price'][i] if i < len(history['price']) else 0
            total += buy * price
            cumulative.append(total)

        ax.plot(cumulative, label=name, color=colors[name], alpha=0.7)

    ax.set_title('Cumulative Spending')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Cost')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # IMPORTANT: create folder first
    import os
    os.makedirs("results", exist_ok=True)

    plt.savefig("results/agent_comparison.png", dpi=150)
    plt.show()

    print("\nPlot saved to 'results/agent_comparison.png'")


if __name__ == "__main__":
    print("RUNNING AGENT COMPARISON...")
    results, histories = run_agent_comparison(100)
    display_comparison(results)
    plot_comparison(histories)