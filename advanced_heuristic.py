# advanced_heuristic.py
from tron_base import TronGame, flood_fill
# from tron_agents import GreedyAgent
from copy import deepcopy
from greedy import GreedyAgent
from minimax import MinimaxAgent
import time

def find_articulation_points(board, start_pos, player_id):
    """
    Find articulation points - moves that would split opponent's space.
    Returns the number of separate regions opponent would be split into.
    """
    opponent_id = 3 - player_id
    
    # Find opponent's reachable space
    opponent_space = set()
    stack = [start_pos]
    visited = set()
    height, width = board.shape
    
    # First, identify all cells reachable by opponent
    opp_pos = None
    for y in range(height):
        for x in range(width):
            if board[y, x] == opponent_id:
                opp_pos = (y, x)
                break
        if opp_pos:
            break
    
    if not opp_pos:
        return 1
    
    # Flood fill from opponent position to find their territory
    stack = [opp_pos]
    visited = set()
    while stack:
        pos = stack.pop()
        if pos in visited:
            continue
        y, x = pos
        if not (0 <= y < height and 0 <= x < width):
            continue
        if board[y, x] != 0 and board[y, x] != opponent_id:
            continue
        
        visited.add(pos)
        opponent_space.add(pos)
        
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            stack.append((y + dy, x + dx))
    
    # Now check if our move at start_pos splits opponent's space
    # Count connected components in opponent_space excluding start_pos
    remaining_space = opponent_space - {start_pos}
    
    if not remaining_space:
        return 1
    
    # Count connected components
    components = 0
    unvisited = remaining_space.copy()
    
    while unvisited:
        components += 1
        start = unvisited.pop()
        stack = [start]
        component_visited = set()
        
        while stack:
            pos = stack.pop()
            if pos in component_visited:
                continue
            if pos not in remaining_space:
                continue
            
            component_visited.add(pos)
            unvisited.discard(pos)
            
            y, x = pos
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (y + dy, x + dx)
                if neighbor in remaining_space and neighbor not in component_visited:
                    stack.append(neighbor)
    
    return components

def advanced_evaluate(board, p1_pos, p2_pos):
    """
    Advanced evaluation considering:
    1. Space control (like greedy)
    2. Articulation points (cutting off opponent)
    3. Voronoi territory (cells closer to you)
    """
    # Basic space control
    p1_space = flood_fill(board, p1_pos, 1)
    p2_space = flood_fill(board, p2_pos, 2)
    space_diff = p1_space - p2_space
    
    # Articulation bonus: does our position split opponent's space?
    p1_splits = find_articulation_points(board, p1_pos, 1)
    p2_splits = find_articulation_points(board, p2_pos, 2)
    articulation_bonus = (p1_splits - p2_splits) * 10  # Weight articulation points heavily
    
    # Voronoi territory - cells closer to us than opponent
    height, width = board.shape
    voronoi_score = 0
    
    for y in range(height):
        for x in range(width):
            if board[y, x] == 0:  # Empty cell
                dist_p1 = abs(y - p1_pos[0]) + abs(x - p1_pos[1])
                dist_p2 = abs(y - p2_pos[0]) + abs(x - p2_pos[1])
                if dist_p1 < dist_p2:
                    voronoi_score += 1
                elif dist_p2 < dist_p1:
                    voronoi_score -= 1
    
    # Combined score
    return space_diff + articulation_bonus + voronoi_score * 0.5

