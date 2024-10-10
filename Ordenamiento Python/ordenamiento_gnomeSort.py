import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Función para implementar Gnome Sort optimizada
def gnome_sort(arr):
    n = len(arr)
    index = 0
    step = max(1, n // 100)  # Reduce la frecuencia de actualización de tqdm

    # Mostrar progreso con tqdm
    with tqdm(total=n, desc="Ordenando", unit="parte") as pbar:
        while index < n:
            if index == 0:
                index += 1
            if arr[index][2] >= arr[index - 1][2]:  # Comparar años
                index += 1
            else:
                # Intercambiar si están en el orden incorrecto
                arr[index], arr[index - 1] = arr[index - 1], arr[index]
                index -= 1
                # Asegurarse de no ir a un índice negativo
                if index < 0:
                    index = 0

            # Actualizar la barra de progreso solo cada cierto número de iteraciones
            if index % step == 0 or index == n - 1:
                pbar.update(1)

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
def print_title(description):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Ordenamiento Gnome Sort - {description}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Función para ejecutar el análisis con todos los datos
def analyze_sort(data, description, output_folder):
    size = len(data)
    print_title(description)
    print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo: {size}" + Style.RESET_ALL)
    print("\n")

    # Copiar el arreglo original para mantener la integridad de los datos
    data_copy = list(data)  # Hacer una copia para evitar modificar el original

    # Iniciar la ordenación con Gnome Sort y medir el tiempo de ejecución
    start_time = time.time()

    # Usar tqdm para la barra de progreso en la ordenación
    tqdm.write(Fore.CYAN + "Ordenando...")
    print("\n")
    gnome_sort(data_copy)

    # Calcular el tiempo de ejecución
    execution_time = time.time() - start_time

    # Mostrar el tiempo de ejecución
    print("\n")
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)
    print("\n")

    # Guardar el DataFrame ordenado en un archivo CSV
    output_file_path = os.path.join(output_folder, f'gnomeSort_Ord_fechaPub_{size}.csv')
    sorted_df = pd.DataFrame(data_copy, columns=['Title', 'Autor', 'Year'])
    sorted_df.to_csv(output_file_path, index=False)

    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    print(Fore.BLUE + f'Archivo CSV guardado en: {output_file_path}' + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

    return execution_time  # Retornar el tiempo de ejecución

# Crear la carpeta de salida si no existe
output_folder = "Data_Ordenamiento/gnomeSort"
os.makedirs(output_folder, exist_ok=True)

# Almacenar tamaños y tiempos de ejecución
sizes = []
execution_times = []

# Análisis con la totalidad de los datos
total_size = len(data_to_sort)
execution_time_total = analyze_sort(data_to_sort, "Total de datos", output_folder)
sizes.append(total_size)
execution_times.append(execution_time_total)

# Análisis con la mitad de los datos
half_data = data_to_sort[:len(data_to_sort) // 2]
half_size = len(half_data)
execution_time_half = analyze_sort(half_data, "Mitad de datos", output_folder)
sizes.append(half_size)
execution_times.append(execution_time_half)

# Análisis con un cuarto de los datos
quarter_data = data_to_sort[:len(data_to_sort) // 4]
quarter_size = len(quarter_data)
execution_time_quarter = analyze_sort(quarter_data, "Un cuarto de datos", output_folder)
sizes.append(quarter_size)
execution_times.append(execution_time_quarter)

# Análisis con solo 100 elementos
hundred_data = data_to_sort[:100]
hundred_size = len(hundred_data)
execution_time_hundred = analyze_sort(hundred_data, "Primeros 100 datos", output_folder)
sizes.append(hundred_size)
execution_times.append(execution_time_hundred)

# Visualización de los resultados
plt.figure(figsize=(10, 6))
plt.plot(sizes, execution_times, marker='o', color='b', label='Tiempo de ejecución')
plt.title('Tamaño de datos vs Tiempo de ejecución (Gnome Sort)', fontsize=14)
plt.xlabel('Tamaño del conjunto de datos', fontsize=12)
plt.ylabel('Tiempo de ejecución (segundos)', fontsize=12)
plt.grid(True)
plt.legend()

# Guardar el gráfico como PNG en la carpeta de salida
output_graph_path = os.path.join(output_folder, 'tiempo_vs_tamaño_gnomeSort.png')
plt.savefig(output_graph_path)
plt.show()

print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)