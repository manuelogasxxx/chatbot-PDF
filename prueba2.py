import random

class AlgoritmoGenetico:
    def __init__(self, individuo_base, population_size, generations, 
                 crossover_probability, mutation_probability, elitism, 
                 maximise_fitness=False):
        self.individuo_base = individuo_base
        self.population_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.elitism = elitism
        self.maximise_fitness = maximise_fitness
        
        # Funciones que se asignarán desde fuera
        self.create_individual = None
        self.fitness_function = None
        self.selection_function = None
        self.crossover_function = None
        self.mutate_function = None
        
        # Resultados
        self.best_individual = None
        
    def crear_poblacion_inicial(self):
        poblacion = []
        for _ in range(self.population_size):
            individuo = self.create_individual(self.individuo_base)
            poblacion.append(individuo)
        return poblacion
    
    def calcular_aptitud_poblacion(self, poblacion):
        return [(ind, self.fitness_function(ind, self.individuo_base)) for ind in poblacion]
    
    def seleccionar_padres(self, poblacion_con_aptitud):
        return self.selection_function([ind for ind, apt in poblacion_con_aptitud])
    
    def aplicar_cruce(self, padre1, padre2):
        if random.random() < self.crossover_probability:
            return self.crossover_function(padre1, padre2)
        return padre1, padre2
    
    def aplicar_mutacion(self, individuo):
        if random.random() < self.mutation_probability:
            individuo_mutado = individuo[:]
            self.mutate_function(individuo_mutado)
            return individuo_mutado
        return individuo
    
    def run(self):
        # Crear población inicial
        poblacion = self.crear_poblacion_inicial()
        poblacion_con_aptitud = self.calcular_aptitud_poblacion(poblacion)
        
        # Ordenar población por aptitud
        poblacion_con_aptitud.sort(key=lambda x: x[1], reverse=self.maximise_fitness)
        self.best_individual = poblacion_con_aptitud[0]
        
        for generacion in range(self.generations):
            nueva_poblacion = []
            
            # Elitismo: mantener el mejor individuo
            if self.elitism and self.best_individual:
                nueva_poblacion.append(self.best_individual[0])
            
            # Crear nueva población
            while len(nueva_poblacion) < self.population_size:
                # Seleccionar padres
                padre1 = self.seleccionar_padres(poblacion_con_aptitud)
                padre2 = self.seleccionar_padres(poblacion_con_aptitud)
                
                # Cruzar
                hijo1, hijo2 = self.aplicar_cruce(padre1, padre2)
                
                # Mutar
                hijo1 = self.aplicar_mutacion(hijo1)
                hijo2 = self.aplicar_mutacion(hijo2)
                
                # Agregar a nueva población
                nueva_poblacion.append(hijo1)
                if len(nueva_poblacion) < self.population_size:
                    nueva_poblacion.append(hijo2)
            
            # Actualizar población
            poblacion = nueva_poblacion
            poblacion_con_aptitud = self.calcular_aptitud_poblacion(poblacion)
            
            # Ordenar y actualizar mejor individuo
            poblacion_con_aptitud.sort(key=lambda x: x[1], reverse=self.maximise_fitness)
            mejor_actual = poblacion_con_aptitud[0]
            
            # Actualizar mejor global si corresponde
            if (self.maximise_fitness and mejor_actual[1] > self.best_individual[1]) or \
               (not self.maximise_fitness and mejor_actual[1] < self.best_individual[1]):
                self.best_individual = mejor_actual
            
            # Opcional: mostrar progreso cada ciertas generaciones
            if generacion % 20 == 0:
                print(f"Generación {generacion}: Mejor aptitud = {self.best_individual[1]}")

        return self.best_individual

