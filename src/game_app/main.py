from map_generation.even_distribution_map_generator import EvenDistributionMapGenerator

map = EvenDistributionMapGenerator(10, 5, ["Rupert", "Sophie"]).create_map()

print(map.planets)
for planet in map.planets:
    print(planet.position.x, planet.position.y)