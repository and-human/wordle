# Wordle Solver using AI Search Algorithms  

## Overview  
This project implements three search algorithms—**Depth First Search (DFS)**, **Breadth First Search (BFS)**, and **Best First Search (using entropy-based heuristic)**—to solve the Wordle game efficiently. The objective is to identify a hidden target word within a limited number of attempts using feedback from the game.  

<img width="973" alt="Screenshot 2025-03-22 at 11 43 41" src="https://github.com/user-attachments/assets/659dfe91-e219-496c-a8c2-6a30b8da2f95" />

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

## Future Improvements  
- Improve the entropy heuristic for better performance.  
- Experiment with hybrid search strategies.  
- Optimize the implementation for larger word sets.  