class AdvancedMinimaxAgent:
    """Minimax with articulation-point aware evaluation"""
    
    def __init__(self, depth=5):
        self.depth = depth
        self.nodes_evaluated = 0
    
    def evaluate_state(self, board, p1_pos, p2_pos):
        """Use advanced evaluation function"""
        return advanced_evaluate(board, p1_pos, p2_pos)
    
    def minimax(self, state, depth, alpha, beta, maximizing_player):
        """Minimax with alpha-beta pruning"""
        self.nodes_evaluated += 1
        if depth == 0 or not state['p1_moves'] or not state['p2_moves']:
            return self.evaluate_state(state['board'], state['p1_pos'], state['p2_pos'])
        
        if maximizing_player:
            max_eval = float('-inf')
            for action in state['p1_moves']:
                new_state = self.simulate_move(state, action, None, 1)
                eval_score = self.minimax(new_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for action in state['p2_moves']:
                new_state = self.simulate_move(state, None, action, 2)
                eval_score = self.minimax(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def simulate_move(self, state, p1_action, p2_action, player):
        """Create new state after hypothetical move"""
        new_state = deepcopy(state)
        directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        
        if player == 1 and p1_action:
            dy, dx = directions[p1_action]
            new_pos = (state['p1_pos'][0] + dy, state['p1_pos'][1] + dx)
            new_state['board'][new_pos] = 1
            new_state['p1_pos'] = new_pos
            new_state['p1_moves'] = self.get_valid_moves_from_board(new_state['board'], new_pos)
        
        if player == 2 and p2_action:
            dy, dx = directions[p2_action]
            new_pos = (state['p2_pos'][0] + dy, state['p2_pos'][1] + dx)
            new_state['board'][new_pos] = 2
            new_state['p2_pos'] = new_pos
            new_state['p2_moves'] = self.get_valid_moves_from_board(new_state['board'], new_pos)
        
        return new_state
    
    def get_valid_moves_from_board(self, board, pos):
        """Helper to get valid moves from board state"""
        moves = []
        directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        height, width = board.shape
        
        for action, (dy, dx) in directions.items():
            new_y, new_x = pos[0] + dy, pos[1] + dx
            if (0 <= new_y < height and 0 <= new_x < width and board[new_y, new_x] == 0):
                moves.append(action)
        return moves
    
    def get_action(self, state, player):
        """Select best action using minimax"""
        self.nodes_evaluated = 0
        moves = state['p1_moves'] if player == 1 else state['p2_moves']
        if not moves:
            return None
        
        best_action = moves[0]
        best_value = float('-inf') if player == 1 else float('inf')
        
        for action in moves:
            new_state = self.simulate_move(state, action if player == 1 else None, 
                                          action if player == 2 else None, player)
            value = self.minimax(new_state, self.depth - 1, float('-inf'), float('inf'), 
                               player == 2)
            
            if player == 1 and value > best_value:
                best_value = value
                best_action = action
            elif player == 2 and value < best_value:
                best_value = value
                best_action = action
        
        return best_action

def compare_heuristics(num_games=15, depth=5, board_size=10):
    """Compare standard minimax vs advanced minimax"""
    print(f"\n{'='*70}")
    print(f"HEURISTIC COMPARISON: Standard vs Advanced Evaluation")
    print(f"Board: {board_size}x{board_size}, Depth: {depth}")
    print(f"{'='*70}\n")
    
    # from tron_agents import MinimaxAgent
    
    standard = MinimaxAgent(depth=depth)
    advanced = AdvancedMinimaxAgent(depth=depth)
    greedy = GreedyAgent()
    
    matchups = [
        ("Advanced Minimax", advanced, "Standard Minimax", standard),
        ("Advanced Minimax", advanced, "Greedy", greedy),
        ("Standard Minimax", standard, "Greedy", greedy)
    ]
    
    results = {}
    
    for name1, agent1, name2, agent2 in matchups:
        print(f"\n--- {name1} vs {name2} ({num_games} games) ---")
        
        wins1 = 0
        wins2 = 0
        draws = 0
        total_time = 0
        
        for game_num in range(num_games):
            game = TronGame(width=board_size, height=board_size)
            state = game.reset()
            moves = 0
            
            start = time.time()
            
            while not game.game_over and moves < 150:
                a1 = agent1.get_action(state, 1)
                a2 = agent2.get_action(state, 2)
                state, reward, done = game.step(a1, a2)
                moves += 1
            
            elapsed = time.time() - start
            total_time += elapsed
            
            if game.winner == 1:
                wins1 += 1
            elif game.winner == 2:
                wins2 += 1
            else:
                draws += 1
        
        win_rate1 = wins1 / num_games * 100
        avg_time = total_time / num_games
        
        results[f"{name1}_vs_{name2}"] = {
            'wins1': wins1,
            'wins2': wins2,
            'draws': draws,
            'win_rate': win_rate1,
            'avg_time': avg_time
        }
        
        print(f"  {name1}: {wins1}, {name2}: {wins2}, Draws: {draws}")
        print(f"  {name1} Win Rate: {win_rate1:.1f}%")
        print(f"  Avg Time/Game: {avg_time:.2f}s")
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    for matchup, stats in results.items():
        print(f"\n{matchup}:")
        print(f"  Win Rate: {stats['win_rate']:.1f}%")
        print(f"  Avg Time: {stats['avg_time']:.2f}s")
    
    return results

if __name__ == "__main__":
    # Test on standard board
    print("\n" + "="*70)
    print("TEST 1: Standard 10x10 Board")
    print("="*70)
    compare_heuristics(num_games=15, depth=5, board_size=10)
    
    # Test on small board where tactics matter more
    print("\n\n" + "="*70)
    print("TEST 2: Small 6x6 Board (Tactics-Heavy)")
    print("="*70)
    compare_heuristics(num_games=15, depth=4, board_size=6)
    
