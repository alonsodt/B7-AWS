# ESTADO del proyecto

> **Última actualización:** 2026-11-22 · **por:** Alonso
>
> Este fichero es el «tablero» del grupo. Léelo antes de empezar y actualízalo al terminar
> (instrucciones en [CLAUDE.md §8](CLAUDE.md#8-al-terminar-una-tarea--actualiza-estadomd)).

## En una frase

Repositorio creado con la estructura, las normas de trabajo, las medidas de seguridad para repo público
y los borradores del esquema de datos. **Todavía no hay código del pipeline ni nada desplegado en AWS.**
Siguiente paso: subir el repo (público), hacer los pasos manuales de AWS/GitHub
([docs/pasos-manuales.md](docs/pasos-manuales.md)) e inspeccionar las webs.

> ⚠️ **El repositorio es PÚBLICO** (lo tiene que ver el profesor). Antes de tu primer commit lee
> [docs/seguridad.md](docs/seguridad.md): nada de claves, `.env`, `*.tfstate` ni datos de los KID en Git.

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
| Alonso | `alonsodt` | _por decidir (A, B o C)_ | _por decidir_ |
| Pietro | _pendiente_ | _por decidir_ | _por decidir_ |
| Raúl | _pendiente_ | _por decidir_ | _por decidir_ |

**Propuesta de reparto por capas** para 3 personas (cada bloque toca un trozo de Terraform, así nadie se queda sin aprender infraestructura):

- **A · Captura + base:** scrapers de las gestoras, subida a S3, manifiesto + Terraform de S3/Aurora y bootstrap OIDC (taller 1).
- **B · Extracción IA + datos:** script de Bedrock, validación, evaluación de calidad, esquema SQL y carga sin duplicados.
- **C · API + app + despliegue:** FastAPI en Lambda, Streamlit en ECS, workflows de GitHub Actions.

Revisión cruzada de pull requests en rueda: A revisa a B, B revisa a C, C revisa a A.

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
| 0 | Organización | Medidas de seguridad para repo público (`.gitignore`, gitleaks, guía) | Alonso | ✅ |
| 0 | Organización | Subir a GitHub (**público**): https://github.com/alonsodt/B7-AWS | Alonso | ✅ |
| 0 | Organización | Invitar a Pietro y Raúl como colaboradores | Alonso | ⬜ |
| 0 | Organización | Proteger `main` (push protection y secret scanning ya activos ✅) ([pasos manuales §C](docs/pasos-manuales.md#c-github-lo-hace-quien-cree-el-repo)) | | ⬜ |
| 0 | Organización | Cada uno: email *noreply* en Git y herramientas instaladas ([§A](docs/pasos-manuales.md#a-preparar-el-ordenador-de-cada-integrante-cada-uno-una-vez)) | Todos | ⬜ |
| 0 | Organización | Decidir el reparto (A/B/C) | Todos | ⬜ |
| 0 | AWS | Alerta de presupuesto + acceso al modelo de Bedrock ([§B](docs/pasos-manuales.md#b-aws-lo-hace-una-persona-en-la-cuenta-que-usemos)) | | ⬜ |
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

- **Repo público:** una clave subida por error queda en el historial aunque se borre. Si pasa: desactivarla en AWS
  al momento ([docs/seguridad.md](docs/seguridad.md#si-se-sube-una-clave-por-error)). El rol de OIDC debe estar restringido a este repo y a `main`.
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

- 2026-11-22 · Alonso · Repo publicado en https://github.com/alonsodt/B7-AWS (público). Workflow `secretos` en verde (4 commits revisados, sin fugas).
  → Queda: invitar a Pietro y Raúl, proteger `main`, pasos manuales de AWS, decidir reparto.

- 2026-11-22 · Alonso · Integrantes: Alonso, Pietro y Raúl. El repo será **público** → añadidos `docs/seguridad.md`,
  `docs/pasos-manuales.md`, workflow `secretos.yml` (gitleaks), `.gitignore` ampliado a datos, normas de seguridad en `CLAUDE.md`.
  → Queda: subir a GitHub, pasos manuales de AWS/GitHub, decidir reparto.
- 2026-11-22 · Alonso · Creado el repositorio: estructura de carpetas, `CLAUDE.md`, `ESTADO.md`, resumen del enunciado,
  arquitectura, glosario, registro de decisiones, plantilla de resultados, borradores de `esquema_kid.py` y `schema.sql`.
  → Queda: subir a GitHub, repartir tareas, inspeccionar las webs.
