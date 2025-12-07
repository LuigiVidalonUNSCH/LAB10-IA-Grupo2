import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI

# --- CONFIGURA TU API KEY ---
client = OpenAI(api_key="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")

# --- CATÁLOGO DE PRODUCTOS ---
catalogo = {
    1: {
        "nombre": "Laptop Lenovo i5",
        "precio": 2300,
        "stock": 5,
        "caracteristicas": "Procesador Intel Core i5, 8GB RAM, SSD 256GB, Pantalla 15.6” Full HD"
    },
    2: {
        "nombre": "Laptop HP Ryzen 5",
        "precio": 2500,
        "stock": 4,
        "caracteristicas": "Procesador AMD Ryzen 5, 8GB RAM, SSD 512GB, Pantalla 15.6” Full HD"
    },
    3: {
        "nombre": "Mouse Logitech",
        "precio": 60,
        "stock": 20,
        "caracteristicas": "Sensor óptico, conexión inalámbrica 2.4GHz, receptor USB Nano"
    },
    4: {
        "nombre": "Teclado Mecánico RGB",
        "precio": 150,
        "stock": 12,
        "caracteristicas": "Switches mecánicos rojos, iluminación RGB, diseño ergonómico"
    },
    5: {
        "nombre": "Audífonos Sony",
        "precio": 180,
        "stock": 10,
        "caracteristicas": "Audio estéreo, cancelación pasiva de ruido, conexión 3.5mm"
    },
    6: {
        "nombre": "Monitor Samsung 24”",
        "precio": 520,
        "stock": 7,
        "caracteristicas": "Pantalla Full HD, panel IPS, 75Hz, diseño sin bordes"
    }
}

# --- FUNCIÓN PARA GENERAR RESPUESTA ---
def obtener_respuesta(mensaje_usuario):
    mensaje_limpio = mensaje_usuario.lower().strip()

    # --- RESPUESTA INMEDIATA SI DICE GRACIAS ---
    if "gracias" in mensaje_limpio or "muchas gracias" in mensaje_limpio:
        return "De nada, estamos aquí para servirte 😊"

    # Convertimos el catálogo a texto
    texto_catalogo = "\n".join([f"{prod}: S/ {precio}" for prod, precio in catalogo.items()])

    prompt_sistema = (
        "Eres un chatbot vendedor profesional. "
        "Respondes preguntas sobre catálogo, precios, productos y recomendaciones. "
        "Este es tu catálogo actual:\n\n"
        f"{texto_catalogo}\n\n"
        "Si te piden precios o productos, responde según este catálogo."
    )

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": mensaje_usuario}
        ]
    )

    return respuesta.choices[0].message.content


# --- FUNCIÓN PARA ENVIAR MENSAJE ---
def enviar():
    mensaje = entrada.get()
    if mensaje.strip() == "":
        return

    # Mostrar mensaje del usuario
    chat.insert(tk.END, f"Tú: {mensaje}\n")

    # Obtener respuesta del bot
    respuesta = obtener_respuesta(mensaje)
    chat.insert(tk.END, f"Bot: {respuesta}\n\n")

    # Limpiar entrada
    entrada.delete(0, tk.END)
    chat.yview(tk.END)


# --- INTERFAZ GRÁFICA ---
ventana = tk.Tk()
ventana.title("ChatBot Vendedor - Catálogo")
ventana.geometry("500x600")

titulo = tk.Label(ventana, text="ChatBot Vendedor", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

chat = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=60, height=25, font=("Arial", 11))
chat.pack(padx=10)

entrada = tk.Entry(ventana, width=60, font=("Arial", 12))
entrada.pack(padx=10, pady=10)

boton_enviar = tk.Button(ventana, text="Enviar", width=10, command=enviar, font=("Arial", 12))
boton_enviar.pack()

ventana.mainloop()
