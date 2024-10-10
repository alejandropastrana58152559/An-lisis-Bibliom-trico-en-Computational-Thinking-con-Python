import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Función para implementar Bucket Sort
def bucket_sort(arr):
    # Encontrar el rango de los años
    min_year = min(item[2] for item in arr)
    max_year = max(item[2] for item in arr)
    
    # Crear botes
    bucket_count = max_year - min_year + 1
    buckets = [[] for _ in range(bucket_count)]

    # Distribuir los elementos en los botes
    for item in arr:
        index = item[2] - min_year  # Índice en el bucket
        buckets[index].append(item)

    # Ordenar cada bucket y concatenarlos
    sorted_arr = []
    for bucket in tqdm(buckets, desc="Ordenando", unit="parte"):
        sorted_arr.extend(sorted(bucket, key=lambda x: x[2]))  # Ordenar cada bucket por año

    return sorted_arr

# Función para medir el tiempo de ejecución y mostrar resultados
def measure_sort_time(data_to_sort, description):
    # Mostrar el tamaño del arreglo
    size = len(data_to_sort)
    print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo ({description}): {size}" + Style.RESET_ALL)

    # Iniciar la ordenación con Bucket Sort y medir el tiempo de ejecución
    start_time = time.time()
    sorted_data = bucket_sort(data_to_sort)
    execution_time = time.time() - start_time

    # Mostrar el tiempo de ejecución
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución ({description}): {execution_time:.4f} segundos" + Style.RESET_ALL)

    return sorted_data, execution_time  # Retornar los datos ordenados y el tiempo

# Cargar el DataFrame existente
input_file_path = 'DataFinal/combined_datafinal.csv'
output_dir = 'Data_Ordenamiento/bucketSort'

# Crear la carpeta si no existe
os.makedirs(output_dir, exist_ok=True)

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

# Crear el título con colores y detalles
def print_title(title):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   {title}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Listas para almacenar tamaños y tiempos de ejecución
sizes = []
execution_times = []

# 1. Totalidad de los datos
print_title("Análisis con Totalidad de los Datos")
sorted_data_total, total_time = measure_sort_time(data_to_sort.copy(), "Totalidad")
sizes.append(len(data_to_sort))  # Guardar el tamaño
execution_times.append(total_time)  # Guardar el tiempo

# Guardar el CSV para la totalidad de los datos
output_file = os.path.join(output_dir, 'bucketSort_Ord_fechaPub_total.csv')
sorted_df = pd.DataFrame(sorted_data_total, columns=['Title', 'Autor', 'Year'])
sorted_df.to_csv(output_file, index=False)
print(Fore.BLUE + f'Archivo CSV guardado en: {output_file}' + Style.RESET_ALL)

# 2. Mitad de los datos
print_title("Análisis con Mitad de los Datos")
half_data = data_to_sort[:len(data_to_sort) // 2]
sorted_data_half, half_time = measure_sort_time(half_data.copy(), "Mitad")
sizes.append(len(half_data))
execution_times.append(half_time)

# Guardar el CSV para la mitad de los datos
output_file = os.path.join(output_dir, 'bucketSort_Ord_fechaPub_mitad.csv')
sorted_df = pd.DataFrame(sorted_data_half, columns=['Title', 'Autor', 'Year'])
sorted_df.to_csv(output_file, index=False)
print(Fore.BLUE + f'Archivo CSV guardado en: {output_file}' + Style.RESET_ALL)

# 3. Un cuarto de los datos
print_title("Análisis con Un Cuarto de los Datos")
quarter_data = data_to_sort[:len(data_to_sort) // 4]
sorted_data_quarter, quarter_time = measure_sort_time(quarter_data.copy(), "Un Cuarto")
sizes.append(len(quarter_data))
execution_times.append(quarter_time)

# Guardar el CSV para un cuarto de los datos
output_file = os.path.join(output_dir, 'bucketSort_Ord_fechaPub_un_cuarto.csv')
sorted_df = pd.DataFrame(sorted_data_quarter, columns=['Title', 'Autor', 'Year'])
sorted_df.to_csv(output_file, index=False)
print(Fore.BLUE + f'Archivo CSV guardado en: {output_file}' + Style.RESET_ALL)

# 4. 100 registros
print_title("Análisis con 100 Registros")
small_data = data_to_sort[:100]
sorted_data_small, small_time = measure_sort_time(small_data.copy(), "100 Registros")
sizes.append(len(small_data))
execution_times.append(small_time)

# Guardar el CSV para 100 registros
output_file = os.path.join(output_dir, 'bucketSort_Ord_fechaPub_100.csv')
sorted_df = pd.DataFrame(sorted_data_small, columns=['Title', 'Autor', 'Year'])
sorted_df.to_csv(output_file, index=False)
print(Fore.BLUE + f'Archivo CSV guardado en: {output_file}' + Style.RESET_ALL)

print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

# Crear gráfico comparativo de Tamaño vs Tiempo de Ejecución
plt.figure(figsize=(10, 6))
plt.plot(sizes, execution_times, marker='o', color='b', linestyle='-', label='Tiempo de ejecución')

# Etiquetas y título del gráfico
plt.xlabel('Tamaño del conjunto de datos')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.title('Comparación de Tamaño vs Tiempo de Ejecución - Bucket Sort')
plt.grid(True)
plt.legend()

# Guardar el gráfico en un archivo PNG
png_output_file = os.path.join(output_dir, 'tiempo_vs_tamaño_bucketSort.png')
plt.savefig(png_output_file)
print(Fore.BLUE + f'Gráfico guardado en: {png_output_file}' + Style.RESET_ALL)

# Mostrar el gráfico
plt.show()
