# --- 1. MODELADO DE DATOS SIMPLE ---
class Contenido:
    def __init__(self, nombre, genero, calificacion, es_adultos=False):
        self.nombre = nombre
        self.genero = genero
        self.calificacion = calificacion
        self.es_adultos = es_adultos

# --- 2. FUNCIONES DE CARGA DE DATOS ---
def cargar_base_datos():
    juegos = []
    peliculas = []
    
    # Datos de prueba (Luego los leeremos de los archivos reales)
    juegos.append(Contenido("Counter-Strike 2", "Action", 8.3, es_adultos=False))
    juegos.append(Contenido("Grand Theft Auto V Enhanced", "Action", 8.9, es_adultos=True))
    juegos.append(Contenido("Slay the Spire", "Indie", 9.7, es_adultos=False))
    
    peliculas.append(Contenido("The Dark Knight", "Action", 9.0, es_adultos=False))
    peliculas.append(Contenido("The Godfather", "Crime", 9.2, es_adultos=True))
    
    return juegos, peliculas

# --- 3. FLUJO PRINCIPAL ---
def iniciar_recomendador():
    print("=========================================")
    print("¡Bienvenido al Recomendador Multimedia!")
    print("=========================================\n")
    
    juegos, peliculas = cargar_base_datos()
    
    try:
        edad = int(input("Por favor, ingresa tu edad para comenzar: "))
    except ValueError:
        print("Entrada no válida. Se asumirá que eres menor de edad por seguridad.")
        edad = 17

    es_mayor_edad = edad >= 18
    if not es_mayor_edad:
        print("🔒 Modo seguro activado: Se filtrará el contenido para mayores de 18 años.\n")
    else:
        print("🔓 Acceso total concedido (Contenido +18 incluido).\n")

    print("¿Qué estás buscando hoy?")
    print("1. Videojuegos")
    print("2. Películas")
    
    opcion_tipo = input("Selecciona una opción (1 o 2): ")
    
    if opcion_tipo == "1":
        base_actual = juegos
        tipo_texto = "Videojuegos"
    elif opcion_tipo == "2":
        base_actual = peliculas
        tipo_texto = "Películas"
    else:
        print("Opción inválida.")
        return

    if not es_mayor_edad:
        base_filtrada_edad = [item for item in base_actual if not item.es_adultos]
    else:
        base_filtrada_edad = base_actual

    generos_disponibles = sorted(list(set(item.genero for item in base_filtrada_edad)))

    print(f"\n--- Géneros Disponibles en {tipo_texto} ---")
    for indice, gen in enumerate(generos_disponibles, start=1):
        print(f"{indice}. {gen}")
        
    try:
        opcion_genero = int(input("\nSelecciona el número del género que te interesa: "))
        genero_seleccionado = generos_disponibles[opcion_genero - 1]
        print(f"\nPerfecto, has seleccionado el género: {genero_seleccionado}")
    except (ValueError, IndexError):
        print("Selección de género inválida.")
        return

    print(f"\n[Próximo paso]: Procesando las mejores recomendaciones de {genero_seleccionado} con Heaps...")

if __name__ == "__main__":
    iniciar_recomendador()
