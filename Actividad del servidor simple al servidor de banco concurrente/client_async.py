import asyncio
import time

async def main():
    # Abre conexión con el servidor
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 5000
    )

    # Solicita el nombre al usuario
    name = input("Ingresa tu nombre: ")

    # Guarda el tiempo inicial
    start_time = time.time()

    # Envía el nombre al servidor
    writer.write(name.encode())

    # Asegura que el mensaje se envíe completamente
    await writer.drain()

    # Espera respuesta del servidor
    data = await reader.read(1024)

    # Guarda el tiempo final
    end_time = time.time()

    # Muestra respuesta
    print(data.decode())

    # Calcula el tiempo total de atención
    print(f"Tiempo de atención: {round(end_time - start_time, 2)} segundos")

    # Cierra la conexión
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
