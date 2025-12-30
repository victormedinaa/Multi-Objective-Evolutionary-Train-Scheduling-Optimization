from dataclasses import dataclass
from typing import List, Tuple, Dict
import random
import numpy as np

@dataclass(frozen=True)
class Train:
    """Immutable Train representation."""
    id: int
    wagons: int
    op_type: str

    def __repr__(self):
        return f"Train(id={self.id}, wagons={self.wagons}, op={self.op_type})"

class TrainSchedulingProblem:
    def __init__(self, num_trains: int = 20, min_wagons: int = 10, max_wagons: int = 30):
        self.num_trains = num_trains
        self.min_wagons = min_wagons
        self.max_wagons = max_wagons
        self.dock_types = ["op1", "op2", "op3"]
        self.trains = self._generate_trains()

    def _generate_trains(self) -> List[Train]:
        trains = []
        for i in range(self.num_trains):
            wagons = random.randint(self.min_wagons, self.max_wagons)
            op = random.choice(self.dock_types)
            trains.append(Train(id=i, wagons=wagons, op_type=op))
        return trains

    def evaluate(self, individual: List[Train]) -> Tuple[float, float]:
        """
        Evaluates a schedule (permutation of trains).
        Returns:
            (total_waiting_time, makespan)
            We want to minimize BOTH.
        """
        dock_remaining_time = {op: 0 for op in self.dock_types}
        total_waiting_time = 0
        
        # Simulation: Trains arrive sequentially (FIFO on single track).
        # We model the delay if the required dock is busy.
        
        simulation_clock = 0
        dock_free_at = {op: 0 for op in self.dock_types}
        
        for train in individual:
            needed_dock = train.op_type
            available_at = dock_free_at[needed_dock]
            
            # If the dock is busy, the train must wait.
            if available_at > simulation_clock:
                wait = available_at - simulation_clock
                total_waiting_time += wait
                simulation_clock = available_at 
            
            # Process train
            processing_time = train.wagons
            start_process = simulation_clock
            end_process = start_process + processing_time
            
            dock_free_at[needed_dock] = end_process
            
            # Update legacy counter for consistency if needed, 
            # but simulation_clock + max(dock_remaining) is equivalent to max(dock_free_at) - start
            dock_remaining_time[train.op_type] = processing_time # Not strictly used in this cleaner logic
            
        final_makespan = simulation_clock + max(max(dock_remaining_time.values()) if dock_remaining_time else 0, 0)
        # More accurately, Makespan is the time the LAST dock finishes:
        final_makespan = max(dock_free_at.values())

        return total_waiting_time, float(final_makespan)

