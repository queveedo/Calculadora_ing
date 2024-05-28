import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def convertir_tasa(tasa, frecuencia):
    if frecuencia == "Mensual":
        tasa_anual = (1 + tasa) ** 12 - 1
    elif frecuencia == "Bimestral":
        tasa_anual = (1 + tasa) ** 6 - 1
    elif frecuencia == "Trimestral":
        tasa_anual = (1 + tasa) ** 4 - 1
    elif frecuencia == "Cuatrimestral":
        tasa_anual = (1 + tasa) ** 3 - 1
    elif frecuencia == "Semestral":
        tasa_anual = (1 + tasa) ** 2 - 1
    elif frecuencia == "Anual":
        tasa_anual = tasa
    elif frecuencia =="Bimensual":
        tasa_anual = (1 + tasa) ** 24 -1
    else:
        raise ValueError("Frecuencia no reconocida")
    return tasa_anual

def calcular_anualidad_vencida(pago, tasa, periodos):
    valor_presente = pago * ((1 - (1 + tasa) ** -periodos) / tasa)
    valor_futuro = pago * (((1 + tasa) ** periodos - 1) / tasa)
    return valor_presente, valor_futuro

def calcular_anualidad_anticipada(pago, tasa, periodos):
    valor_presente = pago * ((1 - (1 + tasa) ** -periodos) / tasa) * (1 + tasa)
    valor_futuro = pago * (((1 + tasa) ** periodos - 1) / tasa) * (1 + tasa)
    return valor_presente, valor_futuro

def calcular_anualidad_perpetua(pago, tasa):
    valor_presente = pago / tasa
    return valor_presente

def calcular_anualidad_diferida(pago, tasa, periodos_diferidos, periodos_anualidad):
    valor_presente_vencida = pago * ((1 - (1 + tasa) ** -periodos_anualidad) / tasa)
    valor_presente_diferida = valor_presente_vencida / ((1 + tasa) ** periodos_diferidos)
    return valor_presente_diferida

def calcular():
    try:
        pago = float(entry_pago.get())
        tasa = float(entry_tasa.get())
        periodos = int(entry_periodos.get())
        frecuencia = frecuencia_var.get()

        tasa_anual = convertir_tasa(tasa, frecuencia)

        if tipo_var.get() == 1:
            vp, vf = calcular_anualidad_vencida(pago, tasa_anual, periodos)
            resultado = f"Valor Presente de la Anualidad Vencida: {vp:.2f}\nValor Futuro de la Anualidad Vencida: {vf:.2f}"
        
        elif tipo_var.get() == 2:
            vp, vf = calcular_anualidad_anticipada(pago, tasa_anual, periodos)
            resultado = f"Valor Presente de la Anualidad Anticipada: {vp:.2f}\nValor Futuro de la Anualidad Anticipada: {vf:.2f}"
        
        elif tipo_var.get() == 3:
            vp = calcular_anualidad_perpetua(pago, tasa_anual)
            resultado = f"Valor Presente de la Anualidad Perpetua: {vp:.2f}"
        
        elif tipo_var.get() == 4:
            periodos_diferidos = int(entry_periodos_diferidos.get())
            vp = calcular_anualidad_diferida(pago, tasa_anual, periodos_diferidos, periodos)
            resultado = f"Valor Presente de la Anualidad Diferida: {vp:.2f}"
        
        else:
            resultado = "Tipo de anualidad no reconocido."

        messagebox.showinfo("Resultado", resultado)

    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce valores válidos.")

def calcular_tasa_interes():
    try:
        valor_presente = float(entry_valor_presente.get())
        pago = float(entry_pago_tasa.get())
        periodos = int(entry_periodos_tasa.get())
        tipo_interes = tipo_interes_combobox.get()

        # Definir las tasas de interés según el tipo seleccionado por el usuario
        tasas_interes = {
            "Bimensual": 24,
            "Mensual": 12,
            "Trimestral": 4,
            "Cuatrimestral": 3,
            "Bimestral": 6,
            "Semestral": 2,
            "Anual": 1
        }

        # Obtener la frecuencia de la tasa de interés seleccionada
        frecuencia = tasas_interes[tipo_interes]

        def valor_presente_anualidad(tasa):
            tasa_efectiva = (1 + tasa) ** frecuencia - 1
            return pago * ((1 - (1 + tasa_efectiva) ** -periodos) / tasa_efectiva)

        tasa_min = 0.00001
        tasa_max = 1.0
        epsilon = 1e-6

        while tasa_max - tasa_min > epsilon:
            tasa_mid = (tasa_min + tasa_max) / 2
            vp_mid = valor_presente_anualidad(tasa_mid)

            if vp_mid < valor_presente:
                tasa_max = tasa_mid
            else:
                tasa_min = tasa_mid

        tasa_interes = (tasa_min + tasa_max) / 2
        tasa_efectiva = frecuencia*((1 + tasa_interes) ** frecuencia - 1)
        resultado = f"Tasa de Interés: {tasa_efectiva:.6f}"

        messagebox.showinfo("Resultado", resultado )
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

