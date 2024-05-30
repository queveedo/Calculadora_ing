import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import math
import pandas as pd
from openpyxl import Workbook
from fpdf import FPDF

# Funciones de cálculo
def calcular_pago_mensual(monto, tasa_mensual, meses):
    if tasa_mensual == 0:
        return monto / meses
    return (monto * tasa_mensual) / (1 - (1 + tasa_mensual) ** -meses)

def calcular_intereses_totales(monto, pago_mensual, meses):
    total_pagado = pago_mensual * meses
    intereses = total_pagado - monto
    return intereses

def calcular_duracion_en_meses(monto, pago_mensual, tasa_mensual):
    if tasa_mensual == 0:
        return monto / pago_mensual
    meses = -math.log(1 - (monto * tasa_mensual) / pago_mensual) / math.log(1 + tasa_mensual)
    return int(math.ceil(meses))

def generar_amortizacion(monto, tasa_mensual, meses):
    pago_mensual = calcular_pago_mensual(monto, tasa_mensual, meses)
    detalles_amortizacion = []

    saldo = monto
    for mes in range(1, meses + 1):
        interes = saldo * tasa_mensual
        principal = pago_mensual - interes
        saldo -= principal
        detalles_amortizacion.append({
            "Periodo": mes,
            "Pago": pago_mensual,
            "Interés": interes,
            "Amortización": principal,
            "Saldo Insoluto": saldo
        })

    return detalles_amortizacion

# Función para manejar los cálculos
def realizar_calculo():
    try:
        monto = float(limpiar_entrada(monto_entry.get()))
        tasa_anual = float(limpiar_entrada(tasa_entry.get()))
        pago_mensual_conocido = pago_mensual_entry.get()
        capitalizacion = capitalizacion_var.get()
        
        if tasa_anual < 0:
            raise ValueError("La tasa de interés no puede ser negativa.")

        # Ajuste de la tasa de interés de acuerdo con el periodo de capitalización
        if capitalizacion == 1:  # Mensual
            tasa_mensual = tasa_anual / 12 / 100
        elif capitalizacion == 2:  # Bimestral
            tasa_mensual = tasa_anual / 100 / 6
        elif capitalizacion == 3:  # Trimestral
            tasa_mensual = tasa_anual / 100 / 4
        elif capitalizacion == 6:  # Semestral
            tasa_mensual = tasa_anual / 100 / 2
        elif capitalizacion == 12:  # Anual
            tasa_mensual = tasa_anual

        if opcion_var.get() in (1, 2, 4):
            plazo = plazo_entry.get()
            if not plazo:
                raise ValueError("Debe ingresar un valor para el periodo.")
            plazo = int(plazo)

        resultado_label.grid_remove()  # Ocultar el label antes de realizar un nuevo cálculo

        if opcion_var.get() == 1:
            pago_mensual = calcular_pago_mensual(monto, tasa_mensual, plazo)
            resultado_text.set(f"Pago mensual: ${pago_mensual:.2f}")

        elif opcion_var.get() == 2:
            pago_mensual = calcular_pago_mensual(monto, tasa_mensual, plazo)
            total_intereses = calcular_intereses_totales(monto, pago_mensual, plazo)
            resultado_text.set(f"Total de intereses: ${total_intereses:.2f}")

        elif opcion_var.get() == 3:
            if not pago_mensual_conocido:
                raise ValueError("Debe ingresar un valor para el pago mensual.")
            pago_mensual = float(limpiar_entrada(pago_mensual_conocido))
            if pago_mensual <= 0:
                raise ValueError("El pago mensual debe ser mayor que cero.")
            meses_para_pagar = calcular_duracion_en_meses(monto, pago_mensual, tasa_mensual)
            resultado_text.set(f"Meses para pagar: {meses_para_pagar} meses")

        elif opcion_var.get() == 4:
            detalles_amortizacion = generar_amortizacion(monto, tasa_mensual, plazo)
            mostrar_amortizacion(detalles_amortizacion)

        resultado_label.grid()  # Mostrar el label después de realizar el cálculo

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except ZeroDivisionError:
        messagebox.showerror("Error", "No se puede dividir por cero. Verifique las entradas.")

