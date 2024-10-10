import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Función para implementar Bitonic Sort
def bitonic_sort(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        # Ascendente ordenado
        bitonic_sort(arr, low, k, 1)
        # Descendente ordenado
        bitonic_sort(arr, low + k, k, 0)
        # Mezclar
        bitonic_merge(arr, low, cnt, direction)

def bitonic_merge(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            if (direction == 1 and arr[i][2] > arr[i + k][2]) or (direction == 0 and arr[i][2] < arr[i + k][2]):
                arr[i], arr[i + k] = arr[i + k], arr[i]
        bitonic_merge(arr, low, k, direction)
        bitonic_merge(arr, low + k, k, direction)

# Función para realizar el análisis de Bitonic Sort
def run_bitonic_sort(data, label):
    print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo ({label}): {len(data)}" + Style.RESET_ALL)

    # Llenar el arreglo a una potencia de 2 para Bitonic Sort
    n = 1
    while n < len(data):
        n *= 2
    n = max(n, len(data))

    # Asegurar que el arreglo tenga la longitud correcta
    data.extend([(None, None, float('inf'))] * (n - len(data)))  # Llenar con inf para evitar problemas

    # Iniciar la ordenación con Bitonic Sort y medir el tiempo de ejecución
    start_time = time.time()

    # Usar tqdm para la barra de progreso en la ordenación
    tqdm.write(Fore.CYAN + f"Ordenando {label}...")
    bitonic_sort(data, 0, n, 1)

    # Calcular el tiempo de ejecución
    execution_time = time.time() - start_time

    # Mostrar el tiempo de ejecución
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución ({label}): {execution_time:.4f} segundos" + Style.RESET_ALL)

    return execution_time  # Retornar el tiempo de ejecución

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

# Función para imprimir títulos con formato
def print_title(label):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Análisis de Ordenamiento Bitonic Sort - {label}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Listas para almacenar los tamaños y tiempos de ejecución
sizes = []
times = []

# Crear directorio si no existe
output_dir = 'Data_Ordenamiento/bitonicSort'
os.makedirs(output_dir, exist_ok=True)

# Función para guardar resultados y generar CSV
def save_sorted_data(data, size_label):
    sorted_df = pd.DataFrame(data, columns=['Title', 'Autor', 'Year'])
    file_name = f'{output_dir}/bitonicSort_Ord_fechaPub_{size_label}.csv'
    sorted_df.to_csv(file_name, index=False)
    print(Fore.MAGENTA + Style.BRIGHT + f"Archivo CSV guardado en: {file_name}" + Style.RESET_ALL)

# Ejecutar el análisis con la totalidad de los datos
total_size = len(data_to_sort)
print_title(f"{total_size}")
data_total = data_to_sort.copy()
execution_time = run_bitonic_sort(data_total, f"Totalidad ({total_size})")
sizes.append(total_size)
times.append(execution_time)
save_sorted_data(data_total, f"{total_size}")

# Ejecutar análisis de la mitad de los datos
half_size = len(data_to_sort) // 2
print_title(f"{half_size}")
data_half = data_to_sort[:half_size].copy()
execution_time = run_bitonic_sort(data_half, f"Mitad ({half_size})")
sizes.append(half_size)
times.append(execution_time)
save_sorted_data(data_half, f"{half_size}")

# Ejecutar análisis de un cuarto de los datos
quarter_size = len(data_to_sort) // 4
print_title(f"{quarter_size}")
data_quarter = data_to_sort[:quarter_size].copy()
execution_time = run_bitonic_sort(data_quarter, f"Un cuarto ({quarter_size})")
sizes.append(quarter_size)
times.append(execution_time)
save_sorted_data(data_quarter, f"{quarter_size}")

# Ejecutar análisis de solo 100 elementos
sample_size = 100
print_title(f"{sample_size}")
data_100 = data_to_sort[:sample_size].copy()
execution_time = run_bitonic_sort(data_100, f"100 elementos ({sample_size})")
sizes.append(sample_size)
times.append(execution_time)
save_sorted_data(data_100, f"{sample_size}")

# Visualizar la comparación de tamaño vs tiempo de ejecución usando Matplotlib
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o', linestyle='-', color='b', label='Bitonic Sort')
plt.title("Tamaño del arreglo vs Tiempo de ejecución (Bitonic Sort)")
plt.xlabel("Tamaño del arreglo")
plt.ylabel("Tiempo de ejecución (segundos)")
plt.grid(True)
plt.legend()

# Guardar el gráfico como archivo PNG
plt_file_path = f'{output_dir}/tiempo_vs_tamaño_bitonicSort.png'
plt.savefig(plt_file_path)
plt.show()

print(Fore.MAGENTA + Style.BRIGHT + f"Gráfico guardado en: {plt_file_path}" + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)





