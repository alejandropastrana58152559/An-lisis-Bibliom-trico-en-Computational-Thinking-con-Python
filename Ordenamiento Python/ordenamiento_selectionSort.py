import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Función para implementar Selection Sort
def selection_sort(arr):
    n = len(arr)
    for i in tqdm(range(n), desc="Ordenando", unit="parte"):
        min_index = i
        for j in range(i + 1, n):
            if arr[j][2] < arr[min_index][2]:  # Comparar años
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

# Cargar el DataFrame existente
input_file_path = 'DataFinal/combined_datafinal.csv'

# Leer el CSV
df = pd.read_csv(input_file_path)

# Filtrar las columnas relevantes
df_filtered = df[['Title', 'Autor', 'Year']]

# Asegurarse de que los valores en 'Year' son enteros válidos
df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')
df_filtered.dropna(subset=['Year'], inplace=True)
df_filtered['Year'] = df_filtered['Year'].astype(int)

# Convertir a lista de tuplas para ordenar
data_to_sort = list(zip(df_filtered['Title'], df_filtered['Autor'], df_filtered['Year']))

# Función para imprimir el título con colores y detalles
def print_title(description):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Ordenamiento Selection Sort - {description}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Inicializar listas para el análisis de tiempo
sizes = []
execution_times = []

# Crear el directorio de salida si no existe
output_dir = 'Data_Ordenamiento/selectionSort'
os.makedirs(output_dir, exist_ok=True)

# Función para ejecutar Selection Sort y mostrar resultados
def analyze_sort(arr, description, size_label):
    print_title(description)
    size = len(arr)
    sizes.append(size)
    print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo: {size}" + Style.RESET_ALL)
    print("\n")

    start_time = time.time()
    tqdm.write(Fore.CYAN + "Ordenando..." )
    print("\n")
    selection_sort(arr)

    execution_time = time.time() - start_time
    execution_times.append(execution_time)

    print("\n")
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)
    print("\n")

    # Guardar los resultados en un archivo CSV
    sorted_df = pd.DataFrame(arr, columns=['Title', 'Autor', 'Year'])
    output_file_path = f'{output_dir}/selectionSort_Ord_fechaPub_{size_label}.csv'
    sorted_df.to_csv(output_file_path, index=False)

    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    print(Fore.BLUE + f'Archivo CSV guardado en: {output_file_path}' + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

# Análisis con diferentes tamaños de datos
analyze_sort(data_to_sort.copy(), "Total de datos", len(data_to_sort))

# Análisis con la mitad de los datos
half_data = data_to_sort[:len(data_to_sort) // 2].copy()
analyze_sort(half_data, "Mitad de datos", len(half_data))

# Análisis con un cuarto de los datos
quarter_data = data_to_sort[:len(data_to_sort) // 4].copy()
analyze_sort(quarter_data, "Un cuarto de datos", len(quarter_data))

# Análisis con solo 100 elementos
hundred_data = data_to_sort[:100].copy()
analyze_sort(hundred_data, "Primeros 100 datos", len(hundred_data))

# Crear el gráfico de tamaño vs tiempo de ejecución
plt.figure(figsize=(10, 6))
plt.plot(sizes, execution_times, marker='o', linestyle='-', color='b', label='Tiempo de Ejecución')
plt.title('Tamaño del Arreglo vs Tiempo de Ejecución (Selection Sort)')
plt.xlabel('Tamaño del Arreglo')
plt.ylabel('Tiempo de Ejecución (segundos)')
plt.grid(True)
plt.legend()

# Guardar la gráfica en la carpeta
graph_output_path = f'{output_dir}/tiempo_vs_tamaño_selectionSort.png'
plt.savefig(graph_output_path)
plt.show()

print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

