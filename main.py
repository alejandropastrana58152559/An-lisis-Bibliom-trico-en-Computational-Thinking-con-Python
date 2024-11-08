import os
import tkinter as tk
from tkinter import messagebox
import subprocess

# Función para ejecutar los archivos Python de los algoritmos
def ejecutar_algoritmo(archivo):
    try:
        # Ejecutar el archivo .py con subprocess
        subprocess.run(["python3", archivo], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al ejecutar {archivo}:\n{e}")
    else:
        messagebox.showinfo("Ejecución", f"Se ejecutó correctamente {archivo}")

# Función para eliminar archivos .csv y .png en las carpetas especificadas
def eliminar_archivos():
    carpetas = ["Data_Ordenamiento", "DataFinal"]  # Carpetas a revisar
    archivos_eliminados = 0

    # Recorrer las carpetas y subcarpetas
    for carpeta in carpetas:
        for root, dirs, files in os.walk(carpeta):
            for file in files:
                if file.endswith('.csv') or file.endswith('.png'):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    archivos_eliminados += 1

    if archivos_eliminados > 0:
        messagebox.showinfo("Eliminación completada", f"Se eliminaron {archivos_eliminados} archivos .csv y .png.")
    else:
        messagebox.showinfo("Eliminación completada", "No se encontraron archivos .csv o .png para eliminar.")

# Función principal para generar la interfaz gráfica
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Algoritmos de Ordenamiento")

    # Cambiar color de fondo
    ventana.configure(bg='black')
    label = tk.Label(ventana, text="Seleccione un algoritmo de ordenamiento para ejecutar:", bg='black', fg='white', font=('Arial', 12, 'bold'))
    label.pack(pady=10)

    # Nuevo botón para generar la base de datos
    btn_transform = tk.Button(ventana, text="Generar Base de Datos", command=lambda: ejecutar_algoritmo('transform_bib_to_csv_to_combined.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_transform.pack(pady=10)

    # Nuevo botón para eliminar archivos
    btn_eliminar_datos = tk.Button(ventana, text="Eliminar Datos", command=eliminar_archivos, bg='red', fg='black', relief='raised', padx=10, pady=5)
    btn_eliminar_datos.pack(pady=10)

    # Botones para cada algoritmo que llama al archivo correspondiente
    btn_binary_insertion = tk.Button(ventana, text="Binary Insertion Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_binaryInsertionSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_binary_insertion.pack(pady=5)

    btn_bitonic = tk.Button(ventana, text="Bitonic Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_bitonicSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_bitonic.pack(pady=5)

    btn_bucket = tk.Button(ventana, text="Bucket Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_bucketSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_bucket.pack(pady=5)

    btn_comb = tk.Button(ventana, text="Comb Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_combSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_comb.pack(pady=5)

    btn_gnome = tk.Button(ventana, text="Gnome Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_gnomeSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_gnome.pack(pady=5)

    btn_heap = tk.Button(ventana, text="Heap Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_HeapSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_heap.pack(pady=5)

    btn_pigeonhole = tk.Button(ventana, text="Pigeonhole Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_pigeOnHoleSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_pigeonhole.pack(pady=5)

    btn_quick = tk.Button(ventana, text="Quick Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_quickSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_quick.pack(pady=5)

    btn_radix = tk.Button(ventana, text="Radix Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_radixSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_radix.pack(pady=5)

    btn_selection = tk.Button(ventana, text="Selection Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_selectionSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_selection.pack(pady=5)

    btn_time = tk.Button(ventana, text="Time Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_timeSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_time.pack(pady=5)

    btn_tree = tk.Button(ventana, text="Tree Sort", command=lambda: ejecutar_algoritmo('Ordenamiento Python/ordenamiento_treeSort.py'), bg='gray', fg='black', relief='raised', padx=10, pady=5)
    btn_tree.pack(pady=5)

    ventana.mainloop()

# Ejecutar la interfaz
crear_interfaz()

