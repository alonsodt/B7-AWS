# ESTADO del proyecto

> **Última actualización:** 2026-11-22 · **por:** _(nombre)_
>
> Este fichero es el «tablero» del grupo. Léelo antes de empezar y actualízalo al terminar
> (instrucciones en [CLAUDE.md §7](CLAUDE.md#7-al-terminar-una-tarea--actualiza-estadomd)).

## En una frase

Repositorio creado con la estructura, las normas de trabajo y los borradores del esquema de datos.
**Todavía no hay código del pipeline ni nada desplegado en AWS.** Siguiente paso: inspeccionar las webs
y montar la conexión GitHub ↔ AWS (contenido del taller 1).

## Fechas clave

| Fecha | Qué | Estado |
|---|---|---|
| _por confirmar_ | Taller 1 – Captura e infraestructura base | ❓ |
| _por confirmar_ | Taller 2 – IA, datos y aplicación | ❓ |
| **mié 2026-12-02** | **Entrega** por el aula virtual (repo + URLs + integrantes) | ⏳ quedan 10 días |
| _por confirmar_ | Taller 3 – Exposición (5 min + 5 min de preguntas, demo en directo) | ❓ |

## Integrantes y reparto

| Persona | Usuario GitHub | Parte principal | Revisa a |
|---|---|---|---|
| _(nombre)_ | | | |
| _(nombre)_ | | | |
| _(nombre)_ | | | |

**Propuesta de reparto por capas** (ajustar al tamaño del grupo):

- **A · Captura:** scrapers de las gestoras + subida a S3 + manifiesto.
- **B · Extracción IA:** script de Bedrock + validación + evaluación de calidad.
- **C · Datos y API:** esquema SQL + carga sin duplicados + FastAPI en Lambda.
- **D · App e infraestructura:** Streamlit + Terraform + GitHub Actions.

Aunque cada uno lleve una parte, **todos tenemos que entender todas** (nos pueden preguntar cualquier cosa).
Por eso cada PR lo revisa alguien de otra parte.

## Dirección que estamos tomando

1. **Seguimos la arquitectura de referencia de los talleres** ([D-001](docs/decisiones.md)). Solo cambiaremos piezas
   con un motivo claro y apuntado.
2. **Primero algo que funcione de punta a punta, luego mejorar.** Orden: 1 gestora fácil (Bestinver) recorriendo
   todo el pipeline → añadir la 2.ª y la 3.ª → ampliaciones.
3. **Código muy comentado y resultados interpretados**, porque el objetivo es aprender (ver [CLAUDE.md](CLAUDE.md)).
4. **Ampliaciones elegidas (propuesta)**, por orden de relación esfuerzo/aprendizaje:
   1. Medir la precisión con KIDs revisados a mano → sale casi gratis de `docs/resultados.md`.
   2. Tests y validaciones en GitHub Actions (p. ej. `pytest` del esquema + `terraform validate`).
   3. Comparar dos modelos de Bedrock en la extracción.
   4. _(si sobra tiempo)_ S3 → Lambda por eventos, o buscador en lenguaje natural.

## Fases y tareas

Leyenda: ⬜ pendiente · 🟡 en curso · ✅ hecho · ❓ falta decidir

| # | Fase | Tarea | Responsable | Estado |
|---|---|---|---|---|
| 0 | Organización | Crear repo, CLAUDE.md, ESTADO.md, estructura | | ✅ |
| 0 | Organización | Subir a GitHub, invitar al grupo y al profesor | | ⬜ |
| 0 | Organización | Rellenar integrantes y reparto | | ⬜ |
| 1 | Captura | Inspeccionar las 3 webs: contar KIDs, revisar `robots.txt` | | ⬜ |
| 1 | Captura | Scraper Bestinver | | ⬜ |
| 1 | Captura | Scraper Azvalor | | ⬜ |
| 1 | Captura | Scraper Cobas (varias clases por ficha) | | ⬜ |
| 2 | Almacenamiento | Subida a S3 + manifiesto `jsonl` | | ⬜ |
| 3 | Extracción | Activar modelo en Bedrock y probar con 1 PDF | | ⬜ |
| 3 | Extracción | Esquema del Anexo A (`extraccion/esquema_kid.py`) | | 🟡 borrador |
| 3 | Extracción | Script por lotes `extraccion/extraer.py` | | ⬜ |
| 4 | Base de datos | Esquema SQL (`base_datos/schema.sql`) | | 🟡 borrador |
| 4 | Base de datos | Carga con upsert (sin duplicados) | | ⬜ |
| 5 | API | FastAPI en Lambda + Function URL | | ⬜ |
| 6 | App | Streamlit (tabla, filtros, gráficos explicados) | | ⬜ |
| 6 | App | Despliegue en ECS Express Mode | | ⬜ |
| 7 | IaC | Bucket de estado de Terraform + rol OIDC GitHub | | ⬜ |
| 7 | IaC | Terraform: S3 + Aurora (taller 1) | | ⬜ |
| 7 | IaC | Terraform: Lambda + ECS + permisos (taller 2) | | ⬜ |
| 7 | IaC | Workflow GitHub Actions (plan en PR, apply en main) | | ⬜ |
| 8 | Entrega | README final (arquitectura, decisiones, cómo desplegar, URLs) | | ⬜ |
| 8 | Entrega | `docs/resultados.md` con interpretación | | ⬜ |
| 8 | Entrega | Guion y ensayo de la exposición (5 min + demo) | | ⬜ |
| 8 | Entrega | `terraform destroy` **después** de la exposición | | ⬜ |

## Decisiones pendientes

| Decisión | Opciones | Quién / cuándo |
|---|---|---|
| Región de AWS | La que use el profesor (comprobar que el modelo de Bedrock está disponible allí) | Taller 1 |
| ¿Cuenta de AWS compartida o una por persona? | Afecta a cómo se configura OIDC y quién despliega | Grupo, ya |
| Modelo de Bedrock | El de la referencia del taller; para la ampliación, un segundo modelo | Taller 2 |
| ¿Las 3 gestoras o solo 2? | Mínimo 2 fuentes y 15 docs: decidir tras contar KIDs | Tras la inspección |
| Esquema SQL definitivo | Borrador en `base_datos/schema.sql` vs. el del taller | Taller 2 |
| ¿Campos extra además del Anexo A? | Divisa, objetivo de inversión, escenarios… | Tras tener el básico |

## Riesgos y cosas a vigilar

- **Coste de AWS:** Aurora y ECS pueden cobrar aunque no se usen. Poner una alerta de presupuesto (AWS Budgets)
  y destruir al acabar.
- **Las webs cambian:** si un scraper deja de encontrar enlaces, que falle con un mensaje claro.
- **Calendario corto:** 10 días hasta la entrega. Priorizar el pipeline completo antes que las ampliaciones.
- **Dudas del enunciado a confirmar con el profesor:**
  - Los mínimos aparecen como `[[2]]` fuentes y `[[15]]` documentos (¿son definitivos?).
  - El apartado 7 dice «cada estudiante deberá entregar», pero la práctica es por grupos: ¿una entrega por grupo?
  - Duración de la exposición: se habla de 5 + 5 min y de «10 minutos con demo»; entendemos 10 min en total.

## Bitácora

_Lo más nuevo arriba. Formato: `AAAA-MM-DD · persona · qué se hizo → qué queda`._

- 2026-11-22 · _(nombre)_ · Creado el repositorio: estructura de carpetas, `CLAUDE.md`, `ESTADO.md`, resumen del enunciado,
  arquitectura, glosario, registro de decisiones, plantilla de resultados, borradores de `esquema_kid.py` y `schema.sql`.
  → Queda: subir a GitHub, repartir tareas, inspeccionar las webs.
