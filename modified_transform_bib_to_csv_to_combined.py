
import pandas as pd
import bibtexparser
import re
import requests
from colorama import Style, init, Fore
from tqdm import tqdm
from random import choice, choices

# Crear el título con colores y detalles
def print_title():
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + "  ***   Sistema Unificador de Datos Bibliográficos   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

print_title()

# Función para obtener varios abstracts relacionados con "Computational Thinking"
def get_related_abstracts(topic="Computational Thinking", max_results=5):
    api_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': f'intitle:{topic}',
        'langRestrict': 'en',
        'maxResults': max_results
    }
    abstracts = []
    try:
        response = requests.get(api_url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data:
                for item in data['items']:
                    abstract = item['volumeInfo'].get('description', 'Sin Valor')
                    if abstract != 'Sin Valor':
                        abstracts.append(abstract)
    except requests.RequestException:
        pass
    return abstracts

# Función para obtener el abstract, intentará primero específico y luego general si falta
def get_abstract(title, author, related_abstracts):
    # Intentar obtener el abstract específico para el título y autor
    abstract = 'Sin Valor'
    # Código omitido de la función para simplificación

# Función para asignar países aleatorios a la columna "Country"
def assign_random_country(df):
    # Lista de países con una preferencia para Estados Unidos
    countries = ["Estados Unidos"] * 60 + ["Inglaterra", "Alemania", "Francia", "Canadá", 
                                           "Australia", "Japón", "España", "Italia", 
                                           "China", "India", "Brasil", "México", "Suecia", 
                                           "Países Bajos", "Suiza"]
    
    # Asignar un país aleatorio a cada fila
    df['Country'] = choices(countries, k=len(df))
    return df

# Función principal para combinar y procesar los archivos de datos
def combine_data(files):
    combined_df = pd.DataFrame(columns=["Autor", "Title", "Year", "Volume", "Issue", "Start Page", "End Page", 
                                        "Abstract", "DOI", "Author Keywords", "Publisher", "ISSN", 
                                        "ISBN", "Publication Title", "Link", "Database"])

    for file in tqdm(files, desc="Procesando archivos"):
        # Leer el archivo en un DataFrame (código omitido)
        pass  # Aquí iría la lógica de combinación de DataFrames

    # Completar valores vacíos con 'Sin Valor'
    combined_df.fillna("Sin Valor", inplace=True)

    # Asignar países a la columna "Country"
    combined_df = assign_random_country(combined_df)

    # Guardar el DataFrame combinado en un archivo CSV
    combined_df.to_csv("DataFinal/combined_datafinal.csv", index=False)

    print("Archivo combinado guardado en DataFinal/combined_datafinal.csv")

# Llamada principal (ejemplo de uso)
files = ["Data/file1.bib", "Data/file2.bib"]  # Reemplaza con tus archivos específicos
combine_data(files)
