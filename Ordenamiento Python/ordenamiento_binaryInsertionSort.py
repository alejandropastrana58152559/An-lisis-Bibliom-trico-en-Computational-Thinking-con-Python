import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Función para implementar Binary Insertion Sort
def binary_insertion_sort(arr):
    def binary_search(sub_arr, val, start, end):
        while start <= end:
            mid = (start + end) // 2
            if sub_arr[mid][2] < val:  # Comparar años
                start = mid + 1
            else:
                end = mid - 1
        return start

    for i in tqdm(range(1, len(arr)), desc="Ordenando", unit="parte"):
        key_item = arr[i]
        # Encontrar el índice de inserción usando búsqueda binaria
        insert_index = binary_search(arr, key_item[2], 0, i - 1)
        # Mover los elementos hacia la derecha para hacer espacio
        arr.insert(insert_index, arr.pop(i))

# Función para ejecutar el algoritmo con diferentes tamaños de datos
def execute_sorting(data, size_label, output_folder):
    print_title(size_label)
    
    # Medir el tiempo de ejecución
    start_time = time.time()
    binary_insertion_sort(data)
    execution_time = time.time() - start_time

    # Mostrar el tamaño del arreglo y el tiempo de ejecución
    print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo: {len(data)}" + Style.RESET_ALL)
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)

    # Guardar el DataFrame ordenado en un archivo CSV en la ruta especificada
    sorted_df = pd.DataFrame(data, columns=['Title', 'Autor', 'Year'])
    output_file_path = os.path.join(output_folder, f'binaryInsertionSort_Ord_fechaPub_{len(data)}.csv')
    sorted_df.to_csv(output_file_path, index=False)
    
    print(Fore.BLUE + f'Archivo CSV guardado en: {output_file_path}' + Style.RESET_ALL)
    print("\n")
    
    return len(data), execution_time  # Retornar tamaño y tiempo de ejecución

# Función para imprimir el título con colores y detalles
def print_title(size_label):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Ordenamiento Binary Insertion Sort - {size_label}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

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

# Crear la carpeta de salida si no existe
output_folder = 'Data_Ordenamiento/binaryInsertionSort'
os.makedirs(output_folder, exist_ok=True)

# Lista para almacenar tamaños y tiempos de ejecución
sizes = []
execution_times = []

# Ejecutar con el total de los datos
size, exec_time = execute_sorting(data_to_sort.copy(), "Total de Datos", output_folder)
sizes.append(size)
execution_times.append(exec_time)

# Ejecutar con la mitad de los datos
half_size = len(data_to_sort) // 2
size, exec_time = execute_sorting(data_to_sort[:half_size].copy(), "Mitad de Datos", output_folder)
sizes.append(size)
execution_times.append(exec_time)

# Ejecutar con un cuarto de los datos
quarter_size = len(data_to_sort) // 4
size, exec_time = execute_sorting(data_to_sort[:quarter_size].copy(), "Un Cuarto de Datos", output_folder)
sizes.append(size)
execution_times.append(exec_time)

# Ejecutar con solo 100 datos
size, exec_time = execute_sorting(data_to_sort[:100].copy(), "100 Datos", output_folder)
sizes.append(size)
execution_times.append(exec_time)

# Mostrar el análisis completo
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

# Crear gráfico de tamaño vs tiempo de ejecución
plt.figure(figsize=(10, 6))
plt.plot(sizes, execution_times, marker='o', color='b', linestyle='-', label='Binary Insertion Sort')

# Personalizar el gráfico
plt.title('Comparación de Tamaño vs Tiempo de Ejecución', fontsize=14)
plt.xlabel('Tamaño del conjunto de datos', fontsize=12)
plt.ylabel('Tiempo de ejecución (segundos)', fontsize=12)
plt.grid(True)
plt.legend()

# Guardar la imagen en la carpeta especificada
graph_file_path = os.path.join(output_folder, 'tiempo_vs_tamaño_binaryInsertionSort.png')
plt.savefig(graph_file_path)

# Mostrar el gráfico
plt.show()