def mostrar_calculadora_anualidades():
    frame_menu_principal.pack_forget()
    frame_tasa_interes.pack_forget()

    # Crear y mostrar la calculadora de anualidades
    frame_anualidades.pack()

    # Variables globales para los campos de entrada
    global entry_pago, entry_tasa, entry_periodos, entry_periodos_diferidos, frecuencia_var, tipo_var
    tipo_var = tk.IntVar()
    frecuencia_var = tk.StringVar(value="Anual")
    entry_pago = tk.Entry(frame_anualidades)
    entry_tasa = tk.Entry(frame_anualidades)
    entry_periodos = tk.Entry(frame_anualidades)
    entry_periodos_diferidos = tk.Entry(frame_anualidades)

    # Etiquetas y campos de entrada
    tk.Label(frame_anualidades, text="Pago periódico:").grid(row=0, column=0, sticky="e")
    entry_pago.grid(row=0, column=1)

    tk.Label(frame_anualidades, text="Tasa de interés (como decimal):").grid(row=1, column=0, sticky="e")
    entry_tasa.grid(row=1, column=1)

    tk.Label(frame_anualidades, text="Número de periodos:").grid(row=2, column=0, sticky="e")
    entry_periodos.grid(row=2, column=1)

    tk.Label(frame_anualidades, text="Número de periodos diferidos:").grid(row=3, column=0, sticky="e")
    entry_periodos_diferidos.grid(row=3, column=1)

    # Opciones de tipo de anualidad
    tk.Radiobutton(frame_anualidades, text="Anualidad Vencida", variable=tipo_var, value=1).grid(row=4, column=0, columnspan=2, sticky="w")
    tk.Radiobutton(frame_anualidades, text="Anualidad Anticipada", variable=tipo_var, value=2).grid(row=5, column=0, columnspan=2, sticky="w")
    tk.Radiobutton(frame_anualidades, text="Anualidad Perpetua", variable=tipo_var, value=3).grid(row=6, column=0, columnspan=2, sticky="w")
    tk.Radiobutton(frame_anualidades, text="Anualidad Diferida", variable=tipo_var, value=4).grid(row=7, column=0, columnspan=2, sticky="w")

    # Opciones de frecuencia de conversión de la tasa de interés
    tk.Label(frame_anualidades, text="Frecuencia de la tasa de interés:").grid(row=8, column=0, sticky="e")
    frecuencia_menu = tk.OptionMenu(frame_anualidades, frecuencia_var, "Bimensual","Mensual",  "Trimestral", "Cuatrimestral","Bimestral", "Semestral", "Anual")
    frecuencia_menu.grid(row=8, column=1, sticky="w")

    # Botón de cálculo para anualidades
    tk.Button(frame_anualidades, text="Calcular Anualidad", command=calcular).grid(row=9, column=0, columnspan=2)

    # Botón de regresar
    tk.Button(frame_anualidades, text="Regresar al Menú Principal", command=mostrar_menu_principal).grid(row=10, column=0, columnspan=2)

def mostrar_calculadora_tasa_interes():
    frame_menu_principal.pack_forget()
    frame_anualidades.pack_forget()

    # Crear y mostrar la calculadora de tasa de interés
    frame_tasa_interes.pack()

    # Variables globales para los campos de entrada
    global entry_valor_presente, entry_pago_tasa, entry_periodos_tasa, tipo_interes_combobox
    entry_valor_presente = tk.Entry(frame_tasa_interes)
    entry_pago_tasa = tk.Entry(frame_tasa_interes)
    entry_periodos_tasa = tk.Entry(frame_tasa_interes)

    # Etiquetas y campos de entrada
    tk.Label(frame_tasa_interes, text="Valor Presente:").grid(row=0, column=0, sticky="e")
    entry_valor_presente.grid(row=0, column=1)

    tk.Label(frame_tasa_interes, text="Pago Periódico:").grid(row=1, column=0, sticky="e")
    entry_pago_tasa.grid(row=1, column=1)

    tk.Label(frame_tasa_interes, text="Número de Periodos:").grid(row=2, column=0, sticky="e")
    entry_periodos_tasa.grid(row=2, column=1)

    # Menú desplegable para elegir el tipo de interés
    tk.Label(frame_tasa_interes, text="Tipo de Interés:").grid(row=3, column=0, sticky="e")
    tipos_interes = ["Bimensual","Mensual",  "Trimestral", "Cuatrimestral", "Bimestral","Semestral", "Anual"]
    tipo_interes_combobox = ttk.Combobox(frame_tasa_interes, values=tipos_interes, state="readonly")
    tipo_interes_combobox.current(0)
    tipo_interes_combobox.grid(row=3, column=1)

    # Botón de cálculo para tasa de interés
    tk.Button(frame_tasa_interes, text="Calcular Tasa de Interés", command=calcular_tasa_interes).grid(row=4, column=0, columnspan=2)

    # Botón de regresar
    tk.Button(frame_tasa_interes, text="Regresar al Menú Principal", command=mostrar_menu_principal).grid(row=5, column=0, columnspan=2)

def mostrar_menu_principal():
    frame_anualidades.pack_forget()
    frame_tasa_interes.pack_forget()

    # Crear y mostrar el menú principal
    frame_menu_principal.pack()

root = tk.Tk()
root.title("Calculadoras Financieras")
root.geometry("400x300")

frame_anualidades = tk.Frame(root)
frame_tasa_interes = tk.Frame(root)

frame_menu_principal = tk.Frame(root)
frame_menu_principal.pack()

# Botón para ir a calculadora de anualidades
tk.Button(frame_menu_principal, text="Ir a Calculadora de Anualidades", command=mostrar_calculadora_anualidades).pack()

# Botón para ir a calculadora de tasa de interés
tk.Button(frame_menu_principal, text="Ir a Calculadora de Tasa de Interés", command=mostrar_calculadora_tasa_interes).pack()

root.mainloop()