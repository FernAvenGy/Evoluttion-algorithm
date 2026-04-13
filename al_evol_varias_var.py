import random
import math
#from tkinter.ttk import Button
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from numpy import mean


'''
Algoritmo evolutivo para optimización de funciones de varias variables
'''

'''  - - - - - - - - - - - - - - - Diccionario de configuraciones - - - - - - - - - - - - - - - '''
FUNCION = 3  # 1, 2 o 3
K = 8 # para función 3

FUNCIONES = {
    1: {
        'ax': -3.0, 'bx': 12.1,
        'ay': 4.1,  'by': 5.8,
        'fitness': lambda x, y: 21.5 + (x * math.sin(4 * math.pi * x)) + (y * math.sin(20 * math.pi * y)),
        'Z':       lambda X, Y, k: 21.5 + (X * np.sin(4 * np.pi * X)) + (Y * np.sin(20 * np.pi * Y))
    },
    2: {
        'ax': -3.0, 'bx': 3.0,
        'ay': -3.0, 'by': 3.0,
        'fitness': lambda x, y: ((1-x)**2 * math.exp(-x**2 - (y+1)**2)) - ((x - x**3 - y**3) * math.exp(-x**2 - y**2)),
        'Z':       lambda X, Y, k: ((1-X)**2 * np.exp(-X**2 - (Y+1)**2)) - ((X - X**3 - Y**3) * np.exp(-X**2 - Y**2))
    },
    3: {
        'ax': 0.0, 'bx': 1.0,
        'ay': 0.0, 'by': 1.0,
        'fitness': lambda x, y: (16 * x * (1-x) * y * (1-y) * math.sin(K * math.pi * x) * math.sin(K * math.pi * y))**2,
        'Z':       lambda X, Y, k: (16 * X * (1-X) * Y * (1-Y) * np.sin(k * np.pi * X) * np.sin(k * np.pi * Y))**2
    }
}

'''  - - - - - - - - - - - - - - - Operaciones del algoritmo evolutivo - - - - - - - - - - - - - - - '''
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
        
    
def mutacion(poblacion, nueva_poblacion, M, ax, bx, ay, by):
    for _ in range(int(M)):
        individuo = random.choice(poblacion)
        x_mutado = individuo[0] + random.gauss(0, individuo[2])
        y_mutado = individuo[1] + random.gauss(0, individuo[3])
        # Mantener dentro de los límites
        if x_mutado < ax:
            x_mutado = ax
        if x_mutado > bx:
            x_mutado = bx
        if y_mutado < ay:
            y_mutado = ay
        if y_mutado > by:
            y_mutado = by
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


'''  - - - - - - - - - - - - - - - Función de algoritmo genético - - - - - - - - - - - - - - - '''
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
    generaciones=0 # Contador de generaciones
    snapshots = [] # Lista para almacenar snapshots de la población cada 200 generaciones
    
    # Generar población inicial de manera random: números decimales que pertenecen a los reales
    poblacion = generar_poblacion(M, ax, bx, ay, by)
    
    # Ciclo de evolución
    for _ in range(i):
        # Calcular el fitness de cada individuo 
        valores_fitness = [fitness(individuo[0], individuo[1]) for individuo in poblacion]
        
        # Crear L nuevos individuos 
        mutacion(poblacion, nuevos_individuos, int(L*m), ax, bx, ay, by) # MUTACIÓN
        n = len(nuevos_individuos)
        cruza_promedio(poblacion, nuevos_individuos, L-n) # CRUZA (los que faltan)
        
        # M + L 
        poblacion.extend(nuevos_individuos)
        
        # Seleccionar a los mejores M individuos
        poblacion = sorted(poblacion, key=lambda individuo: fitness(individuo[0], individuo[1]), reverse=True)[:M]
        valores_fitness = [fitness(individuo[0], individuo[1]) for individuo in poblacion] # Recalcular fitness
        
        print(f"Media del fitness de la generación actual: {sum(valores_fitness)/M} (len={len(valores_fitness)})")
        
        fitness_historial.append(max(valores_fitness)) # Guardar el mejor fitness de la generación actual    
        fitness_promedio.append(mean(valores_fitness)) # Guardar el fitness promedio de la generación actual
        
        if generaciones%200 == 0:
            mejor_idx = valores_fitness.index(max(valores_fitness))
            snapshots.append((generaciones, list(poblacion), poblacion[mejor_idx]))
        
        nuevos_individuos.clear() # Limpiar la lista de nuevos individuos
        generaciones+=1;
    
    # Guardar último snapshot 
    mejor_idx = valores_fitness.index(max(valores_fitness))
    snapshots.append((generaciones, list(poblacion), poblacion[mejor_idx]))
    
    print(f"Se terminó el algoritmo evolutivo después de {i} generaciones, tamaño de la población final: {len(poblacion)}")
    return fitness_historial, fitness_promedio, snapshots

