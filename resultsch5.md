Question 1: Why is the win rate between two random agents approximately equal, and what does this tell us about the relationship between starting position and strategy in Tron?

        The win rate is equal because the agents are using the same strategy and similar starting position (from opposing corners). When the starting position and strategy are the same the restults are roughly the same.

Question 2: Random agents occasionally win by "accidentally" making good moves. Explain why this approach cannot scale to more complex games and what properties an intelligent agent needs that random selection lacks.

    more complex games require a more complexe series of dicisions in order to gain an advantage. This means that the chance of accidentally executing a optimal series of tasks is increasingly smaller in chance. An intelligent agent should not make random choices and should calculate moves based on its environment and opponents moves.

Question 3: How does the average game length between random agents compare to what you might expect from intelligent play, and what does this reveal about the relationship between lookahead and survival time?

    It is much shorter. These agents dont make any offensive decisions and instead are making mistakes that cost them the game/ end it early. More lookahead should lead to a longer survival time.

Question 3b (Visualization): After watching the visualized game, describe how observing the spatial patterns of random movement helps you understand why random agents crash quickly. What visual patterns emerge that text-based statistics don't capture?

    The agents often run into themselves very quickly. The chance of an agent running into itself in this scenario is high because its movement is random. There is no competition because the agents are only changing direction randomly without context.


Question 4: Explain why the greedy agent's flood-fill heuristic is effective against random play, and what assumption about survival it makes that proves generally correct in Tron.

    The random agent loses very quickly. The greedy agent takes longer by efficiently traveling every tile on its side of the board. While it still gets stuck, about 80-90% of the time it outlasted the random agent. The general assumption is that it survives by taking longer to reach a dead end (turn on itself)

Question 5: Describe a scenario where greedy space-maximization could lead to a losing position, demonstrating the difference between local optimality and global strategy.

    If it gets cut off in its path, it will lose. The few games that the random agent won were because the random agent was able to get in the way of the greedy agent before it got in the way of itself. Global strategy beats local optimality because local optimality relies on the local absense of a opponent.

Question 6: How does the computational cost of flood-fill (which explores many cells) compare to random selection, and why might this cost be acceptable for a real-time game?

    It is slightly higher but acceptable because it conserves space and outlasts random. It doesnt consider opponent movement or cells in front, so its cost is not significantly higher than the random agent.

Question 6b (Visualization): After watching the greedy vs random visualization, describe what strategic patterns you noticed in the greedy agent's movement. How does visualizing the space-control heuristic in action deepen your understanding compared to just reading the code?

    by using the space-control heuristic, the greedy agent is wasting time to let the random agent make a mistake. The random agent usually loses quickly because it is not concerned about space fill or offence/defense but randomly changing directions which overtime increases the likelyhood of a lose.




Question 7: Explain why minimax requires an evaluation function at depth limits rather than computing exact game outcomes, and what trade-off this represents between accuracy and computational feasibility. Based on the results, at what depth does minimax start to significantly outperform greedy (if at all)? What does this suggest about the "lookahead horizon" needed in Tron?

    Minimax requiores much more computation for its lookahead. At depths 2, 3 & 4, minimax losed worse to greedy than random even. It sought out a path without realising the mistake ahead. For a lookahead of 5, minimax quickly realized it needed to conserve time and space and chose to zig-zag to the opponents side before wrapping back and winning. More computation means better performance ater a certain point. Minimax behaves like greedy at depth=0, depth=1 is similar. it isnt until depth=5 that minimax came out on top.

Question 8: Analyze how alpha-beta pruning reduces the search space without affecting the final decision, and describe a scenario where pruning would be most effective (many cutoffs vs few cutoffs).

    An agent that explores every state in a tree is going to take much longer without alpha-beta pruning. Games are often time based, so alpha-beta pruning will have a strong advantage when eliminating lots of less optimal states.

