# Multi-Objective Evolutionary Train Scheduling Optimization (MO-ETSO)

## Abstract
This project presents a **Multi-Objective Genetic Algorithm (MOGA)** framework for optimizing train scheduling in constrained single-track railway terminals. By leveraging **Non-dominated Sorting Genetic Algorithm II (NSGA-II)**, we simultaneously minimize total waiting time (efficiency) and makespan (throughput), providing a set of Pareto-optimal solutions rather than a single compromise. The system employs permutation-based representations with robust **Partially Mapped Crossover (PMX)** and **Inversion Mutation** operators to ensure feasibility in the combinatorial search space.

---

## 1. Introduction
Railway scheduling is a classic **NP-hard** combinatorial optimization problem. Efficient scheduling maximizes capacity and minimizes delays, critical for logistics operations. This research upgrades a baseline Genetic Algorithm to a state-of-the-art (SOTA) research framework, introducing multi-objective optimization to handle conflicting criteria.

### 1.1 Problem Formulation
Let $T = \{t_1, t_2, ..., t_n\}$ be a set of trains, each characterized by:
- **Wagons ($w_i$)**: Processing time required.
- **Operation Type ($op_i$)**: Specific dock constraint ($op \in \{Op_1, Op_2, Op_3\}$).

**Constraints**:
- **Single-Track Access**: Trains arrive sequentially on a shared track.
- **Dedicated Docks**: $t_i$ can only be processed at a dock of type $op_i$.

**Objectives**:
1. **Minimize Total Waiting Time ($f_1$)**: The sum of delays incurred by all trains effectively waiting for track/dock availability.
   $$ \min f_1 = \sum_{i=1}^{n} \text{Wait}(t_i) $$
2. **Minimize Makespan ($f_2$)**: The total time to complete all operations.
   $$ \min f_2 = C_{\max} = \max_{i} (\text{CompletionTime}(t_i)) $$

---

## 2. Methodology

### 2.1 Evolutionary Framework: NSGA-II
We employ **NSGA-II** (Deb et al., 2002), a standard in multi-objective optimization, to maintain population diversity and converge closer to the true Pareto-optimal front.

- **Representation**: Permutation encoding of Train IDs.
- **Selection**: Binary Tournament Selection with Crowding Distance.
- **Elitism**: Fast Non-dominated Sorting.

### 2.2 Genetic Operators
To preserve the permutation property (validity of the schedule), we utilize:
- **Crossover**: **Partially Mapped Crossover (PMX)**. This operator transmits ordering and value information from parent permutations to offspring, ensuring no duplicates.
- **Mutation**: **Inversion Mutation**. A segment of the permutation is reversed. This is proven to be more effective for adjacency-based problems (like TSP/Scheduling) than simple swap mutation.

---

## 3. Project Structure
map
```
genetic_scheduler/
├── src/
│   ├── genetic_scheduler/
│   │   ├── problem.py       # Domain logic and DES (Discrete Event Simulation) evaluation
│   │   ├── algorithm.py     # NSGA-II Solver implementation
│   │   ├── operators.py     # Custom PMX and Inversion operators
│   │   └── visualization.py # Pareto and Gantt plotting tools
├── experiments/
│   └── run_experiment.py    # Runner script for reproducing results
├── tests/                   # Unit tests
├── setup.py                 # Installation script
└── requirements.txt         # Dependencies
```

---

## 4. Experimental Results

The algorithm generates a set of non-dominated solutions. Visualizations include:
- **Pareto Front**: Illustrates the trade-off between Waiting Time and Makespan.
- **Gantt Charts**: Detailed schedule visualization for selected Pareto-optimal individuals.

### 4.1 Usage

**Installation**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

**Running Experiments**:
```bash
python experiments/run_experiment.py
```

---

## 5. Conclusion
This framework demonstrates that evolutionary computation, specifically NSGA-II with domain-specific operators, significantly outperforms naive heuristics in complex scheduling tasks. The resulting Pareto front empowers decision-makers to choose between high-throughput (low makespan) and high-efficiency (low wait time) schedules based on operational needs.

---
*Developed as part of an Advanced Research Initiative in Evolutionary Computing.*
