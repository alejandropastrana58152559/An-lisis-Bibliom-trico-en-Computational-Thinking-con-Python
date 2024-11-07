import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from tqdm import tqdm
from colorama import Fore, Style

# Diccionario de categorías y variables con sinónimos representados con guiones
categories = {
    "Habilidades": [
        "Abstraction", "Algorithm", "Algorithmic thinking", "Coding", "Collaboration", "Cooperation", 
        "Creativity", "Critical thinking", "Debug", "Decomposition", "Evaluation", "Generalization", 
        "Logic", "Logical thinking", "Modularity", "Patterns recognition", "Problem solving", 
        "Programming", "Representation", "Reuse", "Simulation"
    ],
    "Conceptos Computationales": [
        "Conditionals", "Control structures", "Directions", "Events", "Funtions", "Loops", 
        "Modular structure", "Parallelism", "Sequences", "Software/hardware", "Variables"
    ],
    "Actitudes Emocionales": [
        "Engagement", "Motivation", "Perceptions", "Persistence", "Self-efficacy", "Self-perceived"
    ],
    "Propiedades psicométricas": [
        "Classical Test Theory - CTT", "Confirmatory Factor Analysis - CFA", "Exploratory Factor Analysis - EFA", 
        "Item Response Theory (IRT) - IRT", "Reliability", "Structural Equation Model - SEM", "Validity"
    ],
    "Herramienta de evaluación": [
        "Beginners Computational Thinking test - BCTt", "Coding Attitudes Survey - ESCAS", "Collaborative Computing Observation Instrument",
        "Competent Computational Thinking test - cCTt", "Computational thinking skills test - CTST", 
        "Computational concepts", "Computational Thinking Assessment for Chinese Elementary Students - CTA-CES",
        "Computational Thinking Challenge - CTC", "Computational Thinking Levels Scale - CTLS", 
        "Computational Thinking Scale - CTS", "Computational Thinking Skill Levels Scale - CTS", 
        "Computational Thinking Test - CTt", "Computational Thinking Test", 
        "Computational Thinking Test for Elementary School Students - CTT-ES", 
        "Computational Thinking Test for Lower Primary - CTtLP", 
        "Computational thinking-skill tasks on numbers and arithmetic", 
        "Computerized Adaptive Programming Concepts Test - CAPCT", "CT Scale - CTS", 
        "Elementary Student Coding Attitudes Survey - ESCAS", "General self-efficacy scale", "ICT competency test", 
        "Instrument of computational identity", "KBIT fluid intelligence subtest", 
        "Mastery of computational concepts Test and an Algorithmic Test", 
        "Multidimensional 21st Century Skills Scale", "Self-efficacy scale", "STEM learning attitude scale - STEM-LAS",
        "The computational thinking scale"
    ],
    "Diseño de investigación": [
        "No experimental", "Experimental", "Longitudinal research", "Mixed methods", "Post-test", "Pre-test", "Quasi-experiments"
    ],
    "Nivel de escolaridad": [
        "Upper elementary education", "Upper elementary school", "Primary school", "Primary education", "Elementary school", 
        "Early childhood education", "Kindergarten -Preschool", "Secondary school", "Secondary education", "high school", 
        "higher education", "University", "College"
    ],
    "Medio": [
        "Block programming", "Mobile application", "Pair programming", "Plugged activities", "Programming", "Robotics", 
        "Spreadsheet", "STEM", "Unplugged activities"
    ],
    "Estrategia": [
        "Construct-by-self mind mapping - CBS-MM", "Construct-on-scaffold mind mapping - COS-MM", "Design-based learning - CTDBL", 
        "Design-based learning - DBL", "Evidence-centred design approach", "Gamification", "Reverse engineering pedagogy - REP", 
        "Technology-enhanced learning", "Collaborative learning", "Cooperative learning", "Flipped classroom", 
        "Game-based learning", "Inquiry-based learning", "Personalized learning", "Problem-based learning", 
        "Project-based learning", "Universal design for learning"
    ],
    "Herramienta": [
        "Alice", "Arduino", "Scratch", "ScratchJr", "Blockly Games", "Code.org", "Codecombat", "CSUnplugged", "Robot Turtles", 
        "Hello Ruby", "Kodable", "LightbotJr", "KIBO robots", "BEE BOT", "CUBETTO", "Minecraft", "Agent Sheets", 
        "Mimo", "Py– Learn", "SpaceChem"
    ]
}

# Función para imprimir el título con el formato solicitado
def print_title(title):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   {title}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Función para procesar los abstracts y contar las palabras clave
def count_keywords_in_abstracts(df):
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

# Generar estadísticas y gráfico
def generate_statistics(keyword_frequencies):
    # Crear la carpeta "statistics" dentro de "requerimiento3" si no existe
    stats_folder = "requerimiento3/statistics"
    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)
    
    # Crear un dataframe de frecuencias
    stats = []
    for category, frequencies in keyword_frequencies.items():
        for keyword, frequency in frequencies.items():
            stats.append([category, keyword, frequency])
    
    df_stats = pd.DataFrame(stats, columns=["Categoría", "Variable", "Frecuencia"])

    # Visualización con matplotlib
    plt.figure(figsize=(14, 8))
    for category in categories:
        subset = df_stats[df_stats["Categoría"] == category]
        plt.bar(subset["Variable"], subset["Frecuencia"], label=category)

    plt.xticks(rotation=90, ha='right', fontsize=8)
    plt.ylabel('Frecuencia')
    plt.title('Frecuencia de Variables por Categoría', fontsize=14, weight='bold')
    plt.legend(title="Categoría")
    plt.tight_layout()
    
    # Guardar el gráfico
    plt.savefig(f"{stats_folder}/frecuencia_variables_por_categoria.png", bbox_inches='tight', dpi=150)
    plt.show()

# Cargar el archivo CSV
file_path = 'DataFinal/combined_datafinal.csv'
df = pd.read_csv(file_path)

# Imprimir el título en la terminal
print_title("Conteo de Palabras según Abstract")

# Procesar los abstracts y generar las frecuencias
keyword_frequencies = count_keywords_in_abstracts(df)

# Generar el gráfico
generate_statistics(keyword_frequencies)

# Mostrar mensaje final en la terminal
print(Fore.GREEN + "Estadísticas generadas y gráfico guardado en 'requerimiento3/statistics/frecuencia_variables_por_categoria.png'")
