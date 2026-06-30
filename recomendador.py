import csv
import heapq

# --- 1. MODELADO DE DATOS AVANZADO (Polimorfismo) ---
class Contenido:
    def __init__(self, nombre, generos, calificacion, es_adultos=False):
        self.nombre = nombre
        self.generos = [g.strip() for g in generos.split(',')] if generos else ['Desconocido']
        self.calificacion = float(calificacion) if calificacion else 0.0
        self.es_adultos = es_adultos

class Videojuego(Contenido):
    def __init__(self, nombre, generos, calificacion, precio, tags, steam_deck, es_adultos=False):
        super().__init__(nombre, generos, calificacion, es_adultos)
        self.precio = precio
        self.tags = tags
        self.steam_deck = steam_deck

class Pelicula(Contenido):
    def __init__(self, nombre, generos, calificacion, duracion, sinopsis, es_adultos=False):
        super().__init__(nombre, generos, calificacion, es_adultos)
        self.duracion = duracion
        self.sinopsis = sinopsis

# --- 2. LECTURA DE ARCHIVOS REALES MEJORADA ---
def cargar_base_datos():
    juegos = []
    peliculas = []
    
    # Leer Videojuegos de Steam
    try:
        with open('steam_games_2026.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tags = row.get('All_Tags', '')
                genero_principal = row.get('Primary_Genre', 'Action')
                
                # Unimos el género principal con las etiquetas para tener más opciones de búsqueda
                generos_totales = f"{genero_principal}, {tags}" if tags else genero_principal
                
                es_adulto = any(x in tags.lower() for x in ['sexual content', 'mature', 'nudity', 'gambling'])
                pct_score = float(row.get('Review_Score_Pct', 0)) / 10.0 if row.get('Review_Score_Pct') else 0.0
                
                juegos.append(Videojuego(
                    nombre=row.get('Name', 'Sin Nombre'),
                    generos=generos_totales,
                    calificacion=pct_score,
                    precio=row.get('Price_USD', 'Free'),
                    tags=tags,
                    steam_deck=row.get('Steam_Deck_Status', 'Unknown'),
                    es_adultos=es_adulto
                ))
    except FileNotFoundError:
        print("⚠️ No se encontró steam_games_2026.csv")

    # Leer Películas de IMDb (Manejo de formato con comillas dobles para sinopsis)
    try:
        with open('imdb_top_1000.csv', mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 7:
                    titulo = row[1]
                    duracion = row[3]
                    generos = row[4]
                    
                    try:
                        calif = float(row[5])
                    except ValueError:
                        continue # Salta la cabecera si no es un número
                        
                    sinopsis = row[6]
                    es_adulto = any(x in generos for x in ['Crime', 'Thriller', 'Horror'])
                    
                    peliculas.append(Pelicula(
                        nombre=titulo,
                        generos=generos,
                        calificacion=calif,
                        duracion=duracion,
                        sinopsis=sinopsis,
                        es_adultos=es_adulto
                    ))
    except FileNotFoundError:
        print("⚠️ No se encontró imdb_top_1000.csv")
        
    return juegos, peliculas

# --- 3. FLUJO PRINCIPAL ---
def iniciar_recomendador():
    print("=========================================")
    print(" 🚀 RECOMENDADOR MULTIMEDIA PRO 🚀")
    print("=========================================\n")
    
    juegos, peliculas = cargar_base_datos()
    
    if not juegos and not peliculas:
        print("Error: No se pudieron cargar las bases de datos. Revisa los archivos.")
        return

    try:
        edad = int(input("Por favor, ingresa tu edad para comenzar: "))
    except ValueError:
        edad = 17

    es_mayor_edad = edad >= 18
    print("🔒 Modo seguro activado" if not es_mayor_edad else "🔓 Acceso total concedido")

    print("\n¿Qué estás buscando hoy?")
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

    # Filtrar por edad
    base_filtrada_edad = base_actual if es_mayor_edad else [item for item in base_actual if not item.es_adultos]

    # Extraer TODOS los géneros individuales sin repetir
    set_generos = set()
    for item in base_filtrada_edad:
        for g in item.generos:
            if g and g != 'Unknown' and g != 'Desconocido':
                set_generos.add(g)
    
    generos_disponibles = sorted(list(set_generos))

    print(f"\n--- 🎭 GÉNEROS ENCONTRADOS ({len(generos_disponibles)}) ---")
    # Mostramos los géneros en columnas para que no ocupe tanto espacio hacia abajo
    for indice, gen in enumerate(generos_disponibles, start=1):
        print(f"{indice:2d}. {gen:<20}", end="\t" if indice % 3 != 0 else "\n")
        
    try:
        opcion_genero = int(input("\n\nSelecciona el número del género: "))
        genero_seleccionado = generos_disponibles[opcion_genero - 1]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    # --- HEAP DE PRIORIDAD ---
    heap_recomendaciones = []
    for item in base_filtrada_edad:
        if genero_seleccionado in item.generos:
            # Multiplicamos por -1 para simular Max-Heap
            heapq.heappush(heap_recomendaciones, (-item.calificacion, item))
            
    print(f"\n🎯 TOP 3 RECOMENDACIONES CONCRETAS DE {genero_seleccionado.upper()} 🎯")
    print("=" * 65)
    
    contador = 1
    while heap_recomendaciones and contador <= 3:
        prioridad, item = heapq.heappop(heap_recomendaciones)
        
        print(f"\n🏅 RECOMENDACIÓN #{contador}")
        print(f"🎬 Título: {item.nombre}")
        print(f"⭐ Calificación: {item.calificacion:.1f}/10")
        
        # Si es un Videojuego, muestra sus datos específicos
        if isinstance(item, Videojuego):
            print(f"💵 Precio: ${item.precio} USD")
            print(f"🎮 Compatibilidad Steam Deck: {item.steam_deck}")
            print(f"🏷️ Etiquetas: {item.tags[:100]}...")
            
        # Si es una Película, muestra su sinopsis y duración
        elif isinstance(item, Pelicula):
            print(f"⏳ Duración: {item.duracion}")
            print(f"📝 Sinopsis: {item.sinopsis}")
            
        print("-" * 65)
        contador += 1

if __name__ == "__main__":
    iniciar_recomendador()
