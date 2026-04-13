import random
import math
from statistics import mean
import matplotlib.pyplot as plt


'''
Algoritmo evolutivo para optimización de funciones de una variable
'''


def cruza_promedio(poblacion, nueva_poblacion, R):
    for _ in range(int(R)):
        padre1 = random.choice(poblacion)
        padre2 = random.choice(poblacion)
        hijo = ((padre1[0]+padre2[0])/2, (padre1[1]+padre2[1])/2)
        nueva_poblacion.append(hijo)
        

def cruza_uniforme(poblacion, nueva_poblacion, R):
    for _ in range(int(R)):
        padre1 = random.choice(poblacion)
        padre2 = random.choice(poblacion)
        hijo = ()
        for i in range(2):
            r = random.uniform(0, 2)
            hijo[i] = padre1[i] if r == 0 else padre2[i]
        nueva_poblacion.append(hijo)
        
    
def mutacion(poblacion, nueva_poblacion, M, a, b):
    for _ in range(int(M)):
        individuo = random.choice(poblacion)
        x_mutado = individuo[0] + random.gauss(0, individuo[1])
        if x_mutado < a:
            x_mutado = a
        if x_mutado > b:
            x_mutado = b
        des_est = 1.0
        nuevo_individuo = (x_mutado, des_est)
        nueva_poblacion.append(nuevo_individuo)
    

def generar_poblacion(M, a, b):
    ''' Genera M individuos, cada uno es una tupla (x, y, des_est_x, des_est_y) donde x e y son coordenadas y 
    des_est_x y des_est_y son desviaciones estándar para la mutación'''
    
    poblacion = []
    for _ in range(M):
        x = random.uniform(a, b)
        des_est_x = random.uniform(0, 1)
        poblacion.append((x, des_est_x))
    return poblacion


def algoritmo_evolutivo(fitness, i, M, L, r, m, a, b):
    '''
    fitness: función de evaluación
    i : número de generaciones
    M: tamaño de la población
    L: número de nuevos individuos por generación
    r: tasa de cruza
    m: tasa de mutación
    a, b: limites del intervalo de búsqueda
    '''
    print("Iniciando algoritmo evolutivo...")
    poblacion = [] # Lista de tuplas(4) para almacenar la población (x, r)
    valores_fitness = [] # Lista para almacenar los valores de fitness de la población
    nuevos_individuos = [] # Lista para almacenar los nuevos individuos generados por cruza y mutación
    fitness_historial = [] # Lista para almacenar el historial de fitness
    fitness_promedio = [] # Lista para almacenar el historial de fitness promedio 
    
    # Generar población inicial de manera random: números decimales que pertenecen a los reales
    poblacion = generar_poblacion(M, a, b)
    
    # Ciclo de evolución
    for _ in range(i): # Número de generaciones
        # Calcular el fitness de cada individuo 
        valores_fitness = [fitness(individuo) for individuo in poblacion]
        
        # Crear L nuevos individuos
        mutacion(poblacion, nuevos_individuos, int(L*m), a, b) # MUTACIÓN
        n = len(nuevos_individuos)
        cruza_promedio(poblacion, nuevos_individuos, L-n) # CRUZA
        
        # M + L
        poblacion.extend(nuevos_individuos)
        
        # Seleccionar a los mejores M individuos
        poblacion = sorted(poblacion, key=fitness, reverse=True)[:M]
        valores_fitness = [fitness(individuo) for individuo in poblacion] 
        
        print(f"Media del fitness de la generación actual: {sum(valores_fitness)/M} (len={len(valores_fitness)})")
        
        fitness_historial.append(max(valores_fitness)) # Guardar el mejor fitness de la generación actual    
        fitness_promedio.append(mean(valores_fitness)) # Guardar el fitness promedio de la generación actual
        
        nuevos_individuos.clear() # Limpiar la lista de nuevos individuos
        
    
    print(f"Se terminó el algoritmo evolutivo después de {i} generaciones, tamaño de la población final: {len(poblacion)}")
    return fitness_historial, fitness_promedio
    
    

def _main__():
    bestfit, fitness_promedio= algoritmo_evolutivo(lambda individuo: (individuo[0]*math.sin(10*math.pi*individuo[0]))+1.0, i=1000, M=20, L=6, r=0.2, m=0.8, a=-1, b=2)
    plt.plot(fitness_promedio, label='Media del fitness')
    plt.plot(bestfit, label='Mejor fitness')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title('Evolución del algoritmo evolutivo')
    plt.legend()
    plt.show()

_main__();