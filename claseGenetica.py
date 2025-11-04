import random
from pyeasyga import pyeasyga


#clase base
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
    # print(hijo1,hijo2)
    return hijo1, hijo2

  # -- Función de mutación
  def FnMutacion(self, individuo):
    # -- Se intercambia los genes de las posiciones dadas por los índices
    indice1 = random.randrange(len(individuo))
    indice2 = random.randrange(len(individuo))
    individuo[indice1], individuo[indice2] = individuo[indice2], individuo[indice1]

  # -- Ejecutar algoritmo genético
  def Ejecutar(self):
    ga = pyeasyga.GeneticAlgorithm( self.individuo,
                                    population_size=self.nroIndividuos,
                                    generations=100,
                                    crossover_probability=0.8,
                                    mutation_probability=0.2,
                                    elitism=True,
                                    maximise_fitness=False)

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
    ga.run()

    # -- Devolver resultado
    return ga.best_individual()



# -- Clase de cuadrado mágico
class CuadradoMagico:
  # -- Constructor
  def __init__(self,n):
    self.nombre = 'Cuadrado mágico 3x3'
    self.tamano=n*n
    self.individuo = list(range(1,self.tamano +1 ))
    self.nroIndividuos = 300

  # -- Texto asociado a la clase
  def __str__(self):
    return self.nombre
  def sumaObjetivo(self):
      return self.n *(self.n * self.n +1)//2
  
  
  # -- Definir la función de aptitud del algoritmo genético
  def FnAptitud(self, individuo, individuoPatron):
    # -- Inicializar lista de sumas
    sumas = [0 for i in range(0, 8)]
     # -- Filas
    sumas[0] = individuo[0] + individuo[1] + individuo[2] # -- Fila 1
    sumas[1] = individuo[3] + individuo[4] + individuo[5] # -- Fila 2
    sumas[2] = individuo[6] + individuo[7] + individuo[8] # -- Fila 3

    # -- Columnas
    sumas[3] = individuo[0] + individuo[3] + individuo[6] # -- Columna 1
    sumas[4] = individuo[1] + individuo[4] + individuo[7] # -- Columna 2
    sumas[5] = individuo[2] + individuo[5] + individuo[8] # -- Columna 3

    # -- Diagonales
    sumas[6] = individuo[0] + individuo[4] + individuo[8] # -- Diagonal 1
    sumas[7] = individuo[2] + individuo[4] + individuo[6] # -- Diagonal 2

    # -- Determinar cuántas sumas son diferentes de 15. Es óptimo cuando todas las sumas son 15
    return len([s for s in sumas if s != 15])
  # -- Mostrar mejor solución
  def MostrarSolucion(self, solucion):
    valores = list(solucion[1])
    for i in range(0, len(valores)):
      if (i % 3 == 0):
        print('\n')
      print(valores[i], ' ', end="")

  # -- Ejecutar algoritmo genético
  def Ejecutar(self):
    # -- Crear objeto de problema de alogritmo Genético
    pga = ProblemaAG('Cuadrado Mágico 3x3',self.individuo,self.nroIndividuos,self.FnAptitud)
    # -- Ejecutar problema de algoritmo genético
    mejorIndividuo = pga.Ejecutar()
    # -- Mostrar el mejor resultado
    if mejorIndividuo[0] == 0:
      print('Se encontró solución ¡¡¡ ÓPTIMA  !!!')
      self.MostrarSolucion(mejorIndividuo)
    else:
      print('No se encontró solución...')
      print('Hay ',mejorIndividuo[0],' filas/columnas/diagonales no óptimas')
      self.MostrarSolucion(mejorIndividuo)
      

#ejecución principal
pcm = CuadradoMagico()
pcm.Ejecutar()