# Función para mostrar la tabla de amortización en el lado derecho
def mostrar_amortizacion(detalles):
    for i in tree.get_children():
        tree.delete(i)

    for detalle in detalles:
        tree.insert("", "end", values=(detalle["Periodo"], f"${detalle['Pago']:.2f}", f"${detalle['Interés']:.2f}", f"${detalle['Amortización']:.2f}", f"${detalle['Saldo Insoluto']:.2f}"))

# Función para limpiar valores de entrada
def limpiar_entrada(valor):
    return valor.replace(',', '').replace(' ', '')

# Función para habilitar o deshabilitar campos de entrada
def actualizar_campos():
    if opcion_var.get() == 3:
        plazo_entry.config(state='disabled')
        pago_mensual_entry.config(state='normal')
    else:
        plazo_entry.config(state='normal')
        pago_mensual_entry.config(state='disabled')

# Función para exportar la tabla a Excel
def exportar_excel():
    detalles = [tree.item(item)["values"] for item in tree.get_children()]
    df = pd.DataFrame(detalles, columns=["Periodo", "Pago", "Interés", "Amortización", "Saldo Insoluto"])
    
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Éxito", f"Archivo Excel guardado en: {file_path}")

# Función para exportar la tabla a PDF
def exportar_pdf():
    detalles = [tree.item(item)["values"] for item in tree.get_children()]
    
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        col_width = pdf.w / 5.5
        row_height = pdf.font_size * 1.5
        
        for row in [["Periodo", "Pago", "Interés", "Amortización", "Saldo Insoluto"]] + detalles:
            for item in row:
                pdf.cell(col_width, row_height, txt=str(item), border=1)
            pdf.ln(row_height)
        
        pdf.output(file_path)
        messagebox.showinfo("Éxito", f"Archivo PDF guardado en: {file_path}")

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Calculadora de Amortización")
ventana.geometry("900x600")  # Dimensiones iniciales, se ajustará automáticamente

estilo = ttk.Style()
estilo.theme_use('clam')

# Estilo personalizado
estilo.configure("TFrame", background="#E8E8E8")
estilo.configure("TLabel", background="#E8E8E8", font=("Helvetica", 12))
estilo.configure("TButton", background="#007ACC", foreground="white", font=("Helvetica", 12, "bold"))
estilo.configure("TRadiobutton", background="#E8E8E8", font=("Helvetica", 12))
estilo.configure("Treeview", font=("Helvetica", 10))
estilo.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#007ACC", foreground="white")

# Variables
opcion_var = tk.IntVar(value=1)
capitalizacion_var = tk.IntVar(value=1)
resultado_text = tk.StringVar()

# Contenedor principal
frame = ttk.Frame(ventana, padding="10")
frame.grid(row=0, column=0, sticky="nsew")

# Configurar la redimensión de las filas y columnas
ventana.grid_rowconfigure(0, weight=1)
ventana.grid_columnconfigure(0, weight=1)

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=3)  # Dar más peso a la columna derecha

# Frame izquierdo
frame_izquierdo = ttk.Frame(frame, padding="10")
frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Frame derecho
frame_derecho = ttk.Frame(frame, padding="10")
frame_derecho.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Configuración de filas y columnas internas
frame_izquierdo.grid_rowconfigure(14, weight=1)
frame_derecho.grid_rowconfigure(0, weight=1)
frame_derecho.grid_columnconfigure(0, weight=1)

# Componentes del frame izquierdo
ttk.Label(frame_izquierdo, text="Monto del préstamo:").grid(row=0, column=0, sticky="w", pady=2)
monto_entry = ttk.Entry(frame_izquierdo)
monto_entry.grid(row=0, column=1, sticky="ew", pady=2)

