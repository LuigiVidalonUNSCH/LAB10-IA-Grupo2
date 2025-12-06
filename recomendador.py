import random
import sys

# --- 1. Catálogo de Productos (con precios y nombres de tu JSON) ---
CATALOGO_COMPLETO = [
    {"id": 1, "nombre": "Laptop Lenovo i5", "precio": 2500.00},
    {"id": 2, "nombre": "Mouse Gamer RGB", "precio": 80.00},
    {"id": 3, "nombre": "Audífonos Sony WH-CH520", "precio": 220.00},
    {"id": 4, "nombre": "Monitor Curvo 27'' Samsung", "precio": 950.00},
    {"id": 5, "nombre": "Teclado Mecánico RGB", "precio": 350.00},
    {"id": 6, "nombre": "Webcam Full HD Logitech", "precio": 180.00},
    {"id": 7, "nombre": "Disco Duro SSD 1TB Kingston", "precio": 400.00},
    {"id": 8, "nombre": "Smartwatch Xiaomi Band 7", "precio": 150.00},
    {"id": 9, "nombre": "Router WiFi 6 Tenda", "precio": 120.00},
    {"id": 10, "nombre": "Impresora Multifuncional HP", "precio": 580.00}
]

# --- 2. Funciones de Ayuda ---

def mostrar_catalogo():
    """Imprime el catálogo completo con ID y precio."""
    print("\n📦 Nuestro Catálogo de Productos 📦")
    print("------------------------------------------")
    for p in CATALOGO_COMPLETO:
        print(f"ID: {p['id']:<2} - {p['nombre']:<30} S/. {p['precio']:.2f}")
    print("------------------------------------------")

def calcular_total(lista_de_compras):
    """Calcula el monto total de la lista de compras."""
    total = sum(p['precio'] for p in lista_de_compras)
    return total

def recomendar_productos(ids_excluidos, n=3):
    """Recomienda 'n' productos que no están en la lista de IDs excluidos."""
    
    productos_disponibles = [p for p in CATALOGO_COMPLETO if p['id'] not in ids_excluidos]
    
    if len(productos_disponibles) >= n:
        recomendados = random.sample(productos_disponibles, n)
    else:
        recomendados = productos_disponibles
        
    return recomendados

def agregar_productos_recomendados(lista_de_compras, ids_recomendados):
    """Permite al usuario agregar productos de una lista a la compra."""
    
    print("\n📝 ¿Deseas agregar alguno de estos productos a tu compra?")
    print("Instrucciones: Ingresa el ID del producto (ej: 4, 7). Escribe [no] para omitir.")
    
    # Crear un diccionario para mapear ID a producto recomendado
    mapa_recomendados = {p['id']: p for p in ids_recomendados}
    
    while True:
        user_input = input(f"ID del producto a añadir o [no]: ").strip().lower()

        if user_input == "no":
            break
        
        try:
            producto_id = int(user_input)
            
            if producto_id in mapa_recomendados:
                producto_a_agregar = mapa_recomendados[producto_id]
                lista_de_compras.append(producto_a_agregar)
                
                # Remover de la lista de recomendados para no volver a ofrecerlo
                del mapa_recomendados[producto_id]
                print(f"🎉 Añadido: {producto_a_agregar['nombre']} a la lista de compras.")
                
            else:
                print("❌ Error: ID no reconocido o ya fue agregado. Intenta de nuevo o escribe [no].")

        except ValueError:
            print("❌ Entrada no válida. Por favor, ingresa un número de ID o escribe [no].")


# --- 3. Bucle de Conversación Principal ---