Question 9: Compare minimax's assumption of optimal opponent play to the greedy agent's behavior. When would this assumption hurt minimax's performance, and when would it help?

    Minimax assumes that the opponent will not cover the space in front of it. This hurts minimax espesially with low lookahead because by the time it uncovers a tile blocked by the opponent it has less options for plays than with higher lookahead. The assumtion helps when the opponent makes a mistake or is turning away from minimax. 

Question 9b (Critical Thinking): If minimax with depth-3 only wins 50-60% of games against greedy (rather than 80-90%), what does this suggest about the relationship between lookahead and the quality of the evaluation function? Consider that both algorithms use the same space-difference heuristic at their search horizon.

    Higher lookahead is always better because it allows minimax to spot mistakes earlier and avoid branching down to a state that will cause it to lose. The combination of lookahead with alpha-beta pruning allows this agent to quickly adjust its path to avoid dead ends and decisions that will lead to a definate loss


Question 10: Explain why MCTS can make good decisions without explicitly evaluating position quality, and how the law of large numbers ensures convergence to optimal play.

    The simulations that MCTS stores give it a estimated decision for a given state. The law of large numbers suggests that the more simulations that MCTS runs, the more accuratly it will decide where to go based on the current state.

Question 11: Compare the UCB1 exploration parameter's role in MCTS to the depth parameter in minimax. How do they both address the exploration-exploitation trade-off, and what makes their approaches fundamentally different?

    while the depth parameter in minimax told the agent how far/deep to look, the UCB1 parameter is a heuristic to decide which child node to expand. they both determine the agents next move, but the key difference is that minimax's depth parameter allows it to look ahead of its current state while the UCB1 parameter only selects the next state (arguable lookahead of 1)

Question 12: Describe why MCTS might outperform minimax in games with high branching factors or deep game trees, referencing the computational complexity of each approach.

    High branching factors are more complex for minimax since the amount of computation increases by branching_factor * depth. MCTS has potential to outperform minimax when the UCB1 is optimal. In this case MCTS will choose the same path as minimax without the additional computations for other branches at the depth parameter.

Question 13: Analyze the trade-offs between using an LLM for game-playing versus traditional algorithms. Consider factors like interpretability, computational cost, and performance ceiling.

    Using an LLM for games is much slower and more resource intensive because of the amount of additional calls and compute to the Model and game. Each of the state changes needs to be a call to the LLM which takes a while. While the LLM has a potentially higher performance ceiling, in this case, the performance and time complexity does not produce a better result against greedy.

Question 14: Explain why prompt engineering is crucial for the LLM agent's performance, and describe how changing the prompt structure might improve or degrade decision quality.

    Just like with humans, different stratigies can either result in higher win chances or lower. Prompt engineering can tell the model things to attept or situations to avoid. Giving an offensive strategy to block the opponent will give the model a different outcome compared to a defensive, time conserving strategy.

Question 15: Compare the LLM's "reasoning" (pattern matching from training) to MCTS's statistical reasoning and minimax's logical reasoning. What are the fundamental epistemological differences in how each approach "knows" what move is best?

    MCTS's statistical reasoning decides a move based on how many times that move resulted in a positive outcome during the simulations/training. LLM reasoning decides a path based on training data. MCTS uses a algorithm to find optimal moves while the LLM uses training information to decide the best move. 

Question 16: Analyze the tournament results to identify which algorithmic properties (lookahead depth, simulation count, heuristic quality) most strongly correlate with winning performance in Tron.

    MCTS is on top by far with 500 simulations slightly outperforming 200 simulations. It seams that running game simulations correlate with winning more than any other algorithm. 

Question 17: Explain why certain matchups might produce unexpected results (e.g., a weaker agent occasionally beating a stronger one), and what this reveals about the relationship between algorithm design and opponent behavior.

   Random did win against minimax-7 and barely against minimax-5. It also apears that agents that dont consider oponent behavior are week to the "fortunate" decisions that it makes. Without watching the games random played, a good guess is that random will make a turn that is in the opponents future path but the algorithm doesnt have a solution. 