ttk.Label(frame_izquierdo, text="Tasa de interés anual (%):").grid(row=1, column=0, sticky="w", pady=2)
tasa_entry = ttk.Entry(frame_izquierdo)
tasa_entry.grid(row=1, column=1, sticky="ew", pady=2)

ttk.Label(frame_izquierdo, text="Periodo de capitalización:").grid(row=2, column=0, sticky="w", pady=2)
capitalizacion_frame = ttk.Frame(frame_izquierdo)
capitalizacion_frame.grid(row=2, column=1, sticky="w", pady=2)
ttk.Radiobutton(capitalizacion_frame, text="Mensual", variable=capitalizacion_var, value=1).pack(side="left")
ttk.Radiobutton(capitalizacion_frame, text="Bimestral", variable=capitalizacion_var, value=2).pack(side="left")
ttk.Radiobutton(capitalizacion_frame, text="Trimestral", variable=capitalizacion_var, value=3).pack(side="left")
ttk.Radiobutton(capitalizacion_frame, text="Semestral", variable=capitalizacion_var, value=6).pack(side="left")
ttk.Radiobutton(capitalizacion_frame, text="Anual", variable=capitalizacion_var, value=12).pack(side="left")

ttk.Label(frame_izquierdo, text="Seleccione una opción:").grid(row=3, column=0, sticky="w", pady=2)
opciones_frame = ttk.Frame(frame_izquierdo)
opciones_frame.grid(row=3, column=1, sticky="w", pady=2)
ttk.Radiobutton(opciones_frame, text="Calcular pago mensual", variable=opcion_var, value=1, command=actualizar_campos).pack(anchor="w")
ttk.Radiobutton(opciones_frame, text="Calcular intereses totales", variable=opcion_var, value=2, command=actualizar_campos).pack(anchor="w")
ttk.Radiobutton(opciones_frame, text="Calcular duración del préstamo", variable=opcion_var, value=3, command=actualizar_campos).pack(anchor="w")
ttk.Radiobutton(opciones_frame, text="Generar tabla de amortización", variable=opcion_var, value=4, command=actualizar_campos).pack(anchor="w")

ttk.Label(frame_izquierdo, text="Periodo (meses):").grid(row=4, column=0, sticky="w", pady=2)
plazo_entry = ttk.Entry(frame_izquierdo)
plazo_entry.grid(row=4, column=1, sticky="ew", pady=2)

ttk.Label(frame_izquierdo, text="Renta (Si conoce su valor):").grid(row=5, column=0, sticky="w", pady=2)
pago_mensual_entry = ttk.Entry(frame_izquierdo, state="disabled")
pago_mensual_entry.grid(row=5, column=1, sticky="ew", pady=2)

ttk.Button(frame_izquierdo, text="Calcular", command=realizar_calculo).grid(row=6, column=0, columnspan=2, pady=10)

# Resultado
resultado_label = ttk.Label(frame_izquierdo, textvariable=resultado_text, font=("Helvetica", 12, "bold"))
resultado_label.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)
resultado_label.grid_remove()  # Inicialmente oculto

# Componentes del frame derecho (tabla de amortización)
columnas = ("Periodo", "Pago", "Interés", "Amortización", "Saldo Insoluto")
tree = ttk.Treeview(frame_derecho, columns=columnas, show="headings")
for col in columnas:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)  # Ajustar el ancho de las columnas

tree.grid(row=0, column=0, sticky="nsew")

# Botones de exportación
botones_frame = ttk.Frame(frame_derecho)
botones_frame.grid(row=1, column=0, pady=10)

ttk.Button(botones_frame, text="Exportar a Excel", command=exportar_excel).grid(row=0, column=0, padx=5)
ttk.Button(botones_frame, text="Exportar a PDF", command=exportar_pdf).grid(row=0, column=1, padx=5)

# Ejecutar aplicación
ventana.mainloop()
