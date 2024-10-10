import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Función para implementar HeapSort
def heapify(arr, n, i):
    largest = i  # Inicializar el nodo más grande como raíz
    left = 2 * i + 1  # índice del hijo izquierdo
    right = 2 * i + 2  # índice del hijo derecho

    # Verificar si el hijo izquierdo es mayor que la raíz
    if left < n and arr[left][2] > arr[largest][2]:
        largest = left

    # Verificar si el hijo derecho es mayor que el nodo más grande hasta ahora
    if right < n and arr[right][2] > arr[largest][2]:
        largest = right

    # Cambiar la raíz si es necesario
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # intercambiar

        # Recursivamente heapificar el subárbol afectado
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    # Construir el heap (reordenar el arreglo)
    for i in tqdm(range(n // 2 - 1, -1, -1), desc="Construyendo Heap", unit="parte"):
        heapify(arr, n, i)

    # Extraer elementos uno por uno del heap
    for i in tqdm(range(n - 1, 0, -1), desc="Ordenando", unit="parte"):
        arr[i], arr[0] = arr[0], arr[i]  # mover la raíz actual al final
        heapify(arr, i, 0)

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

# Función para imprimir el título con colores y detalles
def print_title(description, size):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Ordenamiento HeapSort - {description} (Tamaño: {size})   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Función para ejecutar HeapSort y mostrar resultados
def analyze_sort(arr, description):
    print_title(description, len(arr))
    
    # Iniciar la ordenación con HeapSort y medir el tiempo de ejecución
    start_time = time.time()

    # Usar tqdm para la barra de progreso en la ordenación
    tqdm.write(Fore.CYAN + "Ordenando..." )
    print("\n")
    heap_sort(arr)

    # Calcular el tiempo de ejecución
    execution_time = time.time() - start_time

    # Mostrar el tiempo de ejecución
    print("\n")
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)
    print("\n")
    
    return len(arr), execution_time

# Lista para guardar tamaños y tiempos de ejecución
sizes = []
times = []

# Análisis con diferentes tamaños de datos
for analysis_type, data in [("Total de datos", data_to_sort),
                             ("Mitad de datos", data_to_sort[:len(data_to_sort) // 2]),
                             ("Un cuarto de datos", data_to_sort[:len(data_to_sort) // 4]),
                             ("Primeros 100 datos", data_to_sort[:100])]:
    
    size, time_taken = analyze_sort(data, analysis_type)
    sizes.append(size)
    times.append(time_taken)
    
    # Crear un DataFrame con los resultados ordenados
    sorted_df = pd.DataFrame(data, columns=['Title', 'Autor', 'Year'])
    
    # Guardar el DataFrame ordenado en un nuevo archivo CSV
    output_file_path = f'Data_Ordenamiento/HeapSort/heapSort_Ord_fechaPub_{size}.csv'
    sorted_df.to_csv(output_file_path, index=False)
    
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    print(Fore.BLUE + f'Archivo CSV guardado en: {output_file_path}' + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

# Crear la carpeta de salida si no existe
os.makedirs('Data_Ordenamiento/HeapSort', exist_ok=True)

# Visualizar el tiempo de ejecución vs el tamaño del conjunto de datos
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o', linestyle='-', color='b')
plt.title('Tamaño de datos vs Tiempo de ejecución (HeapSort)', fontsize=14)
plt.xlabel('Tamaño del conjunto de datos', fontsize=12)
plt.ylabel('Tiempo de ejecución (segundos)', fontsize=12)
plt.grid(True)

# Guardar el gráfico como PNG
plt.savefig('Data_Ordenamiento/HeapSort/tiempo_vs_tamaño_heapSort.png')
plt.show()

print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
