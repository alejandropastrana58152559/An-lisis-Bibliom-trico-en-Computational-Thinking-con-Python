import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from colorama import Fore, Style
import warnings

# Desactivar todos los warnings de matplotlib
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
warnings.filterwarnings('ignore', category=DeprecationWarning, module='matplotlib')
warnings.filterwarnings('ignore', category=FutureWarning, module='matplotlib')

# Función para mostrar título
def print_title(title):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   {title}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

# Función para crear la carpeta si no existe
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Algoritmo para generar estadísticas
def generate_statistics(df, stat_type):
    statistics_dir = 'requerimiento2/statistics'
    create_directory(statistics_dir)

    print_title("Generador de Estadísticos .png")

    if stat_type == 'Autores más citados':
        # Filtrar autores válidos y contar apariciones
        author_counts = df['Autor'].value_counts()
        author_counts = author_counts[author_counts.index != 'Sin Valor'].head(15)

        with tqdm(total=100, desc="Generando estadístico de autores más citados", unit="step") as pbar:
            plt.figure(figsize=(10, 6))
            author_counts.plot(kind='bar', color='skyblue')
            plt.title('Top 15 Autores Más Citados')
            plt.xlabel('Autor')
            plt.ylabel('Cantidad de Citas')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/autores_mas_citados.png')
            plt.close()
            pbar.update(100)

        print(Fore.GREEN + "Estadístico de autores más citados generado y guardado en 'statistics'")

    elif stat_type == 'Publicaciones por Año':
        # Contar publicaciones por año
        year_counts = df['Year'].value_counts().sort_index()

        with tqdm(total=100, desc="Generando estadístico de publicaciones por año", unit="step") as pbar:
            plt.figure(figsize=(10, 6))
            year_counts.plot(kind='bar', color='coral')
            plt.title('Publicaciones por Año')
            plt.xlabel('Año')
            plt.ylabel('Cantidad de Publicaciones')
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/publicaciones_por_anio.png')
            plt.close()
            pbar.update(100)

        print(Fore.GREEN + "Estadístico de publicaciones por año generado y guardado en 'statistics'")

    elif stat_type == 'Tipo de Producto':
        # Contar por tipo de producto
        product_type_counts = df['Database'].value_counts()

        with tqdm(total=100, desc="Generando estadístico de tipo de producto", unit="step") as pbar:
            plt.figure(figsize=(10, 6))
            product_type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
            plt.title('Distribución de Productos por Tipo')
            plt.ylabel('')
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/tipo_de_producto.png')
            plt.close()
            pbar.update(100)

        print(Fore.GREEN + "Estadístico de tipo de producto generado y guardado en 'statistics'")

    elif stat_type == 'Afiliación de Autores':
        # Eliminar valores 'Sin Valor' en 'Publisher'
        affiliation_counts = df['Publisher'].value_counts().drop(labels='Sin Valor').head(15)

        with tqdm(total=100, desc="Generando estadístico de afiliación de autores", unit="step") as pbar:
            plt.figure(figsize=(10, 6))
            affiliation_counts.plot(kind='bar', color='purple')
            plt.title('Publicaciones por Institución')
            plt.xlabel('Institución')
            plt.ylabel('Cantidad de Publicaciones')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/afiliacion_autores.png')
            plt.close()
            pbar.update(100)

        print(Fore.GREEN + "Estadístico de afiliación de autores generado y guardado en 'statistics'")

    elif stat_type == 'Análisis por Journal':
        # Contar artículos por journal
        journal_counts = df['Publication Title'].value_counts().head(15)

        with tqdm(total=100, desc="Generando estadístico de análisis por journal", unit="step") as pbar:
            plt.figure(figsize=(10, 6))
            journal_counts.plot(kind='bar', color='teal')
            plt.title('Publicaciones por Journal')
            plt.xlabel('Journal')
            plt.ylabel('Cantidad de Publicaciones')
            plt.xticks(rotation=45, ha='right', fontsize=9)  # Ajuste en tamaño de fuente
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/analisis_por_journal.png')
            plt.close()
            pbar.update(100)

        print(Fore.GREEN + "Estadístico de análisis por journal generado y guardado en 'statistics'")

    elif stat_type == 'Base de Datos vs. Autor':
        # Cruzar base de datos con autor
        db_author_counts = df.groupby(['Database', 'Autor']).size().unstack(fill_value=0)

        # Limitar solo a las 10 bases de datos y 10 autores más frecuentes
        top_databases = db_author_counts.sum(axis=1).nlargest(10).index
        db_author_counts = db_author_counts.loc[top_databases, :]

        # Limitar solo a los 10 autores más frecuentes para cada base de datos
        top_authors = db_author_counts.sum(axis=0).nlargest(10).index
        db_author_counts = db_author_counts.loc[:, top_authors]

        with tqdm(total=100, desc="Generando estadístico de base de datos vs. autor", unit="step") as pbar:
            plt.figure(figsize=(12, 8))  # Ajustar tamaño de la figura
            db_author_counts.plot(kind='bar', stacked=True, colormap='viridis')

            # Título y etiquetas
            plt.title('Cantidad de Productos por Autor y Base de Datos')
            plt.xlabel('Base de Datos')
            plt.ylabel('Cantidad de Productos')
            
            # Ajustar rotación de etiquetas para que no se solapen
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.yticks(fontsize=10)
            
            # Ajustar la leyenda
            plt.legend(title='Autor', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

            # Ajustar el diseño para que no se corte la imagen
            plt.tight_layout()

            # Guardar la imagen en la carpeta de estadísticas con DPI ajustado
            plt.savefig(f'{statistics_dir}/base_datos_vs_autor.png', bbox_inches='tight', dpi=150)
            plt.close()
            pbar.update(100)

    elif stat_type == 'Artículos por Journal':
        # Resumen de artículos por journal y autor
        journal_author_counts = df.groupby(['Publication Title', 'Autor']).size().unstack(fill_value=0)

        # Limitar solo a los 10 journals más frecuentes
        top_journals = journal_author_counts.sum(axis=1).nlargest(10).index
        journal_author_counts = journal_author_counts.loc[top_journals, :]

        # Limitar solo a los 10 autores más frecuentes para cada journal
        top_authors = journal_author_counts.sum(axis=0).nlargest(10).index
        journal_author_counts = journal_author_counts.loc[:, top_authors]

        with tqdm(total=100, desc="Generando estadístico de artículos por journal", unit="step") as pbar:
            plt.figure(figsize=(12, 8))  # Ajustar tamaño de la figura
            journal_author_counts.plot(kind='bar', stacked=True, colormap='plasma')

            # Título y etiquetas
            plt.title('Artículos por Journal y Autor')
            plt.xlabel('Journal')
            plt.ylabel('Cantidad de Artículos')
            
            # Ajustar rotación de etiquetas para que no se solapen
            plt.xticks(rotation=45, ha='right', fontsize=9)
            plt.yticks(fontsize=9)
            
            # Ajustar la leyenda
            plt.legend(title='Autor', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

            # Ajustar el diseño para que no se corte la imagen
            plt.tight_layout()

            # Guardar la imagen en la carpeta de estadísticas con DPI ajustado
            plt.savefig(f'{statistics_dir}/articulos_por_journal.png', bbox_inches='tight', dpi=150)
            plt.close()
            pbar.update(100)

        print(Fore.GREEN + "Estadístico de artículos por journal generado y guardado en 'statistics'")


# Cargar el archivo CSV
df = pd.read_csv('DataFinal/combined_datafinal.csv')

# Generar todas las estadísticas solicitadas
statistics_to_generate = [
    'Autores más citados',
    'Publicaciones por Año',
    'Tipo de Producto',
    'Afiliación de Autores',
    'Análisis por Journal',
    'Base de Datos vs. Autor',
    'Artículos por Journal'
]

for stat in statistics_to_generate:
    generate_statistics(df, stat)