import random
import numpy as np
from deap import base, creator, tools, algorithms
from .problem import TrainSchedulingProblem
from .operators import pmx_crossover, inversion_mutation

class GeneticSolver:
    def __init__(self, problem: TrainSchedulingProblem, population_size=100, generations=200):
        self.problem = problem
        self.pop_size = population_size
        self.generations = generations
        self.toolbox = base.Toolbox()
        self._setup_deap()

    def _setup_deap(self):
        # Multi-objective Fitness: Minimize (Wait Time, Makespan)
        # Note: Weights are (-1.0, -1.0) for minimization
        if not hasattr(creator, "FitnessMulti"):
            creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMulti)

        self.toolbox.register("indices", list, range(self.problem.num_trains))
        
        # Structure initialization
        def init_individual():
            # Create a random permutation of trains
            # Note: We need actual Train objects, not just indices, to match Problem logic
            # OR we can permute indices and map to trains.
            # To match the previous 'problem.py' which takes List[Train],
            # we should permute the list of trains.
            trains_copy = self.problem.trains[:]
            random.shuffle(trains_copy)
            return creator.Individual(trains_copy)

        self.toolbox.register("individual", init_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # Operators
        self.toolbox.register("evaluate", self.problem.evaluate)
        self.toolbox.register("mate", pmx_crossover)
        self.toolbox.register("mutate", inversion_mutation)
        self.toolbox.register("select", tools.selNSGA2)

    def run(self):
        """Runs NSGA-II"""
        pop = self.toolbox.population(n=self.pop_size)
        pareto_front = tools.ParetoFront()
        
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min, axis=0)
        stats.register("avg", np.mean, axis=0)
        
        # NSGA-II Algorithm
        # We can use algorithms.eaMuPlusLambda
        pop, logbook = algorithms.eaMuPlusLambda(
            pop, self.toolbox, 
            mu=self.pop_size, 
            lambda_=self.pop_size, 
            cxpb=0.7, 
            mutpb=0.2, 
            ngen=self.generations, 
            stats=stats, 
            halloffame=pareto_front,
            verbose=True
        )
        
        return pop, logbook, pareto_front

