# mcts.py - Add to this file

from tron_base import TronGame, flood_fill
from greedy import GreedyAgent
import math
import random
from copy import deepcopy
import time
# MCTS implementation
import math
import random
import copy


class MCTSNode:
    def __init__(self, state, player, parent=None, move=None):
        self.state = state
        self.player = player            # player TO MOVE at this node
        self.parent = parent
        self.move = move

        self.children = []
        self.visits = 0
        self.value = 0.0

        self.untried_actions = self.get_moves()

    def get_moves(self):
        return self.state['p1_moves'][:] if self.player == 1 else self.state['p2_moves'][:]

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c=math.sqrt(2)):
        return max(
            self.children,
            key=lambda child: (
                child.value / child.visits
                + c * math.sqrt(math.log(self.visits) / child.visits)
            )
        )


class MCTSAgent:
    def __init__(self, simulations=200):
        self.simulations = simulations

    def search(self, root_state, player):
        self.root_player = player
        root = MCTSNode(copy.deepcopy(root_state), player)

        if self.is_terminal(root_state):
            return None

        for _ in range(self.simulations):
            node = self.select(root)
            result = self.simulate(node.state, node.player)
            self.backpropagate(node, result)

        if not root.children:
            moves = root_state['p1_moves'] if player == 1 else root_state['p2_moves']
            return random.choice(moves) if moves else None

        return max(root.children, key=lambda c: c.visits).move



    def get_action(self, state, player):
        return self.search(state, player)


    # ------------------------
    # Selection + Expansion
    # ------------------------

    def select(self, node):
        while True:
            # If terminal, return immediately
            terminal_value = self.is_terminal(node.state)
            if terminal_value is not None:
                return node

            # If node has moves to expand, expand one
            if not node.is_fully_expanded():
                return self.expand(node)

            # Node fully expanded: go to best child if it exists
            if node.children:
                node = node.best_child()
            else:
                # Node has no children and no moves → treat as terminal
                return node



    def expand(self, node):
        move = node.untried_actions.pop()
        next_state = copy.deepcopy(node.state)
        self.apply_move(next_state, move, node.player)

        next_player = 3 - node.player
        child = MCTSNode(
            state=next_state,
            player=next_player,
            parent=node,
            move=move
        )
        node.children.append(child)
        return child

    # ------------------------
    # Simulation (Rollout)
    # ------------------------

    def simulate(self, state, player, max_depth=200):
        current_state = copy.deepcopy(state)
        current_player = player
        depth = 0

        while depth < max_depth:
            terminal_value = self.is_terminal(current_state)
            if terminal_value is not None:
                return terminal_value

            moves = (
                current_state['p1_moves'] if current_player == 1 else current_state['p2_moves']
            )
            if not moves:  # No moves → current player loses
                return -1 if current_player == self.root_player else 1

            move = random.choice(moves)
            self.apply_move(current_state, move, current_player)
            current_player = 3 - current_player
            depth += 1

        return 0  # Timeout = draw


    # ------------------------
    # Backpropagation
    # ------------------------

    def backpropagate(self, node, result):
        while node:
            node.visits += 1
            node.value += result
            node = node.parent

    # ------------------------
    # Terminal Evaluation
    # ------------------------

    def is_terminal(self, state):
        if 'loser' in state:
            winner = 3 - state['loser']
            return 1 if winner == self.root_player else -1
        return None

        
    def apply_move(self, state, action, player):
        directions = {
            'UP': (-1, 0), 'DOWN': (1, 0),
            'LEFT': (0, -1), 'RIGHT': (0, 1)
        }

        pos = state['p1_pos'] if player == 1 else state['p2_pos']
        dy, dx = directions[action]
        new_pos = (pos[0] + dy, pos[1] + dx)

        h, w = state['board'].shape
        if not (0 <= new_pos[0] < h and 0 <= new_pos[1] < w):
            state['p1_moves'] = []
            state['p2_moves'] = []
            state['loser'] = player
            return

        if state['board'][new_pos] != 0:
            state['p1_moves'] = []
            state['p2_moves'] = []
            state['loser'] = player
            return

        state['board'][new_pos] = player

        if player == 1:
            state['p1_pos'] = new_pos
        else:
            state['p2_pos'] = new_pos

        state['p1_moves'] = self.get_valid_moves(state['board'], state['p1_pos'])
        state['p2_moves'] = self.get_valid_moves(state['board'], state['p2_pos'])

    
    def get_valid_moves(self, board, pos):
        """Get valid moves from position"""
        moves = []
        directions = {'UP': (-1, 0), 'DOWN': (1, 0), 
                     'LEFT': (0, -1), 'RIGHT': (0, 1)}
        height, width = board.shape
        
        for action, (dy, dx) in directions.items():
            new_y, new_x = pos[0] + dy, pos[1] + dx
            if (0 <= new_y < height and 0 <= new_x < width and board[new_y, new_x] == 0):
                moves.append(action)
        return moves

if __name__ == "__main__":
    # Tournament
    print("\n=== MCTS (500 sims) vs GREEDY (5 games) ===\n")
    mcts = MCTSAgent(simulations=500)
    greedy = GreedyAgent()
    results = {'mcts': 0, 'greedy': 0, 'draw': 0}

    for game_num in range(5):
        game = TronGame(width=10, height=10)
        state = game.reset()
        moves = 0
        
        while not game.game_over and moves < 100:
            a1 = mcts.get_action(state, 1)
            a2 = greedy.get_action(state, 2)
            state, reward, done = game.step(a1, a2)
            moves += 1
        
        winner_name = "MCTS" if game.winner == 1 else ("Greedy" if game.winner == 2 else "Draw")
        if game.winner == 1:
            results['mcts'] += 1
        elif game.winner == 2:
            results['greedy'] += 1
        else:
            results['draw'] += 1
        
        print(f"Game {game_num + 1}: Winner = {winner_name}, Moves = {moves}")

    print(f"\nResults: MCTS={results['mcts']}, Greedy={results['greedy']}, Draws={results['draw']}")

    # Optional: Visualize MCTS's probabilistic decision-making
    print("\n" + "="*60)
    print("Watch MCTS vs Greedy - see the exploration!")
    print("="*60)

    game_viz = TronGame(width=10, height=10, visualize=True, cell_size=50)
    state = game_viz.reset()
    move_count = 0

    while not game_viz.game_over and move_count < 100:
        a1 = mcts.get_action(state, 1)
        a2 = greedy.get_action(state, 2)
        state, reward, done = game_viz.step(a1, a2)
        move_count += 1

    winner = "MCTS" if game_viz.winner == 1 else ("Greedy" if game_viz.winner == 2 else "Draw")
    print(f"Visualized game: {winner} wins!")
    game_viz.close()