Question 18: Discuss the time-performance trade-off observed in the results. If this were a real-time game with a 1-second move limit, how would you balance algorithm sophistication against time constraints?

    There seams to be a positive corilation between longer time-performance and win rate. The Agent that came out on top also took the longest. A balanced algorithm might take advantage of this statistic and attempt to git as close to the time constraint without ever exceeding it for a real time game. 

    However, if the agents are able to change their paths realative to the other players movement, in certain games with certain scenarios, it might be better to be as quick as possible. 

Question 19: Does the advanced heuristic improve minimax's performance against greedy? If so, by how much? If not, why might even sophisticated pattern detection fail to help?

    Yes, Advanced minimax did much better that normal minimax against greedy. Advanced won 100% of the time while normal won 0% of the games. 

Question 20: Compare the computational cost of advanced vs standard minimax. Is the articulation-point detection worth the extra computation time given the performance improvement (or lack thereof)?

    The advanced agent is worth the extra computation event though it is 2-3x slower. The extra computation is what gave the agent the max possible increase in performance.

Question 21: The advanced heuristic looks for "cut-off" moves that split opponent's space. In what game situations would this strategic insight matter most, and do these situations occur frequently enough to justify the complexity?

    The cut-off move matters when the opponent is trying to outlast the agent through space conservation in this case. Other situations like defence seem to warrant a move to the opponents side. Because of how tron works, the move of cutting off can happen at different scales meaning the times where it can be used are very likely. the advanced model is justified to take this offensive move resulting in a high win rate against the other agents.

Question 22: Add AdvancedMinimax to the agent tournament and run it again a few times. Create a ranking of all tested algorithms from weakest to strongest, justifying your ranking with specific evidence from tournament results. Then, describe a hypothetical Tron variant (different board size, different rules) where your ranking might change, explaining why.

    1. MCTS-500
    2. MCTS-200
    3. AdvMin-5
    4. Minimax-7
    5. Minimax-5
    6. Random
    7. Advmin-7
    8. Greedy

    larger boards with higher opponent separation will perform worse for random because it has a higher chance of failure. 
    Greedy should do better in this scenario because it will conserve more space and last longer. If the rules change so that running into yourself is allowed, then random will have a much lower chance of failer and a higher chance of winning against other agents.
    Advancedmin also performs worse on larger boards because its lookahead and heuristics are less useful in that scenario.

============================================================
FINAL STANDINGS
============================================================
Agent             Wins Losses  Draws   Win%   Avg Time
------------------------------------------------------------
MCTS-500            15      0      6  71.4%     0.350s
MCTS-200            15      2      4  71.4%     0.260s
AdvMinimax-5        11      7      3  52.4%     0.300s
Random               8     11      2  38.1%     0.141s
Minimax-5            7     14      0  33.3%     0.202s
Minimax-7            7     13      1  33.3%     0.245s
Greedy               6     12      3  28.6%     0.200s
AdvMinimax-7         4     14      3  19.0%     0.703s

Question 23: Compare the "intelligence" exhibited by minimax (logical reasoning), MCTS (statistical sampling), and LLM (pattern matching). Are these fundamentally different types of intelligence, or are they all reducible to the same underlying computational process?

    The problem is the same, but the agents are using different teqniques to solve them. fundamentally, The agents dont always consider all patterns, the LLM "thinks" while MCTS remembers patterns. minimax uses lookahead and dicision making.

Question 24: Imagine you're building a Tron AI for a competition with a strict 100ms time limit per move. Describe your design choices (which algorithm(s), what parameters, any hybrid approaches) and justify each decision with reference to the time-performance trade-offs you observed.

    An expiramental agent might use MCTS with consideration of opponents next move, A heuristic could be added with probability that the opponent moves left, right, up, and down. These probabilities would add time so the simulation count would have to be lower.