def iniciar_conversacion_fluida():
    
    lista_de_compras = []
    # Conjunto de IDs para evitar recomendar productos que ya están en la lista o que ya fueron recomendados
    ids_excluidos_total = set() 
    
    print("--- Sistema de Compras y Recomendación (LAB 10) ---")
    
    # 1. Preguntar el nombre
    nombre_cliente = input("Hola, soy tu asistente de compras. ¿Cuál es tu nombre?: ").strip()
    if not nombre_cliente:
        nombre_cliente = "Cliente"
    print(f"\n¡Un gusto saludarte, {nombre_cliente}!")
    
    # 2. Mostrar la lista de productos
    mostrar_catalogo()
    
    # 3. Bucle para agregar productos iniciales
    print(f"\n🛒 {nombre_cliente}, ingresa los productos que deseas comprar.")
    print("Instrucciones: Ingresa el ID del producto (ej: 1, 5, 8). Escribe [ok] para continuar.")
    
    while True:
        user_input = input(f"Ingresa un ID o [ok]: ").strip().lower()

        if user_input == "ok":
            if lista_de_compras:
                # Actualiza los IDs excluidos con la lista de compras
                ids_excluidos_total.update({p['id'] for p in lista_de_compras})
                break
            else:
                print("❌ Tu lista está vacía. Por favor, agrega al menos un producto.")
                continue
        
        try:
            producto_id = int(user_input)
            producto_encontrado = next((p for p in CATALOGO_COMPLETO if p['id'] == producto_id), None)

            if producto_encontrado:
                lista_de_compras.append(producto_encontrado)
                print(f"🎉 Añadido: {producto_encontrado['nombre']} a la lista.")
            else:
                print(f"❌ Error: El ID {producto_id} no existe en el catálogo.")

        except ValueError:
            print("❌ Entrada no válida. Por favor, ingresa un número de ID o escribe [ok].")
    
    # --- PROCESO DE RECOMENDACIÓN INICIAL (Paso 4 y 5) ---
    print("\n------------------------------------------")
    recomendados_ronda1 = recomendar_productos(ids_excluidos_total, n=3)
    
    if recomendados_ronda1:
        print(f"🧠 ¡Excelente, {nombre_cliente}! Basado en tu selección, te recomendamos 3 productos:")
        for prod in recomendados_ronda1:
            print(f" • {prod['nombre']} (ID: {prod['id']})")
        
        # 5. Permitir agregar los productos recomendados a la lista
        agregar_productos_recomendados(lista_de_compras, recomendados_ronda1)
        
        # Actualizar IDs excluidos después de la posible adición
        ids_excluidos_total.update({p['id'] for p in recomendados_ronda1})
    else:
        print("¡Compraste casi todo! No tenemos suficientes productos para una recomendación inicial.")


    # --- SEGUNDA RONDA DE RECOMENDACIÓN (CONDICIONAL - Paso 6) ---
    # Solo si quedan productos que no han sido comprados ni recomendados
    if len(CATALOGO_COMPLETO) > len(ids_excluidos_total):
        
        while True:
            pide_mas = input("\n¿Te gustaría que te recomendemos otros 3 productos? [si/no]: ").strip().lower()
            
            if pide_mas in ["no", "n"]:
                print("Entendido. Pasemos al resumen de tu compra.")
                break
            
            elif pide_mas in ["si", "s"]:
                recomendados_extra = recomendar_productos(ids_excluidos_total, n=3)
                
                if recomendados_extra:
                    print("\n✨ ¡Aquí tienes otras 3 ideas! ✨")
                    for prod in recomendados_extra:
                        print(f" • {prod['nombre']} (ID: {prod['id']})")
                        
                    # 5. Permitir agregar los productos recomendados a la lista
                    agregar_productos_recomendados(lista_de_compras, recomendados_extra)

                    # Actualiza los excluidos para evitar más repeticiones
                    ids_excluidos_total.update({p['id'] for p in recomendados_extra})
                else:
                    print("\nLo siento, ya no quedan más productos únicos para recomendarte.")
                    break
            else:
                print("Respuesta no válida. Por favor, ingresa [si] o [no].")

    # 7. Mostrar lista de compras y monto total
    total_a_pagar = calcular_total(lista_de_compras)
    
    print(f"\n\n✅ Lista Final de Compras de {nombre_cliente}:")
    for i, item in enumerate(lista_de_compras):
        print(f" {i+1}. {item['nombre']} - S/. {item['precio']:.2f}")
        
    print(f"\n💰 Monto TOTAL a Pagar: S/. {total_a_pagar:.2f}")

    # 8. Preguntar método de pago
    while True:
        pago_input = input("\n¿Prefieres pagar en [efectivo] o con [tarjeta]?: ").strip().lower()
        if pago_input in ["efectivo", "tarjeta"]:
            print(f"¡Entendido! Procesaremos tu pago con {pago_input}.")
            break
        else:
            print("Método no reconocido. Por favor, elige entre [efectivo] o [tarjeta].")

    # 9. Finalizar
    print(f"\n¡Tu compra ha sido procesada con éxito! Gracias por tu visita, {nombre_cliente}.")
    sys.exit()


if __name__ == "__main__":
    iniciar_conversacion_fluida()
