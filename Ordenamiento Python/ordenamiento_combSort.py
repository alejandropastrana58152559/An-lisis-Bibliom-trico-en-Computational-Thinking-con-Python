import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Función para implementar Comb Sort directamente en el DataFrame
def comb_sort_df(df, column):
    n = len(df)
    gap = n
    shrink = 1.3
    sorted = False

    while not sorted:
        # Calcular el nuevo gap
        gap = int(gap / shrink)
        if gap < 1:
            gap = 1
        
        sorted = True
        
        # Mostrar progreso
        print(Fore.CYAN + f"Ordenando... (gap: {gap})" + Style.RESET_ALL)
        
        # Ordenar el DataFrame en el lugar
        for i in range(n - gap):
            if df.iloc[i][column] > df.iloc[i + gap][column]:  # Comparar el año
                # Intercambiar filas en el DataFrame
                df.iloc[i], df.iloc[i + gap] = df.iloc[i + gap].copy(), df.iloc[i].copy()
                sorted = False  # Aún no está completamente ordenado

# Función para imprimir títulos personalizados
def print_analysis_title(description):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Análisis: {description}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Función para realizar el análisis en diferentes tamaños de subconjuntos y guardar CSV
def analyze_sorting_and_save(df_to_sort, description, size_label):
    print_analysis_title(description)  # Imprimir el título con descripción personalizada
    
    size = len(df_to_sort)
    print(Fore.GREEN + Style.BRIGHT + f"\n*** Analizando con {description} ({size} elementos) ***" + Style.RESET_ALL)
    
    # Medir el tiempo de ejecución
    start_time = time.time()
    comb_sort_df(df_to_sort, 'Year')
    execution_time = time.time() - start_time
    
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)

    # Guardar el DataFrame ordenado en un archivo CSV
    output_file_path = f'Data_Ordenamiento/combSort/combSort_Ord_fechaPub_{size_label}.csv'
    df_to_sort.to_csv(output_file_path, index=False)
    
    print(Fore.BLUE + f'Archivo CSV guardado en: {output_file_path}' + Style.RESET_ALL)
    
    return size, execution_time  # Retornar el tamaño y tiempo de ejecución

# Cargar el DataFrame existente
input_file_path = 'DataFinal/combined_datafinal.csv'

# Leer el CSV
df = pd.read_csv(input_file_path)

# Filtrar las columnas relevantes
df_filtered = df[['Title', 'Autor', 'Year']]

# Asegurarse de que los valores en 'Year' son enteros válidos
df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')  # Convertir a numérico
df_filtered.dropna(subset=['Year'], inplace=True)  # Eliminar filas con NaN en 'Year'

# Asegurarse de que los valores de 'Year' son enteros
df_filtered['Year'] = df_filtered['Year'].astype(int)

# Crear el título principal con colores y detalles
def print_main_title():
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + "  ***   Ordenamiento Comb Sort   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

print_main_title()

# Lista para almacenar tamaños y tiempos de ejecución
sizes = []
times = []

# Crear la carpeta si no existe
os.makedirs('Data_Ordenamiento/combSort', exist_ok=True)

# Realizar el análisis con la totalidad de los datos y guardar CSV
size, time_taken = analyze_sorting_and_save(df_filtered.copy(), "la totalidad de los datos", "totalidad")
sizes.append(size)
times.append(time_taken)

# Realizar el análisis con la mitad de los datos y guardar CSV
half_data = df_filtered.iloc[:len(df_filtered) // 2].copy()
size, time_taken = analyze_sorting_and_save(half_data, "la mitad de los datos", "mitad")
sizes.append(size)
times.append(time_taken)

# Realizar el análisis con un cuarto de los datos y guardar CSV
quarter_data = df_filtered.iloc[:len(df_filtered) // 4].copy()
size, time_taken = analyze_sorting_and_save(quarter_data, "un cuarto de los datos", "cuarto")
sizes.append(size)
times.append(time_taken)

# Realizar el análisis con solo 100 elementos y guardar CSV
hundred_data = df_filtered.iloc[:100].copy()
size, time_taken = analyze_sorting_and_save(hundred_data, "100 datos", "100")
sizes.append(size)
times.append(time_taken)

print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

# Graficar los resultados del análisis (tamaño vs tiempo de ejecución)
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o', linestyle='-', color='b')
plt.title('Tamaño vs Tiempo de ejecución (Comb Sort)')
plt.xlabel('Tamaño de los datos')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.grid(True)
plt.savefig('Data_Ordenamiento/combSort/tiempo_vs_tamaño_combSort.png')  # Guardar la gráfica en un archivo PNG
plt.show()

