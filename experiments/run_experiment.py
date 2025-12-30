import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from genetic_scheduler.problem import TrainSchedulingProblem
from genetic_scheduler.algorithm import GeneticSolver
from genetic_scheduler.visualization import plot_pareto_front, plot_gantt_schedule
import matplotlib.pyplot as plt

def main():
    print("Initializing Doctoral-Level Genetic Algorithm Experiment...")
    
    # Challenge: 50 trains, tightly constrained
    problem = TrainSchedulingProblem(num_trains=20, min_wagons=10, max_wagons=50)
    
    solver = GeneticSolver(problem, population_size=50, generations=50)
    
    print("Running NSGA-II Optimization...")
    pop, log, pareto = solver.run()
    
    print(f"Optimization Complete. Pareto Front Size: {len(pareto)}")
    
    # Save results
    output_dir = os.path.dirname(__file__)
    plot_pareto_front(pareto, filename=os.path.join(output_dir, "pareto_front.png"))
    
    # Pick a balanced solution
    best_ind = pareto[0] # Just pick one
    plot_gantt_schedule(best_ind, problem.dock_types, filename=os.path.join(output_dir, "best_schedule_gantt.png"))
    
    print("Results saved to experiments/")
    print("Best Individual Stats:", best_ind.fitness.values)

if __name__ == "__main__":
    main()
