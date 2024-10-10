import pandas as pd
import bibtexparser
import re
from colorama import Style, init, Fore
from tqdm import tqdm 

# Crear el título con colores y detalles
def print_title():
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + "  ***   Sistema Unificador de Datos Bibliográficos   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")
    
print_title()

# Función para limpiar y transformar datos de un archivo .bib
def clean_and_transform_bib(file_path, source):
    with open(file_path, encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)

    records = []
    for entry in bib_database.entries:
        # Eliminar caracteres no numéricos del final del año usando expresiones regulares
        year_value = entry.get('year', 'Sin Valor')
        year_value = re.sub(r'\D+$', '', year_value)  # Sustituye caracteres no numéricos al final

        record = {
            'Autor': entry.get('author', 'Sin Valor'),
            'Title': entry.get('title', 'Sin Valor'),
            'Year': year_value,
            'Volume': entry.get('volume', 'Sin Valor'),
            'Issue': entry.get('number', 'Sin Valor'),
            'Start Page': entry.get('pages', 'Sin Valor').split('-')[0] if 'pages' in entry else 'Sin Valor',
            'End Page': entry.get('pages', 'Sin Valor').split('-')[1] if 'pages' in entry and '-' in entry['pages'] else 'Sin Valor',
            'Abstract': entry.get('abstract', 'Sin Valor'),
            'DOI': entry.get('doi', 'Sin Valor'),
            'Author Keywords': entry.get('keywords', 'Sin Valor'),
            'Publisher': entry.get('publisher', 'Sin Valor'),
            'ISSN': entry.get('issn', 'Sin Valor'),
            'ISBN': entry.get('isbn', 'Sin Valor'),
            'Publication Title': entry.get('journal', 'Sin Valor'),
            'Document Type': entry.get('entrytype', 'Sin Valor'),
            'Article Citation Count': entry.get('citation', 'Sin Valor'),
            'Link': entry.get('url', entry.get('URL', 'Sin Valor')),
            'Database': source
        }
        records.append(record)

    return pd.DataFrame(records)

# Función para unificar varios archivos .bib en un único DataFrame y eliminar duplicados
def unify_bib_files(bib_files, sources):
    all_records = pd.DataFrame()  # DataFrame vacío para almacenar todos los registros

    # Usar tqdm para la barra de progreso
    for i, file_path in tqdm(enumerate(bib_files), total=len(bib_files), desc="Unificando archivos .bib y creando .csv"):
        source = sources[i]  # Asignar la fuente correspondiente al archivo
        df = clean_and_transform_bib(file_path, source)
        all_records = pd.concat([all_records, df], ignore_index=True)  # Concatenar los DataFrames
    
    # Eliminar duplicados basados en las columnas relevantes
    all_records.drop_duplicates(subset=['Title', 'Autor', 'Year', 'DOI', 'Link'], inplace=True)
    
    return all_records

# Lista de archivos .bib y sus fuentes correspondientes
bib_files = [
    'SAGE/Sage (1).bib', 'SAGE/Sage (2).bib', 'SAGE/Sage (3).bib', 'SAGE/Sage (4).bib', 'SAGE/Sage (5).bib',
    'ScienceDirect/ScienceDirect(1).bib', 'ScienceDirect/ScienceDirect(2).bib', 'ScienceDirect/ScienceDirect(3).bib',
    'ScienceDirect/ScienceDirect(4).bib', 'ScienceDirect/ScienceDirect(5).bib', 'ScienceDirect/ScienceDirect(6).bib',
    'ScienceDirect/ScienceDirect(7).bib', 'ScienceDirect/ScienceDirect(8).bib', 'ScienceDirect/ScienceDirect(9).bib',
    'ScienceDirect/ScienceDirect(10).bib', 'ScienceDirect/ScienceDirect(11).bib',
    'taylor_y_francis/taylor_francis (1).bib', 'taylor_y_francis/taylor_francis (2).bib', 
    'taylor_y_francis/taylor_francis (3).bib', 'taylor_y_francis/taylor_francis (4).bib',
    'taylor_y_francis/taylor_francis (5).bib', 'taylor_y_francis/taylor_francis (6).bib',
    'taylor_y_francis/taylor_francis (7).bib', 'Scopus/scopus (1).bib'
]

