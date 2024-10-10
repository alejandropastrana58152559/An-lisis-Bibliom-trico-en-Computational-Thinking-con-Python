import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Crear la carpeta de salida si no existe
output_dir = 'Data_Ordenamiento/timeSort'
os.makedirs(output_dir, exist_ok=True)

# Función para implementar TimSort
def tim_sort(arr):
    min_run = 32

    # Ordenamiento por inserción
    def insertion_sort(sub_arr, left, right):
        for i in range(left + 1, right + 1):
            key_item = sub_arr[i]
            j = i - 1
            while j >= left and sub_arr[j][2] > key_item[2]:  # Comparar el campo Year (índice 2)
                sub_arr[j + 1] = sub_arr[j]
                j -= 1
            sub_arr[j + 1] = key_item

    # Mezcla de dos subarrays
    def merge(left, mid, right):
        left_copy = arr[left:mid + 1]
        right_copy = arr[mid + 1:right + 1]

        left_index, right_index = 0, 0
        sorted_index = left

        # Comparar elementos y mezclar los subarrays
        while left_index < len(left_copy) and right_index < len(right_copy):
            if left_copy[left_index][2] <= right_copy[right_index][2]:  # Comparar el campo Year
                arr[sorted_index] = left_copy[left_index]
                left_index += 1
            else:
                arr[sorted_index] = right_copy[right_index]
                right_index += 1
            sorted_index += 1

        # Copiar los elementos restantes
        while left_index < len(left_copy):
            arr[sorted_index] = left_copy[left_index]
            left_index += 1
            sorted_index += 1

        while right_index < len(right_copy):
            arr[sorted_index] = right_copy[right_index]
            right_index += 1
            sorted_index += 1

    n = len(arr)
    # Dividir el array en pequeñas secciones para ordenar
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end)

    size = min_run
    # Combinar subarrays
    while size < n:
        for left in tqdm(range(0, n, size * 2), desc="Ordenando", unit="parte"):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))

            if mid < right:
                merge(left, mid, right)
        size *= 2

# Cargar el DataFrame existente
input_file_path = 'DataFinal/combined_datafinal.csv'

# Leer el CSV
df = pd.read_csv(input_file_path)

# Filtrar las columnas relevantes
df_filtered = df[['Title', 'Autor', 'Year']]

# Asegurarse de que los valores en 'Year' son enteros válidos
df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')  # Convertir a numérico
df_filtered.dropna(subset=['Year'], inplace=True)  # Eliminar filas con NaN en 'Year'
df_filtered['Year'] = df_filtered['Year'].astype(int)  # Convertir a int

# Convertir a lista de tuplas para ordenar
data_to_sort = list(zip(df_filtered['Title'], df_filtered['Autor'], df_filtered['Year']))

# Función para imprimir el título con colores y detalles
def print_title(description):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Ordenamiento TimSort - {description}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Lista para almacenar tamaños y tiempos de ejecución
sizes = []
execution_times = []

# Función para ejecutar TimSort y mostrar resultados
def analyze_sort(arr, description, size_name):
    print_title(description)
    size = len(arr)
    print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo: {size}" + Style.RESET_ALL)
    print("\n")

    # Iniciar la ordenación con TimSort y medir el tiempo de ejecución
    start_time = time.time()

    # Usar tqdm para la barra de progreso en la ordenación
    tqdm.write(Fore.CYAN + "Ordenando..." )
    print("\n")
    tim_sort(arr)

    # Calcular el tiempo de ejecución
    execution_time = time.time() - start_time

    # Mostrar el tiempo de ejecución
    print("\n")
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)
    print("\n")

    # Guardar los resultados en un archivo CSV
    output_csv_path = f'{output_dir}/timeSort_Ord_fechaPub_{size_name}.csv'
    sorted_df = pd.DataFrame(arr, columns=['Title', 'Autor', 'Year'])
    sorted_df.to_csv(output_csv_path, index=False)

    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    print(Fore.BLUE + f'Archivo CSV guardado en: {output_csv_path}' + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

    # Almacenar los resultados
    sizes.append(size)
    execution_times.append(execution_time)

# Análisis con diferentes tamaños de datos
analyze_sort(data_to_sort.copy(), "Total de datos", len(data_to_sort))

# Análisis con la mitad de los datos
half_data = data_to_sort[:len(data_to_sort) // 2]
analyze_sort(half_data.copy(), "Mitad de datos", len(half_data))

# Análisis con un cuarto de los datos
quarter_data = data_to_sort[:len(data_to_sort) // 4]
analyze_sort(quarter_data.copy(), "Un cuarto de datos", len(quarter_data))

# Análisis con solo 100 elementos
hundred_data = data_to_sort[:100]
analyze_sort(hundred_data.copy(), "Primeros 100 datos", 100)

# Visualizar resultados
plt.figure(figsize=(10, 5))
plt.plot(sizes, execution_times, marker='o', linestyle='-', color='b')
plt.title('Tamaño del arreglo vs Tiempo de Ejecución (TimSort)')
plt.xlabel('Tamaño del arreglo')
plt.ylabel('Tiempo de Ejecución (segundos)')
plt.xticks(sizes)  # Establecer las marcas del eje x
plt.grid()

# Guardar la gráfica como imagen PNG
output_png_path = f'{output_dir}/tiempo_vs_tamaño_timsort.png'
plt.savefig(output_png_path)
plt.show()

print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

