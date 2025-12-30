import random
from typing import List, Tuple
from .problem import Train

def pmx_crossover(ind1: List[Train], ind2: List[Train]) -> Tuple[List[Train], List[Train]]:
    """
    Partially Mapped Crossover (PMX) for Permutations.
    Preserves exact set of trains (no duplicates).
    """
    size = len(ind1)
    p1, p2 = [0] * size, [0] * size

    # Initialize offspring with placeholders
    for i in range(size):
        p1[i] = ind1[i]
        p2[i] = ind2[i]

    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap if needed
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Map for checking duplicates
    # We use Train ID to identify uniqueness
    
    # 1. Copy the segment
    for i in range(cxpoint1, cxpoint2):
        p1[i] = ind2[i]
        p2[i] = ind1[i]

    # 2. Map the rest
    # Using simple DEAP-like logic structure or implementing explicit mapping
    # To be safe and readable, let's use the explicit mapping algorithm
    
    mapping1 = {ind2[i].id: ind1[i] for i in range(cxpoint1, cxpoint2)}
    mapping2 = {ind1[i].id: ind2[i] for i in range(cxpoint1, cxpoint2)}

    for i in range(size):
        if not (cxpoint1 <= i < cxpoint2):
            # Fill p1
            candidate = ind1[i]
            while candidate.id in mapping1:
                candidate = mapping1[candidate.id]
            p1[i] = candidate

            # Fill p2
            candidate = ind2[i]
            while candidate.id in mapping2:
                candidate = mapping2[candidate.id]
            p2[i] = candidate
            
    # Cast to original type to ensure compatibility with DEAP's fitness tracking.
    return type(ind1)(p1), type(ind2)(p2)

def inversion_mutation(individual: List[Train]) -> Tuple[List[Train]]:
    """
    Inversion Mutation: Reverses a segment of the permutation.
    Better for TSP/Scheduling than swap mutation.
    """
    size = len(individual)
    point1 = random.randint(0, size)
    point2 = random.randint(0, size - 1)
    if point2 >= point1:
        point2 += 1
    else:
        point1, point2 = point2, point1

    individual[point1:point2] = individual[point1:point2][::-1]
    return individual,
