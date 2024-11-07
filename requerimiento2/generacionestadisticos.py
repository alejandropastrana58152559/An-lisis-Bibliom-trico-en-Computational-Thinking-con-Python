import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from colorama import Fore, Style
import seaborn as sns
import warnings
import re

# Desactivar todos los warnings de matplotlib
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
warnings.filterwarnings('ignore', category=DeprecationWarning, module='matplotlib')
warnings.filterwarnings('ignore', category=FutureWarning, module='matplotlib')

# Configuración de estilo de Seaborn para gráficos
sns.set_style("whitegrid")

def print_title(title):
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"  ***   {title}   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Algoritmo para generar estadísticas
def generate_statistics(df, stat_type):
    statistics_dir = 'requerimiento2/statistics'
    create_directory(statistics_dir)

    print_title("Generador de Estadísticos .png")

    color_palettes = {
        'Autores más citados': 'coolwarm',
        'Publicaciones por Año': 'rocket',
        'Tipo de Producto': 'pastel',
        'Afiliación de Autores': 'viridis',
        'Análisis por Journal': 'mako',
        'Base de Datos vs. Autor': 'flare',
        'Artículos por Journal': 'crest',
        'Publicaciones por Año y Base de Datos': 'ch:s=.25,rot=-.25',
        'Top 10 Palabras Clave por Año': 'tab20'
    }

    palette = color_palettes.get(stat_type, 'tab10')

    if stat_type == 'Autores más citados':
        df_filtered = df[df['Autor'] != 'Sin Valor']
        author_counts = df_filtered['Autor'].value_counts().head(15)

        with tqdm(total=100, desc="Generando estadístico de autores más citados", unit="step") as pbar:
            plt.figure(figsize=(10, 6))
            author_counts.plot(kind='bar', color=sns.color_palette(palette, len(author_counts)))
            plt.title('Top 15 Autores Más Citados', fontsize=14, color='darkblue', weight='bold')
            plt.xlabel('Autor', fontsize=12, color='grey')
            plt.ylabel('Cantidad de Citas', fontsize=12, color='grey')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/autores_mas_citados.png', bbox_inches='tight', dpi=150)
            plt.close()
            pbar.update(100)

    elif stat_type == 'Publicaciones por Año':
        df_filtered = df[df['Year'] != 'Sin Valor']
        year_counts = df_filtered['Year'].value_counts().sort_index()

        with tqdm(total=100, desc="Generando estadístico de publicaciones por año", unit="step") as pbar:
            plt.figure(figsize=(10, 6))
            year_counts.plot(kind='bar', color=sns.color_palette(palette, len(year_counts)))
            plt.title('Publicaciones por Año', fontsize=14, color='darkblue', weight='bold')
            plt.xlabel('Año', fontsize=12, color='grey')
            plt.ylabel('Cantidad de Publicaciones', fontsize=12, color='grey')
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/publicaciones_por_anio.png', bbox_inches='tight', dpi=150)
            plt.close()
            pbar.update(100)

    elif stat_type == 'Tipo de Producto':
        df_filtered = df[df['Database'] != 'Sin Valor']
        product_type_counts = df_filtered['Database'].value_counts()

        with tqdm(total=100, desc="Generando estadístico de tipo de producto", unit="step") as pbar:
            plt.figure(figsize=(8, 8))
            product_type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette(palette, len(product_type_counts)))
            plt.title('Distribución de Productos por Tipo', fontsize=14, color='darkblue', weight='bold')
            plt.ylabel('')
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/tipo_de_producto.png', bbox_inches='tight', dpi=150)
            plt.close()
            pbar.update(100)

    elif stat_type == 'Afiliación de Autores':
        df_filtered = df[df['Publisher'] != 'Sin Valor']
        affiliation_counts = df_filtered['Publisher'].value_counts().head(15)

        with tqdm(total=100, desc="Generando estadístico de afiliación de autores", unit="step") as pbar:
            plt.figure(figsize=(10, 6))
            affiliation_counts.plot(kind='bar', color=sns.color_palette(palette, len(affiliation_counts)))
            plt.title('Publicaciones por Institución', fontsize=14, color='darkblue', weight='bold')
            plt.xlabel('Institución', fontsize=12, color='grey')
            plt.ylabel('Cantidad de Publicaciones', fontsize=12, color='grey')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/afiliacion_autores.png', bbox_inches='tight', dpi=150)
            plt.close()
            pbar.update(100)

    elif stat_type == 'Análisis por Journal':
        df_filtered = df[df['Publication Title'] != 'Sin Valor']
        journal_counts = df_filtered['Publication Title'].value_counts().head(15)

        with tqdm(total=100, desc="Generando estadístico de análisis por journal", unit="step") as pbar:
            plt.figure(figsize=(10, 6))
            journal_counts.plot(kind='bar', color=sns.color_palette(palette, len(journal_counts)))
            plt.title('Publicaciones por Journal', fontsize=14, color='darkblue', weight='bold')
            plt.xlabel('Journal', fontsize=12, color='grey')
            plt.ylabel('Cantidad de Publicaciones', fontsize=12, color='grey')
            plt.xticks(rotation=45, ha='right', fontsize=9)
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/analisis_por_journal.png', bbox_inches='tight', dpi=150)
            plt.close()
            pbar.update(100)

    elif stat_type == 'Base de Datos vs. Autor':
        df_filtered = df[(df['Database'] != 'Sin Valor') & (df['Autor'] != 'Sin Valor')]
        db_author_counts = df_filtered.groupby(['Database', 'Autor']).size().unstack(fill_value=0)

        top_databases = db_author_counts.sum(axis=1).nlargest(10).index
        db_author_counts = db_author_counts.loc[top_databases, :]

        top_authors = db_author_counts.sum(axis=0).nlargest(10).index
        db_author_counts = db_author_counts.loc[:, top_authors]

        with tqdm(total=100, desc="Generando estadístico de base de datos vs. autor", unit="step") as pbar:
            plt.figure(figsize=(12, 8))
            db_author_counts.plot(kind='bar', stacked=True, colormap=palette)
            plt.title('Cantidad de Productos por Autor y Base de Datos', fontsize=14, color='darkblue', weight='bold')
            plt.xlabel('Base de Datos', fontsize=12, color='grey')
            plt.ylabel('Cantidad de Productos', fontsize=12, color='grey')
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.legend(title='Autor', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/base_datos_vs_autor.png', bbox_inches='tight', dpi=150)
            plt.close()
            pbar.update(100)

    elif stat_type == 'Artículos por Journal':
        df_filtered = df[(df['Publication Title'] != 'Sin Valor') & (df['Autor'] != 'Sin Valor')]
        journal_author_counts = df_filtered.groupby(['Publication Title', 'Autor']).size().unstack(fill_value=0)

        top_journals = journal_author_counts.sum(axis=1).nlargest(10).index
        journal_author_counts = journal_author_counts.loc[top_journals, :]

        top_authors = journal_author_counts.sum(axis=0).nlargest(10).index
        journal_author_counts = journal_author_counts.loc[:, top_authors]

        with tqdm(total=100, desc="Generando estadístico de artículos por journal", unit="step") as pbar:
            plt.figure(figsize=(12, 8))
            journal_author_counts.plot(kind='bar', stacked=True, colormap=palette)
            plt.title('Artículos por Journal y Autor', fontsize=14, color='darkblue', weight='bold')
            plt.xlabel('Journal', fontsize=12, color='grey')
            plt.ylabel('Cantidad de Artículos', fontsize=12, color='grey')
            plt.xticks(rotation=45, ha='right', fontsize=9)
            plt.legend(title='Autor', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
            plt.tight_layout()
            plt.savefig(f'{statistics_dir}/articulos_por_journal.png', bbox_inches='tight', dpi=150)
            plt.close()
            pbar.update(100)

# Cargar el archivo CSV
df = pd.read_csv('DataFinal/combined_datafinal.csv')

# Preprocesar el título de publicación para eliminar contenido no deseado
df['Publication Title'] = df['Publication Title'].str.replace(r"[,(-].*", "", regex=True).str.strip()

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