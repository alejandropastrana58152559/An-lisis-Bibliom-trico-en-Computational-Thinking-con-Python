import streamlit as st
import subprocess
import os
import time
from pathlib import Path
import shutil
import pandas as pd

# Definir las rutas relativas a los scripts
scripts = {
    "Crear Base de Datos": "transform_bib_to_csv_to_combined.py",
    "Generar Estadísticos": "requerimiento2/generacionestadisticos.py",
    "Generar Grafo": "requerimiento5/journalArticuloAnalysis.py",
    "Contar Palabras Claves Abstract": "requerimiento3&4/conteoPalabrasAbstract.py"
}

# Definir los nombres de las imágenes estadísticas que se generarán
statistics_images = [
    'autores_mas_citados.png',
    'publicaciones_por_anio.png',
    'tipo_de_producto.png',
    'afiliacion_autores.png',
    'analisis_por_journal.png',
    'base_datos_vs_autor.png',
    'articulos_por_journal.png'
]

# Definir los nombres de las imágenes de conteo de palabras
wordcount_images = [
    'nube_palabras.png',
    'frecuencia_Habilidades.png',
    'frecuencia_Conceptos_Computationales.png',
    'frecuencia_Actitudes_Emocionales.png',
    'frecuencia_Propiedades_psicométricas.png',
    'frecuencia_Herramienta_de_evaluación.png',
    'frecuencia_Diseño_de_investigación.png',
    'frecuencia_Nivel_de_escolaridad.png',
    'frecuencia_Medio.png',
    'frecuencia_Estrategia.png',
    'frecuencia_Herramienta.png'
]

# Configuración de la interfaz de Streamlit
st.title('ANÁLISIS BIBLIOGRÁFICOS SOBRE "COMPUTATIONAL-THINKING" CON PYTHON')

# Área de salida de la terminal
output_area = st.empty()

# Crear columnas para organizar los botones
col1, col2 = st.columns(2)

# Mostrar los botones para ejecutar los scripts en dos columnas
for i, (button_text, script) in enumerate(scripts.items()):
    with col1 if i % 2 == 0 else col2:
        if st.button(button_text):
            with output_area:
                # Mostrar el estado de ejecución en tiempo real
                st.write(f"Ejecutando: {button_text}...")
                
                # Crear una barra de progreso
                progress_bar = st.progress(0, text="Ejecutando...")
                
                # Ejecutar el script de forma síncrona
                process = subprocess.Popen(
                    ["python", script], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True
                )
                
                # Leer la salida en tiempo real y actualizar la barra de progreso
                for line in process.stdout:
                    st.write(line.strip())
                    progress_bar.progress(1, text="Ejecutando...")

                # Esperar a que termine el proceso
                process.wait()
                
                # Notificar que la ejecución terminó
                progress_bar.progress(1, text="Ejecutado")
                st.success("Ejecución completada.")

# Sección para eliminar las imágenes generadas
if st.button("Eliminar Imágenes Generadas"):
    st.info("Eliminando imágenes generadas...")
    
    # Borrar las estadísticas generales
    statistics_path = 'requerimiento2/statistics'
    if os.path.exists(statistics_path):
        shutil.rmtree(statistics_path)
        
    # Borrar las estadísticas de conteo de palabras
    wordcount_path = 'requerimiento3&4/statistics'
    if os.path.exists(wordcount_path):
        shutil.rmtree(wordcount_path)
        
    # Borrar el grafo del requerimiento 5
    graph_path = 'requerimiento5/statistics'
    if os.path.exists(graph_path):
        shutil.rmtree(graph_path)
        
    st.success("Imágenes eliminadas correctamente. Puede volver a generar las estadísticas.")

# Sección para mostrar las estadísticas generales
st.header("Estadísticas Generales")

# Verificar y mostrar las imágenes de estadísticas generales
statistics_path = 'requerimiento2/statistics'
if os.path.exists(statistics_path):
    tabs = st.tabs([
        "Autores", 
        "Publicaciones", 
        "Tipo Producto", 
        "Afiliaciones",
        "Journals",
        "Base vs Autor",
        "Artículos"
    ])
    
    for tab, image_name in zip(tabs, statistics_images):
        image_path = os.path.join(statistics_path, image_name)
        if os.path.exists(image_path):
            with tab:
                st.image(image_path, use_container_width=True)
                st.caption(f"Visualización: {image_name.replace('.png', '').replace('_', ' ').title()}")
else:
    st.info("No se han generado estadísticas generales aún. Por favor, haga clic en 'Generar Estadísticos' para crear las visualizaciones.")

# Sección para mostrar el grafo de journals y artículos
st.header("Análisis de Relación entre Journals y Artículos")

# Verificar y mostrar el grafo
graph_path = 'requerimiento5/statistics/journal_article_graph.png'
if os.path.exists(graph_path):
    st.image(graph_path, use_container_width=True)
    st.caption("Grafo de relación entre Journals y sus Artículos más citados")
else:
    st.info("No se ha generado el grafo aún. Por favor, haga clic en 'Generar Grafo' para crear la visualización.")

# Sección para mostrar las estadísticas de conteo de palabras
st.header("Análisis de Palabras Clave")

# Verificar y mostrar las imágenes de conteo de palabras
wordcount_path = 'requerimiento3&4/statistics'
if os.path.exists(wordcount_path):
    # Crear dos columnas para la nube de palabras
    col1, col2 = st.columns([1, 1])
    
    # Mostrar la nube de palabras en la primera columna
    nube_path = os.path.join(wordcount_path, 'nube_palabras.png')
    if os.path.exists(nube_path):
        with col1:
            st.subheader("Nube de Palabras Global")
            st.image(nube_path, use_container_width=True)
    
    # Crear pestañas para las categorías
    categoria_tabs = st.tabs([
        "Habilidades",
        "Conceptos Computacionales",
        "Actitudes Emocionales",
        "Propiedades Psicométricas",
        "Herramientas de Evaluación",
        "Diseño de Investigación",
        "Nivel de Escolaridad",
        "Medio",
        "Estrategia",
        "Herramienta"
    ])
    
    # Lista de nombres de archivo sin 'nube_palabras.png'
    categoria_images = [img for img in wordcount_images if img != 'nube_palabras.png']
    
    # Mostrar cada gráfico en su pestaña correspondiente
    for tab, image_name in zip(categoria_tabs, categoria_images):
        image_path = os.path.join(wordcount_path, image_name)
        if os.path.exists(image_path):
            with tab:
                st.image(image_path, use_container_width=True)
                st.caption(f"Frecuencia de palabras en: {image_name.replace('frecuencia_', '').replace('.png', '').replace('_', ' ')}")
else:
    st.info("No se han generado estadísticas de palabras clave aún. Por favor, haga clic en 'Contar Palabras Claves Abstract' para crear las visualizaciones.")

# Sección para mostrar el archivo CSV
st.header("Archivo CSV")
csv_path = "DataFinal/combined_datafinal.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.download_button(
        label="Descargar CSV",
        data=df.to_csv(index=False),
        file_name="combined_datafinal.csv",
        mime="text/csv",
    )
    st.write("Puede visualizar el archivo CSV a continuación:")
    st.dataframe(df)
else:
    st.info("El archivo CSV aún no se ha generado. Por favor, haga clic en 'Crear Base de Datos' para generar el archivo.")