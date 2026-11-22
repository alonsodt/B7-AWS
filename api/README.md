# api/ — Fase 5: API HTTP

**Qué hace:** expone los datos de PostgreSQL a través de URLs, para que la app (o cualquiera con acceso)
pueda consultarlos sin conectarse directamente a la base de datos.

**Referencia del taller:** **FastAPI** dentro de una **AWS Lambda** con **Function URL**
(una URL pública que invoca la Lambda sin necesidad de API Gateway).

## Endpoints mínimos (propuesta)

| Método | Ruta | Devuelve |
|---|---|---|
| GET | `/health` | `{"ok": true}` — para comprobar que la API está viva |
| GET | `/fondos` | Lista de KID (con filtros opcionales: `gestora`, `sri`) |
| GET | `/fondos/{isin}` | Detalle de un fondo por ISIN |
| GET | `/estadisticas` | Resumen: nº de fondos por gestora, SRI medio, gastos medios… |

FastAPI genera la documentación interactiva sola en `/docs` (útil para la demo).

## Ficheros

| Fichero | Estado |
|---|---|
| `main.py` | ⬜ Pendiente (taller 2) |
| `requirements.txt` | ⬜ Pendiente (dependencias propias de la Lambda) |

> La API es la única puerta pública a los datos (junto con la app). Nunca devolver URLs directas al bucket S3.
