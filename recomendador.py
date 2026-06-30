import csv
import heapq  
class Contenido:
    def __init__(self, nombre, genero, calificacion, es_adultos=False):
        self.nombre = nombre
        self.genero = genero
        self.calificacion = float(calificacion) if calificacion else 0.0
        self.es_adultos = es_adultos


def cargar_base_datos():
    juegos = []
    peliculas = []
    
    try:
        with open('steam_games_2026.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
              
                tags = row.get('All_Tags', '').lower()
                genero = row.get('Primary_Genre', 'Desconocido')
                es_adulto = 'sexual content' in tags or 'mature' in tags or 'nudity' in tags
                
               
                pct_score = float(row.get('Review_Score_Pct', 0)) / 10.0
                
                juegos.append(Contenido(
                    nombre=row.get('Name', 'Sin Nombre'),
                    genero=genero,
                    calificacion=pct_score,
                    es_adultos=es_adulto
                ))
    except FileNotFoundError:
        print("⚠️ No se encontró steam_games_2026.csv, usando simulación.")


    try:
        with open('imdb_top_1000.csv', mode='r', encoding='utf-8') as f:
    
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 5:
      
                    titulo = row[1]
                    generos_completos = row[4]
                    primer_genero = generos_completos.split(',')[0].strip()
                    try:
                        calif = float(row[5])
                    except ValueError:
                        calif = 0.0
                    
                    es_adulto = 'Crime' in generos_completos or 'Thriller' in generos_completos
                    
                    peliculas.append(Contenido(
                        nombre=titulo,
                        genero=primer_genero,
                        calificacion=calif,
                        es_adultos=es_adulto
                    ))
    except FileNotFoundError:
        print("⚠️ No se encontró imdb_top_1000.csv, usando simulación.")
        
    return juegos, peliculas

def iniciar_recomendador():
    print("=========================================")
    print("¡Bienvenido al Recomendador Multimedia!")
    print("=========================================\n")
    

    juegos, peliculas = cargar_base_datos()
    
    try:
        edad = int(input("Por favor, ingresa tu edad para comenzar: "))
    except ValueError:
        print("Entrada no válida. Se asumirá menor de edad.")
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

    generos_disponibles = sorted(list(set(item.genero for item in base_filtrada_edad if item.genero)))

    print(f"\n--- Géneros Disponibles en {tipo_texto} ---")
    for indice, gen in enumerate(generos_disponibles, start=1):
        print(f"{indice}. {gen}")
        
    try:
        opcion_genero = int(input("\nSelecciona el número del género que te interesa: "))
        genero_seleccionado = generos_disponibles[opcion_genero - 1]
    except (ValueError, IndexError):
        print("Selección de género inválida.")
        return

    heap_recomendaciones = []
    
    for item in base_filtrada_edad:
        if item.genero == genero_seleccionado:
        
            heapq.heappush(heap_recomendaciones, (-item.calificacion, item))
            
   
    print(f"\n🏆 TOP RECOMENDACIONES DE {genero_seleccionado.upper()} 🏆")
    print("-" * 50)
    
    top_n = 5
    contador = 1
    
    while heap_recomendaciones and contador <= top_n:
       
        prioridad, item_recomendado = heapq.heappop(heap_recomendaciones)
        print(f"{contador}. ⭐ {item_recomendado.calificacion:.1f}/10 - {item_recomendado.nombre}")
        contador += 1
        
    if contador == 1:
        print("No se encontraron elementos para los filtros seleccionados.")

if __name__ == "__main__":
    iniciar_recomendador()
