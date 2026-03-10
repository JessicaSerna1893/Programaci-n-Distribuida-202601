# ============================
# IMPORTACIONES
# ============================

from fastapi import FastAPI, HTTPException
from typing import List
import asyncio

# ============================
# CREACIÓN DE LA APLICACIÓN
# ============================

app = FastAPI()

# ============================
# BASE DE DATOS SIMULADA
# ============================

clientes = []

# contador global de clientes creados
contador_clientes = 0


# ============================
# ENDPOINT RAÍZ
# ============================

@app.get("/")
def home():
    return {"mensaje": "API del Banco funcionando"}


# ============================
# CREAR CLIENTE (CON DELAY)
# ============================

@app.post("/clientes")
async def crear_cliente(nombre: str):

    global contador_clientes

    # Validación básica
    if nombre.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="El nombre no puede estar vacío"
        )

    # Simulación de proceso lento
    await asyncio.sleep(3)

    contador_clientes += 1

    cliente = {
        "id": contador_clientes,
        "nombre": nombre
    }

    clientes.append(cliente)

    return cliente


# ============================
# LISTAR CLIENTES
# ============================

@app.get("/clientes", response_model=List[dict])
def listar_clientes():
    return clientes


# ============================
# OBTENER CLIENTE POR ID
# ============================

@app.get("/clientes/{cliente_id}")
def obtener_cliente(cliente_id: int):

    for cliente in clientes:
        if cliente["id"] == cliente_id:
            return cliente

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )


# ============================
# ACTUALIZAR CLIENTE
# ============================

@app.put("/clientes/{cliente_id}")
def actualizar_cliente(cliente_id: int, nombre: str):

    if nombre.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="El nombre no puede estar vacío"
        )

    for cliente in clientes:
        if cliente["id"] == cliente_id:
            cliente["nombre"] = nombre
            return {
                "mensaje": "Cliente actualizado",
                "cliente": cliente
            }

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )


# ============================
# ELIMINAR CLIENTE
# ============================

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int):

    for cliente in clientes:
        if cliente["id"] == cliente_id:
            clientes.remove(cliente)
            return {"mensaje": "Cliente eliminado"}

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )


# ============================
# CONTADOR GLOBAL
# ============================

@app.get("/estadisticas")
def estadisticas():

    return {
        "clientes_creados": contador_clientes,
        "clientes_actuales": len(clientes)
    }