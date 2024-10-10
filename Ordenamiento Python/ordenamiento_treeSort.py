import pandas as pd
import time
from tqdm import tqdm
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os

# Clase para el nodo del árbol
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

# Función para insertar un nodo en el árbol
def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if key[2] < root.val[2]:  
            root.left = insert(root.left, key)
        elif key[2] > root.val[2]:
            root.right = insert(root.right, key)
        else:
            if key[0] < root.val[0]:
                root.left = insert(root.left, key)
            else:
                root.right = insert(root.right, key)
    return root

# Función para hacer un recorrido inorden y almacenar los valores en una lista
def inorder(root, arr):
    if root:
        inorder(root.left, arr)
        arr.append(root.val)
        inorder(root.right, arr)

# Función para implementar Tree Sort
def tree_sort(arr):
    if not arr:
        return []
    
    root = None
    for item in arr:
        root = insert(root, item)

    sorted_arr = []
    inorder(root, sorted_arr)
    return sorted_arr

# Cargar el DataFrame existente
input_file_path = 'DataFinal/combined_datafinal.csv'
output_dir = 'Data_Ordenamiento/treeSort'  # Ruta para almacenar los archivos
os.makedirs(output_dir, exist_ok=True)  # Crear el directorio si no existe

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
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   Ordenamiento Tree Sort - {description}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Lista para almacenar tamaños y tiempos de ejecución
sizes = []
times = []

# Función para ejecutar Tree Sort y mostrar resultados
def analyze_sort(arr, description):
    print_title(description)
    size = len(arr)
    sizes.append(size)  
    print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo: {size}" + Style.RESET_ALL)
    print("\n")

    # Iniciar la ordenación con Tree Sort y medir el tiempo de ejecución
    start_time = time.time()
    tqdm.write(Fore.CYAN + "Ordenando..." )
    print("\n")
    sorted_data = tree_sort(arr)
    execution_time = time.time() - start_time
    times.append(execution_time)  

    print("\n")
    print(Fore.YELLOW + Style.BRIGHT + f"Tiempo de ejecución: {execution_time:.4f} segundos" + Style.RESET_ALL)
    print("\n")

    # Guardar el DataFrame ordenado en un nuevo archivo CSV
    output_file = f"{output_dir}/treeSort_Ord_fechaPub_{size}.csv"
    sorted_df = pd.DataFrame(sorted_data, columns=['Title', 'Autor', 'Year'])
    sorted_df.to_csv(output_file, index=False)

    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    print(Fore.BLUE + f'Archivo CSV guardado en: {output_file}' + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)

    return sorted_data

# Análisis con diferentes tamaños de datos
sorted_data_total = analyze_sort(data_to_sort, "Total de datos")
analyze_sort(data_to_sort[:len(data_to_sort) // 2], "Mitad de datos")
analyze_sort(data_to_sort[:len(data_to_sort) // 4], "Un cuarto de datos")
analyze_sort(data_to_sort[:100], "Primeros 100 datos")

# Visualización de resultados
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o', linestyle='-', color='b')
plt.title('Comparativa de Tamaño vs. Tiempo de Ejecución - Tree Sort')
plt.xlabel('Tamaño del Arreglo')
plt.ylabel('Tiempo de Ejecución (segundos)')
plt.grid()
plt.xticks(sizes)

# Guardar el gráfico en la misma carpeta
plt.savefig(f"{output_dir}/tiempo_vs_tamaño_treeSort.png")
plt.show()

print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
print(Fore.MAGENTA + Style.BRIGHT + "Análisis completo." + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
