import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter, defaultdict
import re
from tqdm import tqdm
from colorama import Fore, Style, init
import seaborn as sns

# Inicializar colorama y configurar el estilo de seaborn
init(autoreset=True)
sns.set(style="whitegrid", palette="muted")

# Función para cargar categorías y variables desde el archivo de texto
def load_categories_from_file(filepath):
    categories = defaultdict(list)
    with open(filepath, 'r', encoding='utf-8') as file:
        current_category = None
        for line in file:
            line = line.strip()
            if line.lower().startswith("categoría:") or line.lower().startswith("categoria:"):
                current_category = line.split(":")[1].strip()
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
    keyword_frequencies = {category: Counter() for category in categories}
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc=Fore.GREEN + "Procesando abstracts", unit="step"):
        abstract = str(row['Abstract']).lower()
        
        for category, keywords in categories.items():
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if '-' in keyword:
                    unified_keyword = keyword.split('-')[0].lower()
                else:
                    unified_keyword = keyword_lower

                if re.search(r'\b' + re.escape(unified_keyword) + r'\b', abstract):
                    keyword_frequencies[category][unified_keyword] += 1

    return keyword_frequencies

# Función para generar una única nube de palabras
def generate_wordcloud(keyword_frequencies):
    word_frequencies = Counter()
    for category_freq in keyword_frequencies.values():
        word_frequencies.update(category_freq)

    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    wordcloud.generate_from_frequencies(word_frequencies)
    
    stats_folder = "requerimiento3&4/statistics"
    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)
    
    wordcloud_path = os.path.join(stats_folder, 'nube_palabras.png')
    wordcloud.to_file(wordcloud_path)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de Palabras Clave de Abstracts", fontsize=16)
    plt.show()
    print(Fore.GREEN + f"Nube de palabras guardada en: {wordcloud_path}")

# Función para generar gráficos estadísticos por categoría con dis eño Seaborn
def generate_statistics_by_category(keyword_frequencies):
    stats_folder = "requerimiento3&4/statistics"
    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)

    sns.set_palette("Spectral")

    for idx, (category, frequencies) in enumerate(keyword_frequencies.items()):
        df_category = pd.DataFrame(frequencies.items(), columns=["Variable", "Frecuencia"])
        df_category = df_category.sort_values(by="Frecuencia", ascending=False)

        plt.figure(figsize=(12, 6))
        sns.barplot(x="Frecuencia", y="Variable", data=df_category, palette="coolwarm", edgecolor="black")
        
        plt.gca().invert_yaxis()
        plt.xlabel('Frecuencia', fontsize=12, color='darkblue', weight='bold')
        plt.ylabel('Variables', fontsize=12, color='darkblue', weight='bold')
        plt.title(f'Frecuencia de Variables en la Categoría: {category}', fontsize=14, weight='bold', color='darkblue')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
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
