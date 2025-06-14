#!/usr/bin/env python3
"""
Brute force solution for TSP (simplified version)
"""
import time
import itertools
from tsp_simple import load_cities, total_distance

def brute_force_tsp(cities):
    """Solve TSP using brute force approach"""
    # Get city IDs
    city_ids = [city[0] for city in cities]
    
    # Generate all possible permutations (routes)
    all_routes = list(itertools.permutations(city_ids))
    
    # Find the route with minimum distance
    min_distance = float('inf')
    best_route = None
    
    for route in all_routes:
        dist = total_distance(route, cities)
        if dist < min_distance:
            min_distance = dist
            best_route = route
    
    return best_route, min_distance

def main():
    # Load cities
    cities = load_cities('tsp.csv')
    
    # Only use brute force for small instances (limit to 8 cities)
    # if len(cities) > 8:
    #     print(f"Warning: Brute force is not feasible for {len(cities)} cities.")
    #     print("Consider using a smaller subset of cities.")
    #     num_cities = int(input("Enter number of cities to use (1-8): "))
    #     cities = cities[:num_cities]
    
    print(f"Solving TSP with brute force for {len(cities)} cities...")
    
    # Record start time
    start_time = time.time()
    
    # Run brute force algorithm
    best_route, best_distance = brute_force_tsp(cities)
    
    # Calculate elapsed time
    elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print results
    print(f"\nBest route found: {best_route}")
    print(f"Total distance: {best_distance:.2f}")
    print(f"Time taken: {elapsed_time:.2f} ms")
    
    # Save results to file
    with open('brute_force_results.txt', 'w') as f:
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