# app/ — Fase 6: Aplicación web (dashboard)

**Qué hace:** una web sencilla para explorar los fondos: tabla filtrable, gráficos y ficha de detalle.
**Lee los datos de la API** (no de la base de datos directamente).

**Referencia del taller:** **Streamlit** desplegado en **Amazon ECS Express Mode** (contenedor Docker).

## Pantallas mínimas (propuesta)

1. **Tabla de fondos** con filtros por gestora y SRI.
2. **Gráficos** sencillos, cada uno con una frase que explique qué se ve. Por ejemplo:
   - Nº de fondos por nivel de riesgo (SRI 1–7).
   - Gastos corrientes (%) por gestora.
   - Riesgo (SRI) frente a gastos: ¿los fondos más arriesgados son más caros?
3. **Ficha de un fondo**: todos los campos del Anexo A + de qué PDF salió y cuándo se descargó.

## Ficheros

| Fichero | Estado |
|---|---|
| `app.py` | ⬜ Pendiente (taller 2) |
| `Dockerfile` | ⬜ Pendiente |
| `requirements.txt` | ⬜ Pendiente |
