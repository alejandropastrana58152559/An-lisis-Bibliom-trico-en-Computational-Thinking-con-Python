import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Función para implementar Pigeonhole Sort
def pigeonhole_sort(arr):
    if not arr:  # Manejo de caso en el que el arreglo está vacío
        return

    min_val = min(arr, key=lambda x: x[2])[2]
    max_val = max(arr, key=lambda x: x[2])[2]
    size = max_val - min_val + 1

    # Crear "agujeros" para cada valor
    holes = [[] for _ in range(size)]

    # Distribuir los elementos en los agujeros
    for book in arr:
        holes[book[2] - min_val].append(book)

    # Recoger los elementos de los agujeros
    index = 0
    for hole in tqdm(holes, desc="Ordenando", unit="parte"):
        for book in hole:
            arr[index] = book
            index += 1

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
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Ordenamiento Pigeonhole Sort - {description}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Función para realizar el análisis en diferentes tamaños de datos y recopilar tiempos de ejecución
def analyze_sort(data):
    sizes = [len(data), len(data) // 2, len(data) // 4, 100]
    times = []
    
    # Crear carpeta de destino si no existe
    output_folder = 'Data_Ordenamiento/pigeOnHoleSort'
    os.makedirs(output_folder, exist_ok=True)
    
    for size in sizes:
        if size == 100 and len(data) < 100:  # Si hay menos de 100, ajusta el tamaño
            size = len(data)
        current_data = data[:size]

        # Imprimir el título de análisis
        print_title(f"Análisis con tamaño: {size}")

        # Iniciar la ordenación con Pigeonhole Sort y medir el tiempo de ejecución
        start_time = time.time()

        # Usar tqdm para la barra de progreso en la ordenación
        tqdm.write(Fore.CYAN + "Ordenando..." )
        print("\n")
        pigeonhole_sort(current_data)

        # Calcular el tiempo de ejecución
        execution_time = time.time() - start_time
        times.append(execution_time)

        # Mostrar el tiempo de ejecución
        print("\n")
        print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)
        print("\n")

        # Crear un DataFrame con los resultados ordenados
        sorted_df = pd.DataFrame(current_data, columns=['Title', 'Autor', 'Year'])

        # Guardar el DataFrame ordenado en un nuevo archivo CSV en la ruta especificada
        output_file_path = os.path.join(output_folder, f'pigeonholeSort_Ord_fechaPub_{size}.csv')
        sorted_df.to_csv(output_file_path, index=False)

        print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
        print(Fore.BLUE + f'Archivo CSV guardado en: {output_file_path}' + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    
    return sizes, times

# Realizar el análisis y obtener tamaños y tiempos
sizes, times = analyze_sort(data_to_sort)

# Crear el gráfico de tamaño vs tiempo
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o', color='b', linestyle='-', label='Tiempo de Ejecución')
plt.title('Tamaño del Arreglo vs Tiempo de Ejecución (Pigeonhole Sort)')
plt.xlabel('Tamaño del Arreglo')
plt.ylabel('Tiempo de Ejecución (segundos)')
plt.grid(True)
plt.legend()

# Guardar la imagen en la carpeta especificada
graph_file_path = os.path.join('Data_Ordenamiento/pigeOnHoleSort', 'tiempo_vs_tamaño_pigeonholeSort.png')
plt.savefig(graph_file_path)

# Mostrar la gráfica
plt.show()
