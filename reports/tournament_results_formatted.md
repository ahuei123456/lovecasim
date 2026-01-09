# Agent Tournament Results\n\n## Tournament Configuration\n- Games per matchup: 10\n- Total matchups: 15 (6 agents, round-robin)\n- Random seed: 42\n\n## Full Results\n\n```\nAgent initialized on device: cpu
Starting Agent Tournament (Round Robin, 10 games per pair)...
Running 210 games using 4 workers (chunksize=13)...
  Progress: 20/210 games complete
  Progress: 40/210 games complete
  Progress: 60/210 games complete
  Progress: 80/210 games complete
  Progress: 100/210 games complete
  Progress: 120/210 games complete
  Progress: 140/210 games complete
  Progress: 160/210 games complete
  Progress: 180/210 games complete
  Progress: 200/210 games complete
  Progress: 210/210 games complete

Tournament Complete in 10.11s

============================================================
Agent           | ELO    | Wins   | Draws  | Win Rate
------------------------------------------------------------
Smart           | 1142   | 43     | 2      | 71.7%
Ability         | 1070   | 39     | 3      | 65.0%
Random          | 1038   | 31     | 9      | 51.7%
Conservative    | 991    | 26     | 5      | 43.3%
Gamble          | 939    | 22     | 5      | 36.7%
NN              | 931    | 23     | 3      | 38.3%
TrueRandom      | 816    | 7      | 11     | 11.7%
============================================================

MATCHUP WINRATE MATRIX (Row vs Column %)
                | TrueR | Rando | Smart | Abili | Conse | Gambl | NN   
-----------------------------------------------------------------------
TrueRandom      |  ---  | 10.0% |  0.0% |  0.0% |  0.0% | 40.0% | 20.0%
Random          | 80.0% |  ---  | 20.0% | 50.0% | 60.0% | 30.0% | 70.0%
Smart           | 90.0% | 70.0% |  ---  | 40.0% | 90.0% | 60.0% | 80.0%
Ability         | 90.0% | 30.0% | 60.0% |  ---  | 70.0% | 80.0% | 60.0%
Conservative    | 50.0% | 40.0% | 10.0% | 30.0% |  ---  | 80.0% | 50.0%
Gamble          | 50.0% | 30.0% | 40.0% | 20.0% | 20.0% |  ---  | 60.0%
NN              | 60.0% | 20.0% | 20.0% | 40.0% | 50.0% | 40.0% |  --- 
============================================================
\n```\n