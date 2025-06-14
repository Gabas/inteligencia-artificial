#!/usr/bin/env python3
"""
TSP utility functions (simplified version without pandas)
"""
import math
import csv

def load_cities(filename):
    """Load cities from CSV file without using pandas"""
    cities = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city_id = int(row['Cidade'])
            x = float(row['X'])
            y = float(row['Y'])
            cities.append((city_id, x, y))
    return cities

def calculate_distance(city1, city2):
    """Calculate Euclidean distance between two cities"""
    _, x1, y1 = city1
    _, x2, y2 = city2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def total_distance(route, cities):
    """Calculate total distance of a route"""
    distance = 0
    for i in range(len(route) - 1):
        city1 = cities[route[i] - 1]  # Adjust index if city IDs start from 1
        city2 = cities[route[i + 1] - 1]
        distance += calculate_distance(city1, city2)
    
    # Add distance from last city back to first city to complete the circuit
    city1 = cities[route[-1] - 1]
    city2 = cities[route[0] - 1]
    distance += calculate_distance(city1, city2)
    
    return distance