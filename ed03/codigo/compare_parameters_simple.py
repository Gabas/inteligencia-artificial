#!/usr/bin/env python3
"""
Script to compare different parameter configurations for genetic algorithm (simplified)
"""
import time
import csv
from tsp_simple import load_cities, total_distance
from genetic_algorithm_simple import GeneticAlgorithm

def run_experiment(cities, configurations, generations=100):
    """Run genetic algorithm with different configurations"""
    results = []
    
    for config in configurations:
        name = config.pop("name")
        print(f"\nRunning experiment: {name}")
        
        # Initialize genetic algorithm with configuration
        ga = GeneticAlgorithm(cities=cities, **config)
        
        # Record start time
        start_time = time.time()
        
        # Run the genetic algorithm
        best_route, best_distance, fitness_history = ga.run(generations)
        
        # Calculate elapsed time
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Store results
        results.append({
            "Configuration": name,
            "Best Distance": best_distance,
            "Elapsed Time (ms)": elapsed_time,
            "Best Route": best_route,
            "Fitness History": fitness_history
        })
        
        print(f"Configuration: {name}")
        print(f"Best distance: {best_distance:.2f}")
        print(f"Time taken: {elapsed_time:.2f} ms")
    
    return results

def main():
    # Load cities
    cities = load_cities('tsp.csv')
    print(f"Comparing GA configurations for {len(cities)} cities...")
    
    # Define configurations to compare
    configurations = [
        {
            "name": "Default",
            "pop_size": 100,
            "elite_size": 20,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "tournament_size": 5,
            "selection_method": "tournament",
            "crossover_method": "pmx"
        },
        {
            "name": "High Mutation",
            "pop_size": 100,
            "elite_size": 20,
            "mutation_rate": 0.3,
            "crossover_rate": 0.8,
            "tournament_size": 5,
            "selection_method": "tournament",
            "crossover_method": "pmx"
        },
        {
            "name": "Large Population",
            "pop_size": 200,
            "elite_size": 30,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "tournament_size": 5,
            "selection_method": "tournament",
            "crossover_method": "pmx"
        },
        {
            "name": "Roulette Selection",
            "pop_size": 100,
            "elite_size": 20,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "tournament_size": 5,
            "selection_method": "roulette",
            "crossover_method": "pmx"
        },
        {
            "name": "Order Crossover",
            "pop_size": 100,
            "elite_size": 20,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "tournament_size": 5,
            "selection_method": "tournament",
            "crossover_method": "order"
        },
        {
            "name": "Cycle Crossover",
            "pop_size": 100,
            "elite_size": 20,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "tournament_size": 5,
            "selection_method": "tournament",
            "crossover_method": "cycle"
        }
    ]
    
    # Run experiments
    results = run_experiment(cities, configurations, generations=100)
    
    # Save results to CSV file
    with open('ga_comparison_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Configuration', 'Best Distance', 'Elapsed Time (ms)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({
                'Configuration': result['Configuration'],
                'Best Distance': f"{result['Best Distance']:.2f}",
                'Elapsed Time (ms)': f"{result['Elapsed Time (ms)']:.2f}"
            })
    
    # Print results summary
    print("\nResults Summary:")
    print("Configuration, Best Distance, Elapsed Time (ms)")
    for result in results:
        print(f"{result['Configuration']}, {result['Best Distance']:.2f}, {result['Elapsed Time (ms)']:.2f}")
    
    # Also save results to text file for easy reading
    with open('ga_comparison_results.txt', 'w') as f:
        f.write("Results Summary:\n")
        f.write("Configuration\tBest Distance\tElapsed Time (ms)\n")
        for result in results:
            f.write(f"{result['Configuration']}\t{result['Best Distance']:.2f}\t{result['Elapsed Time (ms)']:.2f}\n")

if __name__ == "__main__":
    main()