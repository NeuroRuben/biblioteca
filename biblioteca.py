
import json
import os
from datetime import datetime

ARCHIVO = "biblioteca.json"


def cargar_libros():
    """Carga los libros guardados en el archivo JSON."""
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                return []
    return []


def guardar_libros(libros):
    """Guarda la biblioteca en un archivo JSON."""
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(libros, archivo, ensure_ascii=False, indent=4)


def fecha_valida(fecha, formato="%Y"):
    """Comprueba que una fecha tenga el formato indicado."""
    try:
        datetime.strptime(fecha, formato)
        return True
    except ValueError:
        return False


def agregar_libro(libros):
    """Solicita los datos de un libro y lo añade a la biblioteca."""
    print("\n--- Añadir un libro ---")

    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()

    if not titulo or not autor:
        print("El título y el autor son obligatorios.")
        return

    publicacion = input("Año de publicación (AAAA): ").strip()

    if not fecha_valida(publicacion):
        print("Fecha no válida. Introduce solo el año de publicación.")
        return

    try:
        paginas = int(input("Número de páginas: "))
        if paginas <= 0:
            print("El número de páginas debe ser positivo.")
            return
    except ValueError:
        print("Introduce un número entero válido.")
        return

    genero = input("Género literario: ").strip()
    lectura = input(
        "Fecha de lectura (AAAA-MM-DD) "
        "o pulsa Enter si aún no lo has leído: "
    ).strip()

    if lectura and not fecha_valida(lectura):
        print("Fecha de lectura no válida.")
        return

    libro = {
        "titulo": titulo,
        "autor": autor,
        "fecha_publicacion": publicacion,
        "paginas": paginas,
        "genero": genero,
        "fecha_lectura": lectura or None
    }

    libros.append(libro)
    guardar_libros(libros)
    print(f"\nLibro '{titulo}' añadido correctamente.")


def mostrar_libros(libros):
    """Muestra todos los libros registrados."""
    print("\n--- Mi biblioteca virtual ---")

    if not libros:
        print("Todavía no hay libros registrados.")
        return

    for i, libro in enumerate(libros, start=1):
        estado = libro["fecha_lectura"] or "Pendiente de lectura"

        print(f"\n{i}. {libro['titulo']}")
        print(f"   Autor: {libro['autor']}")
        print(f"   Publicación: {libro['fecha_publicacion']}")
        print(f"   Páginas: {libro['paginas']}")
        print(f"   Género: {libro['genero']}")
        print(f"   Fecha de lectura: {estado}")


def buscar_libro(libros):
    """Busca libros por título o autor."""
    termino = input("\nIntroduce un título o autor: ").strip().casefold()

    resultados = [
        libro for libro in libros
        if termino in libro["titulo"].casefold()
        or termino in libro["autor"].casefold()
    ]

    if resultados:
        print("\n--- Resultados de búsqueda ---")
        mostrar_libros(resultados)
    else:
        print("No se encontraron libros.")


def marcar_leido(libros):
    """Registra la fecha de lectura de un libro."""
    titulo = input("\nTítulo del libro leído: ").strip().casefold()

    encontrados = [
        libro for libro in libros
        if libro["titulo"].casefold() == titulo
    ]

    if not encontrados:
        print("No se encontró ese libro.")
        return

    for libro in encontrados:
        fecha = input(
            f"Fecha de lectura de '{libro['titulo']}' "
            "(AAAA-MM-DD, Enter para hoy): "
        ).strip()

        if not fecha:
            fecha = datetime.today().strftime("%Y-%m-%d")

        if not fecha_valida(fecha):
            print("Fecha no válida.")
            return

        libro["fecha_lectura"] = fecha

    guardar_libros(libros)
    print("Fecha de lectura guardada correctamente.")


def mostrar_estadisticas(libros):
    """Muestra estadísticas de la biblioteca."""
    total = len(libros)
    leidos = sum(1 for libro in libros if libro["fecha_lectura"])
    pendientes = total - leidos
    paginas = sum(libro["paginas"] for libro in libros)

    print("\n--- Estadísticas ---")
    print(f"Total de libros: {total}")
    print(f"Libros leídos: {leidos}")
    print(f"Libros pendientes: {pendientes}")
    print(f"Total de páginas de la colección: {paginas}")

    generos = {}
    for libro in libros:
        genero = libro["genero"] or "Sin género"
        generos[genero] = generos.get(genero, 0) + 1

    if generos:
        print("\nLibros por género:")
        for genero, cantidad in sorted(generos.items()):
            print(f"  {genero}: {cantidad}")


def menu():
    libros = cargar_libros()

    while True:
        print("\n====== BIBLIOTECA VIRTUAL ======")
        print("1. Añadir un libro")
        print("2. Mostrar todos los libros")
        print("3. Buscar por título o autor")
        print("4. Registrar fecha de lectura")
        print("5. Ver estadísticas")
        print("6. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            agregar_libro(libros)
        elif opcion == "2":
            mostrar_libros(libros)
        elif opcion == "3":
            buscar_libro(libros)
        elif opcion == "4":
            marcar_leido(libros)
        elif opcion == "5":
            mostrar_estadisticas(libros)
        elif opcion == "6":
            print("¡Hasta pronto! Tu biblioteca está guardada.")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")


if __name__ == "__main__":
    menu()
