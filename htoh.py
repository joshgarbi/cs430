# Import all components from our modules
from tron_base import TronGame, RandomAgent
from greedy import GreedyAgent
from minimax import MinimaxAgent
from mcts import MCTSAgent
from advanced_heuristic import AdvancedMinimaxAgent
import time

# Define all agents using our imported classes
agents = {
    'Minimax-5': MinimaxAgent(depth=5),
    'Minimax-7': MinimaxAgent(depth=7),
    'MCTS-500': MCTSAgent(simulations=500),
    'MCTS-200': MCTSAgent(simulations=200),
    'AdvMinimax-5': AdvancedMinimaxAgent(depth=5),
    'AdvMinimax-7': AdvancedMinimaxAgent(depth=7),
    'Greedy': GreedyAgent(),
    'Random': RandomAgent(),
}

# Tournament function
def run_round_robin_tournament(games_per_matchup=3):
    """Run round-robin tournament between all agents"""
    print("\n=== ROUND-ROBIN TOURNAMENT ===")
    print("(Each matchup: {} games, 10x10 grid)\n".format(games_per_matchup))
    
    results = {name: {'wins': 0, 'losses': 0, 'draws': 0, 'time': 0} for name in agents}
    
    agent_names = list(agents.keys())
    for i, name1 in enumerate(agent_names):
        for name2 in agent_names[i+1:]:
            print(f"\n{name1} vs {name2}:")
            
            for game_num in range(games_per_matchup):
                game = TronGame(width=20, height=20)
                state = game.reset()
                moves = 0
                
                start_time = time.time()
                while not game.game_over and moves < 100:
                    a1 = agents[name1].get_action(state, 1)
                    a2 = agents[name2].get_action(state, 2)
                    state, reward, done = game.step(a1, a2)
                    moves += 1
                elapsed = time.time() - start_time
                
                if game.winner == 1:
                    results[name1]['wins'] += 1
                    results[name2]['losses'] += 1
                    print(f"  Game {game_num + 1}: {name1} wins ({moves} moves, {elapsed:.2f}s)")
                elif game.winner == 2:
                    results[name2]['wins'] += 1
                    results[name1]['losses'] += 1
                    print(f"  Game {game_num + 1}: {name2} wins ({moves} moves, {elapsed:.2f}s)")
                else:
                    results[name1]['draws'] += 1
                    results[name2]['draws'] += 1
                    print(f"  Game {game_num + 1}: Draw ({moves} moves, {elapsed:.2f}s)")
                
                results[name1]['time'] += elapsed / 2
                results[name2]['time'] += elapsed / 2
    
    # Display final standings
    print("\n" + "="*60)
    print("FINAL STANDINGS")
    print("="*60)
    print(f"{'Agent':<15} {'Wins':>6} {'Losses':>6} {'Draws':>6} {'Win%':>6} {'Avg Time':>10}")
    print("-"*60)
    
    sorted_agents = sorted(results.items(), key=lambda x: x[1]['wins'], reverse=True)
    for name, stats in sorted_agents:
        total_games = stats['wins'] + stats['losses'] + stats['draws']
        win_pct = (stats['wins'] / total_games * 100) if total_games > 0 else 0
        avg_time = stats['time'] / total_games if total_games > 0 else 0
        print(f"{name:<15} {stats['wins']:>6} {stats['losses']:>6} {stats['draws']:>6} {win_pct:>5.1f}% {avg_time:>9.3f}s")
    
    return results

# Test code when run directly
if __name__ == "__main__":
    run_round_robin_tournament(3)