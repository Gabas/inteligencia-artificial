#!/usr/bin/env python3
"""
Main script to run genetic algorithm on TSP instances (simplified version without matplotlib)
"""
import time
import argparse
from tsp_simple import load_cities, calculate_distance
from genetic_algorithm_simple import GeneticAlgorithm

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Solve TSP using Genetic Algorithm')
    parser.add_argument('--file', type=str, default='tsp.csv', help='CSV file with city coordinates')
    parser.add_argument('--pop_size', type=int, default=100, help='Population size')
    parser.add_argument('--generations', type=int, default=500, help='Number of generations')
    parser.add_argument('--crossover_rate', type=float, default=0.95, help='Crossover rate')
    parser.add_argument('--mutation_rate', type=float, default=0.01, help='Mutation rate')
    parser.add_argument('--elite_size', type=int, default=50, help='Elite size')
    parser.add_argument('--tournament_size', type=int, default=10, help='Tournament size')
    parser.add_argument('--selection', type=str, default='tournament', 
                        choices=['tournament', 'roulette'], help='Selection method')
    parser.add_argument('--crossover', type=str, default='pmx', 
                        choices=['pmx', 'order', 'cycle'], help='Crossover method')
    args = parser.parse_args()
    
    # Load cities from CSV file
    cities = load_cities(args.file)
    print(f"Solving TSP for {len(cities)} cities...")
    
    # Initialize genetic algorithm
    ga = GeneticAlgorithm(
        cities=cities,
        pop_size=args.pop_size,
        elite_size=args.elite_size,
        mutation_rate=args.mutation_rate,
        crossover_rate=args.crossover_rate,
        tournament_size=args.tournament_size,
        selection_method=args.selection,
        crossover_method=args.crossover
    )
    
    # Record start time
    start_time = time.time()
    
    # Run the genetic algorithm
    best_route, best_distance, fitness_history = ga.run(args.generations)
    
    # Calculate elapsed time
    elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print results
    print(f"\nBest route found: {best_route}")
    print(f"Total distance: {best_distance:.2f}")
    print(f"Time taken: {elapsed_time:.2f} ms")
    
    # Save best route to file
    with open('best_route.txt', 'w') as f:
        f.write(f"Best Route: {best_route}\n")
        f.write(f"Total Distance: {best_distance:.2f}\n")
        f.write(f"Time Taken: {elapsed_time:.2f} ms\n")
        
        # Also write city coordinates in order of the route
        f.write("\nCity Coordinates (in route order):\n")
        for city_id in best_route:
            city = cities[city_id - 1]  # Adjust index if city IDs start from 1
            _, x, y = city
            f.write(f"City {city_id}: ({x:.2f}, {y:.2f})\n")

if __name__ == "__main__":
    main()