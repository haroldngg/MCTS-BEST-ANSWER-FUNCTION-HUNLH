# Poker Simulation with MCTS

## Project Overview
This Python-based project simulates poker games using Monte Carlo Tree Search (MCTS) for strategic decision-making. The simulation covers various poker game scenarios, incorporating detailed poker mechanics, AI-driven decision processes, and extensive game tree exploration. The goal is to analyze and understand the effectiveness of different poker strategies in a controlled, simulated environment.

## Key Features
- **Card Handling:** Implements classes and methods for efficient management and shuffling of poker cards, mimicking real-world randomness and game conditions.
- **AI Decision Making:** Utilizes advanced predictive models for making informed AI decisions at each node within the game tree, based on current and possible future game states.
- **Game Tree Exploration:** Employs MCTS algorithms to systematically explore potential game outcomes and strategically optimize decision-making processes.
- **Visualization:** Offers tools for visualizing game states and decision trees, facilitating a better understanding of game dynamics through graphical representations using `matplotlib` and `networkx`.

## Getting Started

### Prerequisites
Ensure you have Python 3.6 or later installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

### Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/tchimby/MCTS-BEST-ANSWER-FUNCTION-HUNLH.git


## Example Game Simulation

Below is an example game session played by the poker simulation. This detailed breakdown showcases player interactions, AI decisions, and game outcomes during a typical round of poker.

### Game Setup
- **Player's Hand:** `[ Q ♠ ]`, `[ 3 ♦ ]`
- **Opponent's Hand:** `[ J ♠ ]`, `[ 4 ❤ ]`

### Preflop
- **Preflop Move:** Both players check.
- **Player Action:** Checked.
- **Opponent Action:** Checked.
- **Pot Size:** 0

### Flop
- **Flop Cards:** `[ T ♠ ]`, `[ 9 ♣ ]`, `[ 8 ❤ ]`
- **Postflop Move:** Player checks; opponent folds.
- **Player Action:** Checked.
- **Opponent Action:** Folded.
- **Outcome:** Player wins the pot.
- **Pot Size at Win:** 10

### Commentary
- **Preflop:** Both players decided to check, indicating a cautious approach possibly due to the moderate strength of their hands.
- **Flop:** The community cards `[ T ♠ ]`, `[ 9 ♣ ]`, `[ 8 ❤ ]` opened up potential straight draws, but with no immediate high hand and a non-aggressive preflop round, the player opted to check. The opponent, possibly not seeing a viable continuation or being out of position, chose to fold.
- **Result:** With the opponent's fold, the player secured a small pot of 10 units without further contest.

This example illustrates the simulation's capability to handle typical poker decision-making processes and adapt strategies based on the evolving game state.


