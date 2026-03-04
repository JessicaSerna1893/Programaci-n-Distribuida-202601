import asyncio
import time

# Recurso compartido
contador_clientes = 0

# Lock para controlar acceso concurrente
lock = asyncio.Lock()

# Semáforo para simular número limitado de cajeros
cajeros = asyncio.Semaphore(2)  # Solo 2 clientes pueden ser atendidos al tiempo


async def handle_client(reader, writer):
    global contador_clientes

    addr = writer.get_extra_info('peername')
    print(f"Cliente conectado desde {addr}")

    data = await reader.read(1024)
    nombre = data.decode().strip()

    tiempo_inicio = time.time()

    # Espera turno (control de concurrencia)
    async with cajeros:

        # Controla acceso al recurso compartido
        async with lock:
            contador_clientes += 1
            cliente_actual = contador_clientes

        print(f"Atendiendo cliente #{cliente_actual}: {nombre}")

        # Simula atención bancaria (delay)
        await asyncio.sleep(3)

        tiempo_fin = time.time()
        tiempo_total = round(tiempo_fin - tiempo_inicio, 2)

        respuesta = (
            f"Cliente #{cliente_actual} atendido.\n"
            f"Nombre: {nombre}\n"
            f"Tiempo de atención: {tiempo_total} segundos\n"
            f"Total clientes atendidos: {contador_clientes}\n"
        )

        writer.write(respuesta.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()

    print(f"Cliente {nombre} desconectado\n")


async def main():
    server = await asyncio.start_server(
        handle_client, "0.0.0.0", 5000
    )

    print("Servidor bancario async ejecutándose en puerto 5000...")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