'''  - - - - - - - - - - - - - - - Funciones para graficar - - - - - - - - - - - - - - - - '''
def graficar_evolucion(snapshots, ax, bx, ay, by, k=2):
    x = np.linspace(ax, bx, 300)
    y = np.linspace(ay, by, 300)
    X, Y = np.meshgrid(x, y)
    
    Z = FUNCIONES[FUNCION]['Z'](X, Y, K)

    fig, ax_plot = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.15)  

    # Índice del frame actual
    estado = {'frame': 0}  
    def dibujar(frame):
        ax_plot.cla()
        ax_plot.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5, zorder=1)
        ax_plot.set_xlim(ax, bx)
        ax_plot.set_ylim(ay, by)

        gen, poblacion, mejor = snapshots[frame]
        xs = [ind[0] for ind in poblacion]
        ys = [ind[1] for ind in poblacion]

        ax_plot.scatter(xs, ys, c='steelblue', s=25, alpha=0.8, label='Población')
        ax_plot.scatter(mejor[0], mejor[1], c='red', s=100, marker='*', label='Mejor individuo')
        ax_plot.set_title(f'Generación {gen}  ({frame+1}/{len(snapshots)})')
        ax_plot.legend(loc='upper right')
        fig.canvas.draw()

    def siguiente(event):
        if estado['frame'] < len(snapshots) - 1:
            estado['frame'] += 1
            dibujar(estado['frame'])

    def anterior(event):
        if estado['frame'] > 0:
            estado['frame'] -= 1
            dibujar(estado['frame'])

    # Crear botones
    ax_prev = plt.axes([0.3, 0.03, 0.15, 0.06])
    ax_next = plt.axes([0.55, 0.03, 0.15, 0.06])
    btn_prev = Button(ax_prev, '← Anterior')
    btn_next = Button(ax_next, 'Siguiente →')

    btn_prev.on_clicked(anterior)
    btn_next.on_clicked(siguiente)

    dibujar(0) # mostrar primer frame
    plt.show()
    return btn_prev, btn_next  # retornar para que no se destruyan por garbage collection

    
    
'''  - - - - - - - - - - - - - - - - - - - MAIN - - - - - - - - - - - - - - - - - - - - - '''
# def _main__():
config = FUNCIONES[FUNCION]

best_fit, fitness_promedio, snapshots = algoritmo_evolutivo(config['fitness'], 100, 10, 5, 0.5, 0.2, config['ax'], config['bx'], config['ay'], config['by'])
plt.plot(fitness_promedio, label='Media del fitness')
plt.plot(best_fit, label='Mejor fitness')
plt.xlabel('Generación')
plt.ylabel('Fitness')
plt.title('Evolución del algoritmo evolutivo')
plt.legend()
plt.show()

anima = graficar_evolucion(snapshots, config['ax'], config['bx'], config['ay'], config['by'])


#_main__();