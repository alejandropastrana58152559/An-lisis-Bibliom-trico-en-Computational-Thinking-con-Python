import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Crear la ruta de salida si no existe
output_folder = 'Data_Ordenamiento/radixSort'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Función para implementar Counting Sort, subproceso de Radix Sort
def counting_sort(arr, exp):
    n = len(arr)
    output = [None] * n
    count = [0] * 10

    # Contar las ocurrencias de cada dígito
    for i in range(n):
        index = (arr[i][2] // exp) % 10
        count[index] += 1

    # Ajustar el count para que contenga las posiciones reales
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Construir el arreglo de salida
    for i in range(n - 1, -1, -1):
        index = (arr[i][2] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    # Copiar el arreglo de salida a arr
    for i in range(n):
        arr[i] = output[i]

# Función para implementar Radix Sort
def radix_sort(arr):
    max_value = max(arr, key=lambda x: x[2])[2]
    exp = 1
    max_digits = len(str(max_value))

    for digit in tqdm(range(max_digits), desc="Ordenando", unit="dígito"):
        counting_sort(arr, exp)
        exp *= 10

# Cargar el DataFrame existente
input_file_path = 'DataFinal/combined_datafinal.csv'

# Leer el CSV
df = pd.read_csv(input_file_path)

# Filtrar las columnas relevantes
df_filtered = df[['Title', 'Autor', 'Year']]

# Asegurarse de que los valores en 'Year' sean enteros válidos
df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')
df_filtered.dropna(subset=['Year'], inplace=True)
df_filtered['Year'] = df_filtered['Year'].astype(int)

# Convertir a lista de tuplas para ordenar
data_to_sort = list(zip(df_filtered['Title'], df_filtered['Autor'], df_filtered['Year']))

# Función para imprimir el título con colores y detalles
def print_title(description):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Ordenamiento Radix Sort - {description}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Listas para almacenar los tamaños y tiempos de ejecución
sizes = []
execution_times = []

# Función para ejecutar Radix Sort y mostrar resultados
def analyze_sort(arr, description):
    print_title(description)
    size = len(arr)
    print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo: {size}" + Style.RESET_ALL)
    print("\n")

    # Iniciar la ordenación con Radix Sort y medir el tiempo de ejecución
    start_time = time.time()

    tqdm.write(Fore.CYAN + "Ordenando...")
    radix_sort(arr)

    # Calcular el tiempo de ejecución
    execution_time = time.time() - start_time
    print("\n")
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)
    print("\n")

    # Guardar el resultado en CSV
    sorted_df = pd.DataFrame(arr, columns=['Title', 'Autor', 'Year'])
    output_file_path = os.path.join(output_folder, f"radixSort_Ord_fechaPub_{size}.csv")
    sorted_df.to_csv(output_file_path, index=False)

    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    print(Fore.BLUE + f'Archivo CSV guardado en: {output_file_path}' + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

    # Agregar los resultados a las listas
    sizes.append(size)
    execution_times.append(execution_time)

# Análisis con diferentes tamaños de datos
analyze_sort(data_to_sort.copy(), "Total de datos")

# Análisis con la mitad de los datos
half_data = data_to_sort[:len(data_to_sort) // 2]
analyze_sort(half_data.copy(), "Mitad de datos")

# Análisis con un cuarto de los datos
quarter_data = data_to_sort[:len(data_to_sort) // 4]
analyze_sort(quarter_data.copy(), "Un cuarto de datos")

# Análisis con solo 100 elementos
hundred_data = data_to_sort[:100]
analyze_sort(hundred_data.copy(), "Primeros 100 datos")

# Visualización de los resultados
plt.figure(figsize=(10, 6))
plt.plot(sizes, execution_times, marker='o', linestyle='-', color='b')
plt.title('Tamaño del arreglo vs Tiempo de ejecución (Radix Sort)')
plt.xlabel('Tamaño del arreglo')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.grid()

# Guardar la gráfica en un archivo .png
graph_output_path = os.path.join(output_folder, 'tiempo_vs_tamaño_radixSort.png')
plt.savefig(graph_output_path)

plt.show()

print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
