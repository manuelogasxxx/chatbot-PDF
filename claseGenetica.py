#modificado por: Manuel Fernández Mercado ID:254485
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
    self.n=n
    self.tamano=n*n
    self.suma_objetivo = n*(n*n+1)//2
    self.individuo = list(range(1,self.tamano +1 ))
    self.nroIndividuos = 300

  # -- Texto asociado a la clase
  def __str__(self):
    return self.nombre
  def sumaObjetivo(self):
      return self.n *(self.n * self.n +1)//2
  
  
  # -- Definir la función de aptitud del algoritmo genético
  def FnAptitud(self, individuo, individuoPatron):
    
    n=self.n
    suma_objetivo= self.suma_objetivo
    #lista de sumas
    sumas = []
        # -- Sumar filas
    for i in range(n):
        fila_sum = sum(individuo[i*n:(i+1)*n])
        sumas.append(fila_sum)
    
    # -- Sumar columnas
    for j in range(n):
        columna_sum = sum(individuo[j::n])
        sumas.append(columna_sum)
    
    # -- Sumar diagonal principal
    diag_principal = sum(individuo[i*n + i] for i in range(n))
    sumas.append(diag_principal)
    
    # -- Sumar diagonal secundaria
    diag_secundaria = sum(individuo[i*n + (n-1-i)] for i in range(n))
    sumas.append(diag_secundaria)

    # -- Determinar cuántas sumas son diferentes a la objetivo. Es óptimo cuando todas las sumas son iguales a la objetivo
    return len([s for s in sumas if s != suma_objetivo])
  
  
  # -- Mostrar mejor solución
  def MostrarSolucion(self, solucion):
    valores = list(solucion[1])
    n = self.n
    
    print(f"\nCuadrado mágico {n}x{n} (Suma objetivo: {self.suma_objetivo})")
    print("=" * (n * 4))
    
    for i in range(n):
        for j in range(n):
            print(f"{valores[i*n + j]:3}", end=" ")
        print()

  # -- Ejecutar algoritmo genético
  def Ejecutar(self):
    # -- Crear objeto de problema de alogritmo Genético
    pga = ProblemaAG('Cuadrado Mágico nxn',self.individuo,self.nroIndividuos,self.FnAptitud)
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
#se puede cambiar para que sean más que 3, con 4 o más tarda un poco en dar el resultado
pcm = CuadradoMagico(3)
pcm.Ejecutar()