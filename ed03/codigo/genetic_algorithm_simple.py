#!/usr/bin/env python3
"""
Genetic Algorithm implementation for TSP (simplified version)
"""
import random
from tsp_simple import total_distance

class GeneticAlgorithm:
    def __init__(self, cities, pop_size=100, elite_size=20, mutation_rate=0.1, 
                 crossover_rate=0.8, tournament_size=5, selection_method='tournament',
                 crossover_method='pmx'):
        self.cities = cities
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.city_ids = [city[0] for city in cities]
        
    def create_initial_population(self):
        """Create initial population of random routes"""
        population = []
        for _ in range(self.pop_size):
            route = self.city_ids.copy()
            random.shuffle(route)
            population.append(route)
        return population
    
    def calculate_fitness(self, route):
        """Calculate fitness of a route (inverse of distance)"""
        dist = total_distance(route, self.cities)
        return 1 / dist if dist > 0 else float('inf')
    
    def evaluate_population(self, population):
        """Evaluate all routes in the population"""
        fitness_results = {}
        for i, route in enumerate(population):
            fitness_results[i] = self.calculate_fitness(route)
        return {k: v for k, v in sorted(fitness_results.items(), key=lambda item: item[1], reverse=True)}
    
    def select_parents(self, fitness_results):
        """Select parents for crossover"""
        selection_results = []
        
        if self.selection_method == 'tournament':
            # Tournament selection
            for _ in range(len(fitness_results)):
                tournament = random.sample(list(fitness_results.keys()), self.tournament_size)
                best_in_tournament = min(tournament, key=lambda x: -fitness_results[x])
                selection_results.append(best_in_tournament)
        else:
            # Roulette wheel selection
            fitness_sum = sum(fitness_results.values())
            probabilities = [fitness / fitness_sum for fitness in fitness_results.values()]
            indices = list(fitness_results.keys())
            
            # Simple roulette wheel implementation
            for _ in range(len(fitness_results)):
                pick = random.random() * fitness_sum
                current = 0
                for i, key in enumerate(fitness_results.keys()):
                    current += fitness_results[key]
                    if current > pick:
                        selection_results.append(key)
                        break
            
        return selection_results
    
    def create_mating_pool(self, population, selection_results):
        """Create mating pool from selected parents"""
        mating_pool = [population[i] for i in selection_results]
        return mating_pool
    
    def pmx_crossover(self, parent1, parent2):
        """Partially Mapped Crossover (PMX)"""
        size = len(parent1)
        
        # Choose crossover points
        start, end = sorted(random.sample(range(size), 2))
        
        # Create children with parent values
        child1 = [None] * size
        child2 = [None] * size
        
        # Copy segment from parents
        child1[start:end+1] = parent1[start:end+1]
        child2[start:end+1] = parent2[start:end+1]
        
        # Map remaining positions
        for i in range(start, end+1):
            if parent2[i] not in child1:
                pos = parent2.index(parent1[i])
                while start <= pos <= end:
                    pos = parent2.index(parent1[pos])
                child1[pos] = parent2[i]
                
            if parent1[i] not in child2:
                pos = parent1.index(parent2[i])
                while start <= pos <= end:
                    pos = parent1.index(parent2[pos])
                child2[pos] = parent1[i]
        
        # Fill remaining positions
        for i in range(size):
            if child1[i] is None:
                child1[i] = parent2[i]
            if child2[i] is None:
                child2[i] = parent1[i]
                
        return child1, child2
    
    def order_crossover(self, parent1, parent2):
        """Order Crossover (OX)"""
        size = len(parent1)
        
        # Choose crossover points
        start, end = sorted(random.sample(range(size), 2))
        
        # Create children
        child1 = [None] * size
        child2 = [None] * size
        
        # Copy segment from parents
        child1[start:end+1] = parent1[start:end+1]
        child2[start:end+1] = parent2[start:end+1]
        
        # Fill remaining positions in order from other parent
        for parent, child in [(parent2, child1), (parent1, child2)]:
            # Get positions to fill
            positions_to_fill = [i for i in range(size) if child[i] is None]
            
            # Get values to insert
            values_to_insert = [x for x in parent if x not in child]
            
            # Fill positions
            for pos, val in zip(positions_to_fill, values_to_insert):
                child[pos] = val
        
        return child1, child2
    
    def cycle_crossover(self, parent1, parent2):
        """Cycle Crossover (CX)"""
        size = len(parent1)
        child1 = [None] * size
        child2 = [None] * size
        
        # Find cycles
        i = 0
        while None in child1:
            if child1[i] is None:
                # Start a new cycle
                curr_cycle = []
                start_val = parent1[i]
                val = start_val
                
                while True:
                    j = parent1.index(val)
                    curr_cycle.append(j)
                    child1[j] = parent1[j]
                    child2[j] = parent2[j]
                    val = parent2[j]
                    if val == start_val:
                        break
            
            # Find next unfilled position
            if None in child1:
                i = child1.index(None)
            
        # Swap for remaining positions
        for i in range(size):
            if child1[i] is None:
                child1[i], child2[i] = parent2[i], parent1[i]
        
        return child1, child2
    
    def crossover(self, parent1, parent2):
        """Perform crossover based on selected method"""
        if random.random() > self.crossover_rate:
            # Skip crossover
            return parent1.copy(), parent2.copy()
            
        if self.crossover_method == 'pmx':
            return self.pmx_crossover(parent1, parent2)
        elif self.crossover_method == 'order':
            return self.order_crossover(parent1, parent2)
        elif self.crossover_method == 'cycle':
            return self.cycle_crossover(parent1, parent2)
        else:
            # Default to PMX
            return self.pmx_crossover(parent1, parent2)
    
    def breed_population(self, mating_pool):
        """Breed a new population through crossover"""
        children = []
        
        # Add elite routes directly
        for i in range(self.elite_size):
            children.append(mating_pool[i])
        
        # Perform crossover for rest of population
        for i in range(self.pop_size - self.elite_size):
            parent1, parent2 = random.sample(mating_pool, 2)
            child1, _ = self.crossover(parent1, parent2)
            children.append(child1)
            
        return children
    
    def mutate(self, route):
        """Perform mutation (swap mutation)"""
        for i in range(len(route)):
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(route) - 1)
                route[i], route[j] = route[j], route[i]
        return route
    
    def mutate_population(self, population):
        """Apply mutation to entire population"""
        mutated_pop = []
        
        # Preserve elite without mutation
        for i in range(self.elite_size):
            mutated_pop.append(population[i])
        
        # Mutate the rest
        for i in range(self.elite_size, len(population)):
            mutated_route = self.mutate(population[i].copy())
            mutated_pop.append(mutated_route)
            
        return mutated_pop
    
    def next_generation(self, current_pop):
        """Create the next generation"""
        # Evaluate population fitness
        fitness_results = self.evaluate_population(current_pop)
        
        # Get sorted routes
        sorted_pop = [current_pop[i] for i in fitness_results.keys()]
        
        # Select parents
        selection_results = self.select_parents(fitness_results)
        
        # Create mating pool
        mating_pool = self.create_mating_pool(current_pop, selection_results)
        
        # Breed population
        children = self.breed_population(mating_pool)
        
        # Mutate population
        next_gen = self.mutate_population(children)
        
        return next_gen
    
    def run(self, generations):
        """Run the genetic algorithm"""
        # Create initial population
        population = self.create_initial_population()
        
        # Track best route
        best_distance = float('inf')
        best_route = None
        fitness_history = []
        
        # Evolve for specified number of generations
        for gen in range(generations):
            # Create next generation
            population = self.next_generation(population)
            
            # Get best route in current generation
            fitness_results = self.evaluate_population(population)
            best_index = list(fitness_results.keys())[0]
            best_current_route = population[best_index]
            best_current_distance = total_distance(best_current_route, self.cities)
            
            # Track average fitness
            avg_fitness = sum(fitness_results.values()) / len(fitness_results)
            fitness_history.append(avg_fitness)
            
            # Update best overall route
            if best_current_distance < best_distance:
                best_distance = best_current_distance
                best_route = best_current_route
            
            # Print progress
            if gen % 10 == 0 or gen == generations - 1:
                print(f"Generation {gen}: Best distance = {best_current_distance:.2f}")
        
        return best_route, best_distance, fitness_history