import json
from typing import Any
from dotenv import load_dotenv
from cliente_redis import obtener_conexion
from modelo_usuario import (
    crear_usuario_json,
    leer_usuario_json,
    actualizar_usuario_json,
    eliminar_usuario,
    listar_usuarios,
)

load_dotenv()

def imprimir(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def prompt_json(prompt: str) -> str:
    texto = input(prompt).strip()
    if not texto:
        raise ValueError("Entrada JSON vacía")
    json.loads(texto)
    return texto

def menu() -> None:
    try:
        conexion = obtener_conexion()
        print("Conectado a Redis correctamente")
    except Exception as e:
        print(f"ERROR: no se pudo conectar a Redis: {e}")
        return

while True:
    print("\n" + "="*40)
    print(" MENU USUARIOS REDIS")
    print("="*40)
    print("1) Crear usuario (introduce JSON)")
    print("2) Leer usuario (por ID)")
    print("3) Actualizar usuario (ID + JSON)")
    print("4) Eliminar usuario (por ID)")
    print("5) Listar todos los usuarios")
    print("6) Salir")
    print("-"*40)

    opcion = input("Selecciona una opcion (1-6): ").strip()

    try:
        if opcion == "1":
            try:
                datos = prompt_json("Introduce JSON del usuario: ")
            except Exception as e:
                print(f"JSON invalido: {e}")
                continue

            creado = crear_usuario_json(conexion, datos)
            imprimir({"creado": bool(creado)})
            if creado:
                print("Usuario creado exitosamente")
            else:
                print("El usuario ya existe")

        elif opcion == "2":
            idu = input("ID del usuario: ").strip()
            usuario = leer_usuario_json(conexion, idu)
            imprimir({"usuario": usuario})
            if usuario is None:
                print("Usuario no encontrado")

        elif opcion == "3":
            idu = input("ID del usuario a actualizar: ").strip()

            try:
                datos = prompt_json("JSON de actualizacion: ")
            except Exception as e:
                print(f"JSON invalido: {e}")
                continue

            modo = input("Modo (mezclar/reemplazar) [mezclar]: ").strip() or "mezclar"
            actualizado = actualizar_usuario_json(conexion, idu, datos, modo=modo)
            imprimir({"actualizado": bool(actualizado)})
            if actualizado:
                print("Usuario actualizado")
            else:
                print("Usuario no encontrado")

        elif opcion == "4":
            idu = input("ID del usuario a eliminar: ").strip()
            eliminado = eliminar_usuario(conexion, idu)
            imprimir({"eliminado": bool(eliminado)})
            if eliminado:
                print("Usuario eliminado")
            else:
                print("Usuario no encontrado")

        elif opcion == "5":
            usuarios = listar_usuarios(conexion)
            imprimir({"total": len(usuarios), "usuarios": usuarios})
            print(f"Total de usuarios: {len(usuarios)}")

        elif opcion == "6":
            print("Hasta luego!")
            break

        else:
            print("Opcion no valida. Intenta del 1 al 6.")

    except Exception as e:
        print(f"ERROR: {e}")

def main() -> int:
    try:
        menu()
        return 0
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())