# -- Clase problemas de Algoritmos Geneticos con caso especial de cruce y mutación
class ProblemaAG:
    # -- Constructor
    def __init__(self, nombre, individuo, nroIndividuos, FnAptitud):
        self.nombre = nombre
        self.individuo = individuo
        self.nroIndividuos = nroIndividuos
        self.FnAptitud = FnAptitud

    # -- Nombre
    def __str__(self):
        return self.nombre

    # -- Crear individuo
    def FnIndividuo(self, individuo):
        individuoNuevo = individuo[:]
        random.shuffle(individuoNuevo)
        return individuoNuevo

    # -- Función de selección
    def FnSeleccion(self, poblacion):
        return random.choice(poblacion)

    # -- Función de cruce
    def FnCruce(self, padre1, padre2):
        # -- Determinar aleatoriamente el índice para el cruce
        indiceCruce = random.randrange(1, len(padre1))
        hijo1 = padre1[:indiceCruce] + [i for i in padre2 if i not in padre1[:indiceCruce]]
        hijo2 = padre2[:indiceCruce] + [i for i in padre1 if i not in padre2[:indiceCruce]]
        return hijo1, hijo2

    # -- Función de mutación
    def FnMutacion(self, individuo):
        # -- Se intercambia los genes de las posiciones dadas por los índices
        indice1 = random.randrange(len(individuo))
        indice2 = random.randrange(len(individuo))
        individuo[indice1], individuo[indice2] = individuo[indice2], individuo[indice1]

    # -- Ejecutar algoritmo genético
    def Ejecutar(self):
        ga = AlgoritmoGenetico(
            self.individuo,  # individuo_base (patrón para crear individuos)
            self.nroIndividuos,  # population_size (número entero)
            generations=100,
            crossover_probability=0.8,
            mutation_probability=0.2,
            elitism=True,
            maximise_fitness=False
        )

        # -- Asignar lógica de crear individuos al algoritmo genético
        ga.create_individual = self.FnIndividuo
        # -- Asignar función de aptitud
        ga.fitness_function = self.FnAptitud
        # -- Asignar función de Selección
        ga.selection_function = self.FnSeleccion
        # -- Asignar función de curce (crossover)
        ga.crossover_function = self.FnCruce
        # -- Asignar función de mutación
        ga.mutate_function = self.FnMutacion

        # -- Ejecutar el algoritmo genético
        return ga.run()

# -- Clase del problema de las 8 reinas
class Problema8Reinas:
    # -- Constructor
    def __init__(self):
        self.nombre = 'Problema de las 8 reinas'
        self.individuo = [0,1,2,3,4,5,6,7]
        self.nroIndividuos = 200

    # -- Texto asociado a la clase
    def __str__(self):
        return self.nombre

    # -- Definir la función de aptitud del algoritmo genético
    def FnAptitud(self, individuo, individuoPatron):
        # -- Inicializar  número de colisiones
        nroAtaques = 0
        # -- Determinar el número de reinas que se atacan entre sí (colisiones)
        for i in range(0,len(individuo)):
            # -- Determinar la fila en la que está la reina
            f = individuo[i]
            # -- Se verificará sólo sobre las diagonales de (i,f); para lo cual
            #    se incrementará siempre i; mientras que f se decrementará e incrementará en 1
            incremento = 1
            for k in range(i+1,len(individuo)):
                # -- Se verifica con la casilla de la diagonal superior y diagonal inferior
                if (individuo[k] == f-incremento) or (individuo[k] == f+incremento):
                    nroAtaques += 1
                incremento += 1
        return nroAtaques

    # -- Mostrar mejor solución
    def MostrarSolucion(self, solucion):
        # -- Imprimir el mejor individuo
        print(f"Aptitud: {solucion[0]}, Individuo: {solucion[1]}")
        # -- Imprimir la parte superior del tablero con códigos ASCII
        print('┌───┬───┬───┬───┬───┬───┬───┬───┐')
        for k in range(0, 8):
            # -- Imprimir cada fila, ubicando la reina en la respectiva columna
            TextoLinea = '│'
            for c in range(0,8):
                TextoLinea += ' '+('R' if solucion[1][c]==k else ' ')+' │'
            print(TextoLinea)
            # -- Imprimir las líneas intermedias o la parte final del tablero
            if k < 7:
                print('├───┼───┼───┼───┼───┼───┼───┼───┤')
            else:
                print('└───┴───┴───┴───┴───┴───┴───┴───┘')

    # -- Ejecutar algoritmo genético
    def Ejecutar(self):
        # -- Crear objeto del problema de las 8 reinas
        p8r = ProblemaAG('Problema de las 8 reinas', self.individuo, self.nroIndividuos, self.FnAptitud)
        # -- Ejecutar problema de algoritmo genético
        mejorIndividuo = p8r.Ejecutar()
        # -- Mostrar el mejor resultado
        if mejorIndividuo[0] == 0:
            print('Se encontró solución ¡¡¡ ÓPTIMA  !!!')
            self.MostrarSolucion(mejorIndividuo)
        else:
            print('No se encontró solución óptima...')
            print('Hay ',mejorIndividuo[0],' colisiones')
            self.MostrarSolucion(mejorIndividuo)

# Ejecutar el problema
p8r = Problema8Reinas()
p8r.Ejecutar()