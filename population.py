from genome import Genome
import random

'''
Create population of genomes

create list of 40 genomes of which 4 best are going to be elite group and 18 are gonna be recombining
'''

class Population:
    def __init__(self, index: int, number_of_genomes: int, number_of_elite: int, list_to_try) -> None:
        self.index = index
        self.number_of_genomes = number_of_genomes
        self.number_of_elite = number_of_elite
        self.number_of_parents = (self.number_of_genomes - self.number_of_elite)//2
        self.list_of_population: list[Genome] = []
        self.list_to_try: list = list_to_try
        self.population_ranking: dict = {}
        self.best_possible_sum = sum(self.list_to_try)//2
        self.list_of_elites: list[Genome]
        self.best_fitness: float
        self.best_of_all: Genome
        self.max_fitness: float
        self.best_of_population: list[Genome]

        if sum(self.list_to_try)%2 == 1:
            self.max_fitness = 1 - abs(self.best_possible_sum-sum(self.list_to_try)/2)/self.best_possible_sum
        else:
            self.max_fitness = 1
        pass

    def create_population(self):
        for i in range(self.number_of_genomes):
            self.list_of_population.append(Genome(index= i, numbers= self.list_to_try))
            self.list_of_population[i].gene_init()
            self.list_of_population[i].mutate()
            self.list_of_population[i].fitness_count()


    def apply_fitness(self):
        for i in range(len(self.list_of_population)):
            self.population_ranking[self.list_of_population[i]] = self.list_of_population[i].genome_fitness
        
        
        
    def ranking_sort(self):
        sorted_ranking = sorted(self.population_ranking.items(), key=lambda x:x[1], reverse=True)
        sorted_ranking = sorted_ranking[:self.number_of_parents]
        self.population_ranking = dict(sorted_ranking)
        self.best_of_population = list(self.population_ranking.keys())[:self.number_of_parents]
        self.list_of_elites = list(self.population_ranking.keys())[:self.number_of_elite]
        self.best_fitness = sorted_ranking[0][1]
        self.best_of_all = sorted_ranking[0][0]

    def create_new_population(self, last_population_results: list[Genome], list_of_elites: list[Genome]):
        self.list_of_population.extend(list_of_elites)
        for i in range(0, int(self.number_of_parents/2), 2):
            parent1_genes = last_population_results[i].genes
            parent2_genes = last_population_results[i+1].genes
            for _ in range(1):
                crossover_point = random.randint(0,len(parent1_genes)-1)
                #crossover_point = int(len(parent1_genes)//2)
                self.list_of_population.append(Genome(
                    index=len(self.list_of_population),
                    numbers=self.list_to_try,
                    genes=[*parent1_genes[:crossover_point],*parent2_genes[crossover_point:]]
                ))
                self.list_of_population.append(Genome(
                    index=len(self.list_of_population),
                    numbers=self.list_to_try,
                    genes=[*parent2_genes[:crossover_point],*parent1_genes[crossover_point:]]
                ))
                self.list_of_population[-1].mutate()
                self.list_of_population[-2].mutate()
                self.list_of_population[-1].fitness_count()
                self.list_of_population[-2].fitness_count()
                

