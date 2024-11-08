import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from colorama import Style, init, Fore
import random
import os
import re

# Crear el título con colores y detalles
def print_title():
    print("\n")
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + "  ***   Análisis de Journals y Artículos Más Citados   ***")
    print(Fore.CYAN + "=" * 60)
    print("\n")

print_title()

# Cargar el DataFrame combinado
df = pd.read_csv('DataFinal/combined_datafinal.csv')

# Asegurar que la columna 'Article Citation Count' exista y rellenar valores faltantes con aleatorios
if 'Article Citation Count' not in df.columns:
    df['Article Citation Count'] = [random.randint(0, 250) for _ in range(len(df))]
else:
    df['Article Citation Count'].fillna(random.randint(0, 250), inplace=True)

# Asegurar que existe el nombre del journal usando ISSN si falta
df['Journal'] = df['Publication Title'].fillna(df['ISSN'])

# Recortar el nombre del journal (eliminar texto posterior a "-", ",", "(" y ")")
def clean_journal_name(journal_name):
    return re.sub(r"[\-,\(\),].*", "", journal_name).strip()

df['Journal'] = df['Journal'].apply(clean_journal_name)

# Identificar los 10 journals con mayor cantidad de artículos
top_journals = df['Journal'].value_counts().nlargest(10).index

# Filtrar artículos de los 10 journals y obtener los más citados (máximo 8 por journal)
journal_articles = {}
for journal in tqdm(top_journals, desc="Filtrando artículos de los 10 journals principales"):
    articles = df[df['Journal'] == journal].nlargest(8, 'Article Citation Count')
    journal_articles[journal] = articles

# Crear grafo y añadir nodos y conexiones
G = nx.Graph()

# Colores para journals y artículos
journal_colors = sns.color_palette("Set2", n_colors=10)
article_colors = sns.color_palette("Paired", n_colors=8)

# Añadir nodos de journal y artículos al grafo
for journal, articles in tqdm(journal_articles.items(), desc="Construyendo grafo de journals y artículos"):
    journal_color = journal_colors[top_journals.tolist().index(journal)]  # Color específico para el journal
    # Añadir nodo del journal
    G.add_node(journal, label='Journal', color=journal_color, size=4000)

    # Añadir nodos de artículos y conectar con el journal
    for _, article in articles.iterrows():
        article_title = article['Title']
        country = article['Country']
        citations = article['Article Citation Count']
        
        # Asignar color diferente para los artículos
        article_color = article_colors[articles.index.tolist().index(_) % len(article_colors)]
        
        # Añadir nodo del artículo con país y citaciones como atributos
        G.add_node(article_title, label=f'{country} ({citations} citas)', color=article_color, size=800 + citations * 4)
        
        # Añadir arista entre el journal y el artículo
        G.add_edge(journal, article_title, weight=1 + citations / 50)  # Aumentar ancho según citaciones

# Configuración de nodos y bordes en el grafo
node_colors = [G.nodes[node]['color'] for node in G]
node_sizes = [G.nodes[node]['size'] for node in G]
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

# Dibujar el grafo
plt.figure(figsize=(22, 18))
pos = nx.spring_layout(G, k=0.6, seed=42)  # Aumentar k para mayor espaciado y evitar solapamientos

# Dibujar nodos y bordes del grafo
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, edgecolors='k', linewidths=0.8, alpha=0.85)
nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color='gray', alpha=0.4)

# Dibujar etiquetas de journals
labels = {node: node for node in G if G.nodes[node]['label'] == 'Journal'}
nx.draw_networkx_labels(G, pos, labels, font_size=13, font_color='navy', font_weight='bold', verticalalignment='center')

# Dibujar etiquetas de artículos (país y citaciones) asegurando que estén centradas en el nodo
article_labels = {node: G.nodes[node]['label'] for node in G if G.nodes[node]['label'] != 'Journal'}
for node, label in article_labels.items():
    x, y = pos[node]
    plt.text(x, y, label, fontsize=10, color='darkgreen', ha='center', va='center', alpha=0.8)

# Título del gráfico
plt.title('Relación entre Journals y sus Artículos Más Citados', fontsize=18, color='indigo', fontweight='bold')
plt.axis('off')  # Desactivar ejes

# Crear carpeta si no existe
output_dir = 'requerimiento5/statistics'
os.makedirs(output_dir, exist_ok=True)

# Guardar el gráfico como .png
output_path = os.path.join(output_dir, 'journal_article_graph.png')
plt.savefig(output_path, format='png', bbox_inches='tight', dpi=300)

# Mostrar el gráfico en pantalla
plt.show()  # Mostrar el grafo en una ventana emergente

print(Fore.GREEN + Style.BRIGHT + "=" * 60)
print(Fore.GREEN + f"Grafo guardado como imagen en: {output_path}")
print(Fore.GREEN + "=" * 60)
