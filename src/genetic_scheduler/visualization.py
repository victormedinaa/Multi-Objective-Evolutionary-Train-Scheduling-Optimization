import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_pareto_front(pareto_front, filename="pareto_front.png"):
    """Plots the Pareto Front of non-dominated solutions."""
    costs = np.array([ind.fitness.values for ind in pareto_front])
    # costs[:, 0] = Wait Time, costs[:, 1] = Makespan
    
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    plt.scatter(costs[:, 0], costs[:, 1], c='red', marker='o', s=100, label='Pareto Optimal')
    plt.xlabel('Total Waiting Time')
    plt.ylabel('Makespan (Total Completion Time)')
    plt.title('Pareto Front: Wait Time vs Makespan')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_gantt_schedule(individual, dock_types, filename="gantt_chart.png"):
    """
    Simulates the schedule again to get start/end times and plots Gantt.
    """
    # Re-simulate to get timings
    dock_free_at = {op: 0 for op in dock_types}
    simulation_clock = 0
    
    schedule_data = [] # (TrainID, Dock, Start, End)
    
    for train in individual:
        needed_dock = train.op_type
        available_at = dock_free_at[needed_dock]
        
        if available_at > simulation_clock:
            simulation_clock = available_at
        
        start_process = simulation_clock
        end_process = start_process + train.wagons
        dock_free_at[needed_dock] = end_process
        
        schedule_data.append((train.id, needed_dock, start_process, end_process))
    
    # Plotting
    plt.figure(figsize=(12, 6))
    colors = sns.color_palette("hls", n_colors=len(dock_types))
    dock_colors = dict(zip(dock_types, colors))
    
    yticks = []
    yticklabels = []
    
    # Map docks to Y-axis positions
    dock_y_map = {op: i for i, op in enumerate(dock_types)}
    
    for tid, dock, start, end in schedule_data:
        duration = end - start
        y = dock_y_map[dock]
        plt.barh(y, duration, left=start, height=0.5, color=dock_colors[dock], edgecolor='black')
        plt.text(start + duration/2, y, f"T{tid}", ha='center', va='center', color='white', fontweight='bold')
        
    plt.yticks(list(dock_y_map.values()), list(dock_y_map.keys()))
    plt.xlabel("Time")
    plt.title("Optimized Train Schedule (Gantt Chart)")
    plt.grid(True, axis='x')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
