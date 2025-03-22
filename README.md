Here’s a GitHub README for your project:  

---

# Wordle Solver using AI Search Algorithms  

## Overview  
This project implements three search algorithms—**Depth First Search (DFS)**, **Breadth First Search (BFS)**, and **Best First Search (using entropy-based heuristic)**—to solve the Wordle game efficiently. The objective is to identify a hidden target word within a limited number of attempts using feedback from the game.  

## Search Algorithms Implemented  
### 1. Depth First Search (DFS)  
- Explores the word space recursively, reducing the search space with each step.  
- Uses a set to track visited words and a recursive approach to process feedback.  
- No backtracking is required since the search space is progressively narrowed.  

### 2. Breadth First Search (BFS)  
- Explores words level by level using a queue (FIFO).  
- Ensures all words at the current depth are evaluated before moving deeper.  
- More systematic but computationally expensive compared to DFS.  

### 3. Best First Search (Entropy-Based Heuristic)  
- Uses entropy to guide the search towards the most informative guesses.  
- Simulates potential feedback patterns and selects the word with the highest information gain.  
- Achieves the best performance in reducing the number of guesses.  

## Results  
| Algorithm  | Avg. Guesses (10 Targets) | Performance Comparison |
|------------|--------------------------|-------------------------|
| **BFS**   | 121.63 guesses           | Slowest                 |
| **DFS**   | 4.43 guesses             | ~27x faster than BFS    |
| **Best First** | 3.47 guesses          | ~21.62% faster than DFS |

- **Best First Search** outperforms DFS and BFS due to its heuristic-driven approach.  
- **DFS** is significantly more efficient than BFS for this problem.  

## Usage  
1. Clone the repository:  
   ```sh
   git clone https://github.com/yourusername/wordle-search-ai.git
   cd wordle-search-ai
   ```
2. Install dependencies (if any).  
3. Run the solver using the desired search method:  
   ```sh
   python solver.py --method dfs
   python solver.py --method bfs
   python solver.py --method best-first
   ```

## Future Improvements  
- Improve the entropy heuristic for better performance.  
- Experiment with hybrid search strategies.  
- Optimize the implementation for larger word sets.  

## Authors  
- **Amog Rao**  
- **Anshuman Sharma**  

---

Would you like any modifications, such as adding installation requirements or example outputs?
