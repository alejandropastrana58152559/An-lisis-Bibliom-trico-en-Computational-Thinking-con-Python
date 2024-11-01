import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Style, Fore, init
from tqdm import tqdm
import os
import time

# Configuración de colorama y estilo de gráficos
init(autoreset=True)
sns.set(style="whitegrid")
plt.rcParams["figure.autolayout"] = True

# Cambiar fuente a una más completa
plt.rcParams['font.family'] = 'DejaVu Sans'

# Definir la ruta de salida y crear carpeta si no existe
output_folder = 'requerimiento2/statistics'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Leer el archivo CSV
df = pd.read_csv('DataFinal/combined_datafinal.csv')

# Filtrar datos que no tengan "Sin Valor"
df = df.replace("Sin Valor", pd.NA)

# Imprimir los nombres de las columnas para verificación
print("Nombres de columnas:", df.columns)

# Función para imprimir títulos
def print_title(msg):
    print("\n")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  {msg}  ")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Variables y configuraciones para análisis simple
simple_analysis_configs = [
    ("Autor", "15 autores más citados", "autor", df['Autor'].dropna().value_counts().nlargest(15)),
    ("Year", "Año de publicación", "year", df['Year'].dropna().value_counts().sort_index()),
    ("Publisher", "Publisher", "publisher", df['Publisher'].dropna().value_counts()),
    ("Database", "Base de datos", "database", df['Database'].dropna().value_counts()),
    ("Publication Title", "Journal", "journal", df['Publication Title'].dropna().value_counts()),
]

# Generar gráficos para análisis simple
print_title("Generando estadísticos descriptivos y guardando gráficos en PNG")

start_time = time.time()

with tqdm(total=len(simple_analysis_configs), desc="Generando estadísticos simples", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
    for var, title, filename, data in simple_analysis_configs:
        plt.figure(figsize=(10, 6))
        
        # Usar `hue` para evitar la advertencia de `palette`
        sns.barplot(x=data.values, y=data.index, palette="viridis", hue=data.index, dodge=False)
        
        plt.title(f"{title}", fontsize=14)
        plt.xlabel("Cantidad", fontsize=12)
        plt.ylabel(var, fontsize=12)
        
        # Ajustar márgenes para evitar advertencias
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plt.tight_layout()
        
        # Guardar gráfico
        plt.savefig(f"{output_folder}/{filename}_estadistico.png")
        plt.close()
        
        # Actualizar barra de progreso
        tqdm.write(f"Gráfico de {title} guardado.")
        pbar.update(1)
    
# Configuraciones para análisis combinado
combined_analysis_configs = []
# Comprobar si la columna 'Document Type' existe antes de agregarla a la configuración
if 'Document Type' in df.columns:
    combined_analysis_configs.append(("Year", "Tipo de producto", "Año - Tipo de producto", "year_doc_type", 
     df.groupby(['Year', 'Document Type']).size().unstack(fill_value=0).reset_index()))

combined_analysis_configs.append(("Database", "Autor", "Base de datos - Autor", "database_author", 
     df.groupby(['Database', 'Autor']).size().unstack(fill_value=0).dropna(how='all').reset_index()))
combined_analysis_configs.append(("Publication Title", "Title", "Journal - Artículo", "journal_article", 
     df.groupby(['Publication Title', 'Title']).size().unstack(fill_value=0).dropna(how='all').reset_index()))

# Generar gráficos para análisis combinado
print_title("Generando estadísticos descriptivos combinados y guardando gráficos en PNG")

with tqdm(total=len(combined_analysis_configs), desc="Generando estadísticos combinados", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
    for var1, var2, title, filename, data in combined_analysis_configs:
        plt.figure(figsize=(12, 8))
        sns.heatmap(data.set_index(var1), annot=True, cmap="YlGnBu", cbar=True)
        plt.title(f"{title}", fontsize=14)
        plt.xlabel(var2, fontsize=12)
        plt.ylabel(var1, fontsize=12)
        
        # Ajustar márgenes para evitar advertencias
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plt.tight_layout()
        
        # Guardar gráfico
        plt.savefig(f"{output_folder}/{filename}_estadistico_combinado.png")
        plt.close()
        
        # Actualizar barra de progreso
        tqdm.write(f"Gráfico combinado de {title} guardado.")
        pbar.update(1)

end_time = time.time()
print(Fore.GREEN + f"\nEstadísticos generados y guardados en la carpeta '{output_folder}'. Tiempo total: {end_time - start_time:.2f} segundos.")
print("=" * 60)





