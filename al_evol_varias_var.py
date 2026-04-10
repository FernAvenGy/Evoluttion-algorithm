import random
import math
import matplotlib.pyplot as plt
from numpy import mean

'''
Algoritmo evolutivo para optimización de funciones de varias variables
'''


def cruza_promedio(poblacion, nueva_poblacion, R):
    for _ in range(int(R)):
        padre1 = random.choice(poblacion)
        padre2 = random.choice(poblacion)
        hijo = ((padre1[0]+padre2[0])/2, (padre1[1]+padre2[1])/2, (padre1[2]+padre2[2])/2, (padre1[3]+padre2[3])/2)
        nueva_poblacion.append(hijo)
        

def cruza_uniforme(poblacion, nueva_poblacion, R):
    for _ in range(int(R)):
        padre1 = random.choice(poblacion)
        padre2 = random.choice(poblacion)
        hijo = ()
        for i in range(4):
            r = random.uniform(0, 2)
            hijo[i] = padre1[i] if r == 0 else padre2[i]
        nueva_poblacion.append(hijo)
        
    
def mutacion(poblacion, nueva_poblacion, M):
    for _ in range(int(M)):
        individuo = random.choice(poblacion)
        x_mutado = individuo[0] + random.gauss(0, individuo[2])
        y_mutado = individuo[1] + random.gauss(0, individuo[3])
        des_est_x_mutada = 1.0
        des_est_y_mutada = 1.0
        nuevo_individuo = (x_mutado, y_mutado, des_est_x_mutada, des_est_y_mutada)
        nueva_poblacion.append(nuevo_individuo)
    

def generar_poblacion(M, ax, bx, ay, by):
    ''' Genera M individuos, cada uno es una tupla (x, y, des_est_x, des_est_y) donde x e y son coordenadas y 
    des_est_x y des_est_y son desviaciones estándar para la mutación'''
    
    poblacion = []
    for _ in range(M):
        x = random.uniform(ax, bx)
        y = random.uniform(ay, by)
        des_est_x = random.uniform(0, 1)
        des_est_y = random.uniform(0, 1)
        poblacion.append((x, y, des_est_x, des_est_y))
    return poblacion


def algoritmo_evolutivo(fitness, i, M, L, r, m, ax, bx, ay, by):
    '''
    fitness: función de evaluación
    i: número de generaciones
    M: tamaño de la población
    L: número de nuevos individuos por generación
    r: tasa de cruza
    m: tasa de mutación
    ax, bx: límites del intervalo de búsqueda para la variable x
    ay, by: límites del intervalo de búsqueda para la variable y
    b: final de intervalo de búsqueda
    '''
    print("Iniciando algoritmo evolutivo...")
    poblacion = [] # Lista de tuplas(4) para almacenar la población (x, r)
    valores_fitness = [] # Lista para almacenar los valores de fitness de la población
    nuevos_individuos = [] # Lista para almacenar los nuevos individuos generados por cruza y mutación
    fitness_historial = [] # Lista para almacenar el historial de fitness a lo largo de las generaciones
    fitness_promedio = [] # Lista para almacenar el fitness promedio de cada generación
    
    # Generar población inicial de manera random: números decimales que pertenecen a los reales
    poblacion = generar_poblacion(M, ax, bx, ay, by)
    
    # Ciclo de evolución
    for _ in range(i):
        # Calcular el fitness de cada individuo 
        valores_fitness = [fitness(individuo) for individuo in poblacion]
        
        # Crear L nuevos individuos 
        mutacion(poblacion, nuevos_individuos, int(L*m)) # MUTACIÓN
        n = len(nuevos_individuos)
        cruza_promedio(poblacion, nuevos_individuos, L-n) # CRUZA (los que faltan)
        
        # M + L 
        poblacion.extend(nuevos_individuos)
        
        # Seleccionar a los mejores M individuos
        poblacion = sorted(poblacion, key=fitness, reverse=True)[:M]
        
        fitness_historial.append(max(valores_fitness)) # Guardar el mejor fitness de la generación actual    
        fitness_promedio.append(mean(valores_fitness)) # Guardar el fitness promedio de la
        
        nuevos_individuos.clear() # Limpiar la lista de nuevos individuos
    
    return fitness_historial, fitness_promedio
    
    

def _main__():
    bestfit, fitness_promedio = algoritmo_evolutivo(lambda individuo: math.sin(individuo[0]) + math.cos(individuo[1]), 100, 10, 5, 0.5, 0.2, -10, 10, -10, 10)
    plt.plot(fitness_promedio, label='Media del fitness')
    plt.plot(bestfit, label='Mejor fitness')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title('Evolución del algoritmo evolutivo')
    plt.legend()
    plt.show()

_main__();