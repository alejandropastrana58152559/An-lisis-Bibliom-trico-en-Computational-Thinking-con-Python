import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter, defaultdict
import re
from tqdm import tqdm
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Función para cargar categorías y variables desde el archivo de texto
def load_categories_from_file(filepath):
    categories = defaultdict(list)
    with open(filepath, 'r', encoding='utf-8') as file:
        current_category = None
        for line in file:
            line = line.strip()
            # Detectar el inicio de una nueva categoría
            if line.lower().startswith("categoría:") or line.lower().startswith("categoria:"):
                current_category = line.split(":")[1].strip()
            # Detectar variables dentro de una categoría
            elif line and current_category and not line.lower().startswith("variables:"):
                categories[current_category].append(line)
    return dict(categories)

# Función para imprimir el título con el formato solicitado
def print_title(title):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   {title}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Función para procesar los abstracts y contar las palabras clave
def count_keywords_in_abstracts(df, categories):
    # Almacenar resultados de las frecuencias por categoría
    keyword_frequencies = {category: Counter() for category in categories}
    
    # Progreso de la terminal con tqdm y colorama
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc=Fore.GREEN + "Procesando abstracts", unit="step"):
        abstract = str(row['Abstract']).lower()  # Convertir a minúsculas para búsqueda insensible a mayúsculas
        
        # Procesar sinónimos con guiones, unificando en una sola palabra
        for category, keywords in categories.items():
            for keyword in keywords:
                # Reemplazar sinónimos por la palabra clave unificada
                keyword_lower = keyword.lower()
                if '-' in keyword:
                    unified_keyword = keyword.split('-')[0].lower()  # Seleccionar la primera parte como la palabra clave unificada
                else:
                    unified_keyword = keyword_lower

                # Buscar si la palabra clave (o su versión unificada) aparece en el abstract
                if re.search(r'\b' + re.escape(unified_keyword) + r'\b', abstract):  # Asegurarse de que sea una palabra completa
                    keyword_frequencies[category][unified_keyword] += 1

    return keyword_frequencies

# Función para generar una única nube de palabras
def generate_wordcloud(keyword_frequencies):
    # Combinar todas las palabras clave en un solo diccionario para WordCloud
    word_frequencies = Counter()
    for category_freq in keyword_frequencies.values():
        word_frequencies.update(category_freq)

    # Crear la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    wordcloud.generate_from_frequencies(word_frequencies)
    
    # Guardar y mostrar la nube de palabras
    stats_folder = "requerimiento3&4/statistics"
    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)
    
    wordcloud_path = os.path.join(stats_folder, 'nube_palabras.png')
    wordcloud.to_file(wordcloud_path)
    
    # Mostrar la nube de palabras
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de Palabras Clave de Abstracts", fontsize=16)
    plt.show()
    print(Fore.GREEN + f"Nube de palabras guardada en: {wordcloud_path}")

# Función para generar gráficos estadísticos por categoría
def generate_statistics_by_category(keyword_frequencies):
    # Crear la carpeta "statistics" dentro de "requerimiento3&4" si no existe
    stats_folder = "requerimiento3&4/statistics"
    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)
    
    # Colores para cada categoría
    category_colors = [
        '#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1', '#955251',
        '#B565A7', '#009B77', '#DD4124', '#45B8AC', '#EFC050', '#5B5EA6'
    ]
    
    # Crear y guardar un gráfico de barras para cada categoría
    for idx, (category, frequencies) in enumerate(keyword_frequencies.items()):
        df_category = pd.DataFrame(frequencies.items(), columns=["Variable", "Frecuencia"])
        df_category = df_category.sort_values(by="Frecuencia", ascending=False)
        
        # Seleccionar color específico para la categoría
        color = category_colors[idx % len(category_colors)]

        # Generar el gráfico de barras
        plt.figure(figsize=(12, 6))
        plt.barh(df_category["Variable"], df_category["Frecuencia"], color=color)
        plt.gca().invert_yaxis()  # Invertir el eje Y para que los más frecuentes estén arriba
        plt.xlabel('Frecuencia', fontsize=12, weight='bold')
        plt.ylabel('Variables', fontsize=12, weight='bold')
        plt.title(f'Frecuencia de Variables en la Categoría: {category}', fontsize=14, weight='bold', color=color)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Guardar el gráfico para cada categoría
        plt.savefig(f"{stats_folder}/frecuencia_{category.replace(' ', '_')}.png", bbox_inches='tight', dpi=150)
        plt.close()
        print(Fore.GREEN + f"Gráfico de frecuencia de '{category}' guardado en {stats_folder}")

# Función para imprimir el conteo final de palabras
def print_final_count(keyword_frequencies):
    print_title("Conteo Final de Palabras por Categoría")
    for category, frequencies in keyword_frequencies.items():
        print(Fore.CYAN + f"\nCategoría: {category}")
        for keyword, count in frequencies.items():
            print(Fore.YELLOW + f" - {keyword}: {count}")

# Cargar el archivo de categorías
categories_filepath = 'requerimiento3&4/CategoríaVariables.txt'
categories = load_categories_from_file(categories_filepath)

# Cargar el archivo CSV con los abstracts
file_path = 'DataFinal/combined_datafinal.csv'
df = pd.read_csv(file_path)

# Imprimir el título en la terminal
print_title("Conteo de Palabras según Abstract")

# Procesar los abstracts y generar las frecuencias
keyword_frequencies = count_keywords_in_abstracts(df, categories)

# Generar la única nube de palabras y los gráficos de barras por categoría
generate_wordcloud(keyword_frequencies)
generate_statistics_by_category(keyword_frequencies)

# Imprimir el conteo final de palabras por categoría
print_final_count(keyword_frequencies)

# Mostrar mensaje final en la terminal
print(Fore.GREEN + "Estadísticas y nube de palabras generadas en 'requerimiento3&4/statistics'")
