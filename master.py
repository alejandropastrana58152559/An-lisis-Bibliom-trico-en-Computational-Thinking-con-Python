import streamlit as st
import subprocess
import os
import time
from pathlib import Path

# Definir las rutas relativas a los scripts
scripts = {
    "Crear Base de Datos": "transform_bib_to_csv_to_combined.py",
    "Generar Estadísticos": "requerimiento2/generacionestadisticos.py",
    "Generar Grafo": "requerimiento5/journalArticuloAnalysis.py",
    "Contar Palabras Claves Abstract": "requerimiento3&4/conteoPalabrasAbstract.py"
}

# Ruta donde se almacenan las imágenes generadas
statistics_path = 'statistics/'

# Configuración de la interfaz de Streamlit
st.title("Ejecutar Algoritmos y Visualizar Resultados")

# Área de salida de la terminal
output_area = st.empty()

# Mostrar los botones para ejecutar los scripts
for button_text, script in scripts.items():
    if st.button(button_text):
        with output_area:
            # Mostrar el estado de ejecución en tiempo real
            st.write(f"Ejecutando: {button_text}...")
            
            # Ejecutar el script de forma síncrona
            process = subprocess.Popen(
                ["python", script], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            
            # Leer la salida en tiempo real
            for line in process.stdout:
                st.write(line.strip())  # Mostrar la salida en el área de texto

            # Esperar a que termine el proceso
            process.wait()
            
            # Mostrar el resultado (gráficas generadas)
            time.sleep(2)  # Esperar un momento para asegurarse que las imágenes se hayan guardado
            
            # Mostrar las imágenes generadas
            for image_file in Path(statistics_path).glob("*.png"):
                st.image(image_file, caption=image_file.name, use_column_width=True)

# Notificar que la ejecución terminó
st.success("Ejecución completada. Imágenes y resultados generados.")


