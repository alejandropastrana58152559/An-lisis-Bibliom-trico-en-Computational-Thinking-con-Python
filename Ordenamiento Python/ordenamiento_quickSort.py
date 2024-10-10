import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import random
import matplotlib.pyplot as plt
import os

# Función para implementar QuickSort iterativo
def quick_sort(arr):
    stack = [(0, len(arr) - 1)]

    with tqdm(total=len(arr), desc="Ordenando", unit="parte") as pbar:
        while stack:
            low, high = stack.pop()
            if low < high:
                # Particionar y obtener índice de pivote
                pi = partition(arr, low, high)
                # Empujar los subarreglos a la pila
                stack.append((low, pi - 1))
                stack.append((pi + 1, high))
            pbar.update(1)

def partition(arr, low, high):
    # Elegir un pivote aleatorio
    pivot_index = random.randint(low, high)
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high][2]  # Usar el año como pivote
    i = low - 1

    for j in range(low, high):
        if arr[j][2] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Cargar el DataFrame existente
input_file_path = 'DataFinal/combined_datafinal.csv'

# Leer el CSV
df = pd.read_csv(input_file_path)

# Filtrar las columnas relevantes
df_filtered = df[['Title', 'Autor', 'Year']]

# Asegurarse de que los valores en 'Year' son enteros válidos
df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')  # Convertir a numérico, establecer errores como NaN
df_filtered.dropna(subset=['Year'], inplace=True)  # Eliminar filas con NaN en 'Year'

# Asegurarse de que los valores de 'Year' son enteros
df_filtered['Year'] = df_filtered['Year'].astype(int)

# Convertir a lista de tuplas para ordenar
data_to_sort = list(zip(df_filtered['Title'], df_filtered['Autor'], df_filtered['Year']))

# Crear directorio para guardar los resultados si no existe
output_directory = 'Data_Ordenamiento/quickSort'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Función para imprimir el título con colores y detalles
def print_title(description):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Ordenamiento QuickSort - {description}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Listas para almacenar tamaños y tiempos de ejecución
sizes = []
execution_times = []

# Función para ejecutar QuickSort y mostrar resultados
def analyze_sort(arr, description, size):
    print_title(description)
    sizes.append(size)  # Agregar tamaño a la lista
    print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo: {size}" + Style.RESET_ALL)
    print("\n")

    # Iniciar la ordenación con QuickSort y medir el tiempo de ejecución
    start_time = time.time()

    # Usar tqdm para la barra de progreso en la ordenación
    tqdm.write(Fore.CYAN + "Ordenando..." )
    print("\n")
    quick_sort(arr)

    # Calcular el tiempo de ejecución
    execution_time = time.time() - start_time
    execution_times.append(execution_time)  # Agregar tiempo a la lista

    # Mostrar el tiempo de ejecución
    print("\n")
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)
    print("\n")

    # Crear un DataFrame con los resultados ordenados
    sorted_df = pd.DataFrame(arr, columns=['Title', 'Autor', 'Year'])

    # Guardar el DataFrame ordenado en un nuevo archivo CSV
    output_file_path = f'{output_directory}/quickSort_Ord_fechaPub_{size}.csv'
    sorted_df.to_csv(output_file_path, index=False)

    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    print(Fore.BLUE + f'Archivo CSV guardado en: {output_file_path}' + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

# Análisis con diferentes tamaños de datos
analyze_sort(data_to_sort.copy(), "Total de datos", len(data_to_sort))
analyze_sort(data_to_sort[:len(data_to_sort) // 2].copy(), "Mitad de datos", len(data_to_sort) // 2)
analyze_sort(data_to_sort[:len(data_to_sort) // 4].copy(), "Un cuarto de datos", len(data_to_sort) // 4)
analyze_sort(data_to_sort[:100].copy(), "Primeros 100 datos", 100)

# Crear la gráfica de comparación tamaño vs tiempo de ejecución
plt.figure(figsize=(10, 6))
plt.plot(sizes, execution_times, marker='o', linestyle='-', color='b', label='QuickSort')

plt.title('Tamaño del arreglo vs Tiempo de ejecución')
plt.xlabel('Tamaño del arreglo')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.grid(True)
plt.xticks(sizes)  # Marcas en el eje x para cada tamaño
plt.legend()

# Guardar el gráfico en la misma carpeta de salida
plt.savefig(f'{output_directory}/quickSort_tiempo_vs_tamaño.png')

# Mostrar el gráfico
plt.show()

print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)