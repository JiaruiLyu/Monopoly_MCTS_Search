# Monopoly_MCTS_Search

## How to run

Package Requirement
1. Python 3.9 or above
2. Numpy

To run user interactive mode, run the following command

```shell
python3 AI_Monopoly_Games/play_monopoly.py
```

To run experiments, run the following command

```shell
python3 AI_Monopoly_Games/auto_monopoly.py
```

## AI Modes
There are two Baseline AI modes and two MCT modes
To see what they are and to change them, visit ```Game.py``` on the top. Change the following variables

```python
BASE_LINE_AI_MODE = 0 # 0 for random, 1 for greedy (pick best rent/price property)
MCT_AI_MODE = 0 # 0 for random, 1 for uct improved
```