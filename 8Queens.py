
import random

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
        nuevo = individuo[:]
        random.shuffle(nuevo)
        return nuevo

    # -- Función de selección (torneo simple)
    def FnSeleccion(self, poblacion, fitness):
        i1, i2 = random.sample(range(len(poblacion)), 2)
        return poblacion[i1] if fitness[i1] < fitness[i2] else poblacion[i2]

    # -- Función de cruce (tipo OX)
    def FnCruce(self, padre1, padre2):
        punto = random.randrange(1, len(padre1))
        hijo1 = padre1[:punto] + [x for x in padre2 if x not in padre1[:punto]]
        hijo2 = padre2[:punto] + [x for x in padre1 if x not in padre2[:punto]]
        return hijo1, hijo2

    # -- Función de mutación (intercambio)
    def FnMutacion(self, individuo):
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]

    # -- Ejecutar algoritmo genético
    def Ejecutar(self, generaciones=100, p_cruce=0.8, p_mutacion=0.2, elitismo=True):
        #  Crear población inicial
        poblacion = [self.FnIndividuo(self.individuo) for _ in range(self.nroIndividuos)]

        for gen in range(generaciones):
            # Evaluar fitness
            fitness = [self.FnAptitud(ind) for ind in poblacion]

            # Guardar mejor individuo
            mejor_ind = min(zip(fitness, poblacion), key=lambda x: x[0])
            nuevo_poblacion = [mejor_ind[1]] if elitismo else []

            #  Reproducción
            while len(nuevo_poblacion) < self.nroIndividuos:
                padre1 = self.FnSeleccion(poblacion, fitness)
                padre2 = self.FnSeleccion(poblacion, fitness)

                if random.random() < p_cruce:
                    hijo1, hijo2 = self.FnCruce(padre1, padre2)
                else:
                    hijo1, hijo2 = padre1[:], padre2[:]

                # Mutación
                if random.random() < p_mutacion:
                    self.FnMutacion(hijo1)
                if random.random() < p_mutacion:
                    self.FnMutacion(hijo2)

                nuevo_poblacion.extend([hijo1, hijo2])

            #  Reemplazar población
            poblacion = nuevo_poblacion[:self.nroIndividuos]

        #  Evaluar última generación y devolver el mejor
        fitness = [self.FnAptitud(ind) for ind in poblacion]
        mejor_fitness, mejor_individuo = min(zip(fitness, poblacion), key=lambda x: x[0])

        return mejor_fitness, mejor_individuo

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
  def FnAptitud(self, individuo):
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
    print(solucion)
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
    p8r = ProblemaAG('Problema de las 8 reinas',self.individuo,self.nroIndividuos,self.FnAptitud)
    # -- Ejecutar problema de algoritmo genético
    mejorIndividuo = p8r.Ejecutar()
    # -- Mostrar el mejor resultado
    if mejorIndividuo[0] == 0:
      print('Se encontró solución ¡¡¡ ÓPTIMA  !!!')
      self.MostrarSolucion(mejorIndividuo)
    else:
      print('No se encontró solución...')
      print('Hay ',mejorIndividuo[0],' colisiones')
      self.MostrarSolucion(mejorIndividuo)
      


p8r = Problema8Reinas()
p8r.Ejecutar()