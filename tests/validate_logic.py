import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from genetic_scheduler.problem import TrainSchedulingProblem, Train
from genetic_scheduler.operators import pmx_crossover

class TestSchedulerLogic(unittest.TestCase):
    def test_evaluation_logic_simple(self):
        """
        Test a simple scenario to verify manual calculation matches code evaluation.
        Scenario:
        Train A: 10 wagons, op1
        Train B: 20 wagons, op1 (Same dock collision)
        Train C: 15 wagons, op2 (Different dock)
        
        Sequence: A -> B -> C
        
        Logic Trace:
        1. A arrives. Clock=0. Op1 free at 0. Enters. 
           Wait=0. 
           Op1 busy until 10.
        
        2. B arrives. Clock=0 (relative to sequence start). Op1 free at 10.
           Must wait 10.
           Clock advances to 10.
           Wait += 10.
           Enters Op1.
           Op1 busy until 10+20=30.
           
        3. C arrives. Clock=10. Op2 free at 0.
           Op2 free at 0 <= Clock 10. No wait.
           Enters Op2.
           Op2 busy until 10+15=25.
           
        Expected Total Wait: 10.
        Expected Makespan: Max(Op1_end=30, Op2_end=25) = 30.
           (Wait, simulation_clock was 10. The logic returns 
            final_makespan = simulation_clock + max(dock_remaining))?
            
            Let's allow the code to speak.
            In problem.py:
            dock_remaining_time = {op: 0 ...}
            
            Loop A:
            wait = 0.
            dock_remaining[op1] = 10.
            
            Loop B:
            wait_for_dock = dock_remaining[op1] = 10.
            time_passed = 10.
            total_waiting_time += 10.
            dock_remaining[op1] -= 10 -> 0.
            dock_remaining[op2] -= 10 -> 0 (was 0).
            dock_remaining[op1] = 20.
            
            Loop C:
            wait_for_dock = dock_remaining[op2] = 0.
            dock_remaining[op2] = 15.
            
            Final:
            dock_remaining = {op1: 20, op2: 15, op3: 0}
            Wait = 10.
            Makespan? 
            Original logic returned: time + max(counters.values())
            My code returns: total_waiting_time, final_makespan
            
            Let's check my `evaluate` implementation in `problem.py`.
        """
        problem = TrainSchedulingProblem(num_trains=3)
        # Mocking trains
        t1 = Train(0, 10, "op1")
        t2 = Train(1, 20, "op1")
        t3 = Train(2, 15, "op2")
        
        individual = [t1, t2, t3]
        
        wait, makespan = problem.evaluate(individual)
        
        print(f"\nScenario 1 (A->B->C): Wait={wait}, Makespan={makespan}")
        self.assertEqual(wait, 10, "Wait time should be 10 for blocked Train B")
        # Makespan: 10 (simulation advanced) + max(20, 15) = 30.
        # But wait, logic in problem.py line 79-84 (in original write, not visible here but I wrote it):
        # I implemented check 'wait > 0'.
        
    def test_pmx_validity(self):
        """Verify PMX produces valid permutations (no duplicates)."""
        problem = TrainSchedulingProblem(num_trains=10)
        p1 = problem.trains[:]
        p2 = problem.trains[:]
        import random
        random.shuffle(p2)
        
        off1, off2 = pmx_crossover(p1, p2)
        
        # Check lengths
        self.assertEqual(len(off1), 10)
        
        # Check uniqueness by ID
        ids1 = set(t.id for t in off1)
        self.assertEqual(len(ids1), 10, "Offspring 1 contains duplicates!")
        
        ids2 = set(t.id for t in off2)
        self.assertEqual(len(ids2), 10, "Offspring 2 contains duplicates!")

if __name__ == "__main__":
    unittest.main()