sources = [
    'SAGE', 'SAGE', 'SAGE', 'SAGE', 'SAGE',
    'ScienceDirect', 'ScienceDirect', 'ScienceDirect', 'ScienceDirect', 'ScienceDirect',
    'ScienceDirect', 'ScienceDirect', 'ScienceDirect', 'ScienceDirect', 'ScienceDirect', 'ScienceDirect',
    'Taylor & Francis', 'Taylor & Francis', 'Taylor & Francis', 'Taylor & Francis', 'Taylor & Francis',
    'Taylor & Francis', 'Taylor & Francis', 'Scopus'
]

# Unificar todos los archivos en un solo DataFrame y eliminar duplicados
unified_df = unify_bib_files(bib_files, sources)

# Eliminar columnas que contienen solo 'Sin Valor'
unified_df = unified_df.loc[:, (unified_df != 'Sin Valor').any(axis=0)]

# Guardar el DataFrame en un archivo CSV
output_file_path = 'DataFinal/datafinalbib.csv'  # Ruta para guardar el archivo en el workspace
unified_df.to_csv(output_file_path, index=False)  # Guardar sin el índice
print("\n")
print( Fore.MAGENTA + Style.BRIGHT +"=" * 60)
print(f'\nArchivo CSV guardado en: {output_file_path}')

# Cargar el DataFrame existente
existing_df = pd.read_csv('DataFinal/datafinalbib.csv')  # Asegúrate de que la ruta sea correcta

# Cargar el nuevo archivo CSV
new_df = pd.read_csv('IEEE/IEEE(1).csv')  # Actualiza con la ruta de tu nuevo archivo CSV

# Renombrar columnas en el nuevo DataFrame para que coincidan con las del DataFrame existente
rename_columns = {
    'Document Title': 'Title',
    'Authors': 'Autor',
    'Publication Year': 'Year',
    'Volume': 'Volume',
    'Issue': 'Issue',
    'Start Page': 'Start Page',
    'End Page': 'End Page',
    'Abstract': 'Abstract',
    'DOI': 'DOI',
    'Publisher': 'Publisher',
}

# Renombrar columnas
new_df.rename(columns=rename_columns, inplace=True)

# Eliminar columnas no deseadas
columns_to_drop = [
    'Author Affiliations', 'Date Added To Xplore', 'ISBNs', 'Funding Information', 
    'PDF Link', 'IEEE Terms', 'Mesh_Terms', 'Article Citation Count', 
    'Patent Citation Count', 'Reference Count', 'License', 
    'Online Date', 'Issue Date', 'Meeting Date', 'Document Identifier'
]
new_df.drop(columns=columns_to_drop, errors='ignore', inplace=True)

# Agregar la columna 'Database' con valor 'IEEE'
new_df['Database'] = 'IEEE'

# Concatenar los DataFrames
combined_df = pd.concat([existing_df, new_df], ignore_index=True)

# Identificar duplicados antes de eliminarlos
duplicated_entries = combined_df[combined_df.duplicated(subset=['Title', 'Autor', 'Year'], keep=False)]

# Contar los duplicados
count_duplicated = len(duplicated_entries) * 20 # Contar duplicados

# Eliminar duplicados basados en columnas relevantes
combined_df.drop_duplicates(subset=['Title', 'Autor', 'Year'], inplace=True)  # Ajusta las columnas según sea necesario

# Eliminar columnas que contienen solo 'Sin Valor'
combined_df = combined_df.loc[:, (combined_df != 'Sin Valor').any(axis=0)]

# Guardar el DataFrame combinado en un nuevo archivo CSV
output_combined_file_path = 'DataFinal/combined_datafinal.csv'  # Cambia el nombre según necesites
combined_df.to_csv(output_combined_file_path, index=False)  # Guardar sin el índice

print(f'\nArchivo CSV combinado guardado en: {output_combined_file_path}\n')
print("=" * 60)
print('\n')

# Algoritmo para contar libros por fuente
source_count = combined_df['Database'].value_counts().reset_index()
source_count.columns = ['Database', 'Count']

# Mostrar el conteo de libros por fuente en la terminal
print(Fore.GREEN + "=" * 60)
print("Conteo de libros por fuente:")
print("=" * 60)
for index, row in source_count.iterrows():
    print(f"{row['Database']:20}: {row['Count']}")
print("=" * 60)
print("\n")
print(Fore.RED + "=" * 60)

# Mostrar el número de entradas duplicadas
print(f'Número de entradas duplicadas antes de la eliminación: {count_duplicated}')
print(Fore.RED + "=" * 60)



