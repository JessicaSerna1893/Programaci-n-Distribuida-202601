# ============================
# IMPORTACIONES
# ============================

from fastapi import FastAPI, HTTPException
from typing import List
import asyncio

# ============================
# CREACIÓN DE LA API
# ============================

app = FastAPI()

# ============================
# BASE DE DATOS SIMULADA
# ============================

citas = []
contador_citas = 0

# ============================
# ENDPOINT RAÍZ
# ============================

@app.get("/")
async def home():
    return {"mensaje": "Sistema de citas médicas funcionando"}

# ============================
# CREAR CITA
# ============================

@app.post("/citas")
async def crear_cita(paciente: str, doctor: str, fecha: str):

    global contador_citas

    # Validación básica
    if paciente.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="El nombre del paciente no puede estar vacío"
        )

    # Simulación de proceso lento
    await asyncio.sleep(2)

    contador_citas += 1

    cita = {
        "id": contador_citas,
        "paciente": paciente,
        "doctor": doctor,
        "fecha": fecha,
        "estado": "activa"
    }

    citas.append(cita)

    return {
        "mensaje": "Cita creada correctamente",
        "cita": cita
    }

# ============================
# LISTAR CITAS
# ============================

@app.get("/citas", response_model=List[dict])
async def listar_citas():
    return citas

# ============================
# BUSCAR CITA POR PACIENTE
# ============================

@app.get("/citas/paciente/{nombre}")
async def buscar_cita(nombre: str):

    resultados = []

    for cita in citas:
        if cita["paciente"].lower() == nombre.lower():
            resultados.append(cita)

    if not resultados:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron citas para este paciente"
        )

    return resultados

# ============================
# CANCELAR CITA
# ============================

@app.delete("/citas/{cita_id}")
async def cancelar_cita(cita_id: int):

    for cita in citas:
        if cita["id"] == cita_id:
            cita["estado"] = "cancelada"
            return {
                "mensaje": "Cita cancelada correctamente",
                "cita": cita
            }

    raise HTTPException(
        status_code=404,
        detail="Cita no encontrada"
    )
