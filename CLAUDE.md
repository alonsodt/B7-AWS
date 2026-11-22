# CLAUDE.md — Instrucciones para Claude (y para cualquier asistente de IA)

Este repositorio es la **Práctica B7 (Módulo Cloud) de un máster**: un pipeline en AWS que descarga
los KID (documentos de datos fundamentales) de fondos de inversión, extrae sus datos con un LLM de
Amazon Bedrock, los guarda en PostgreSQL y los muestra con una API y un dashboard.
Lo trabajamos **varias personas del grupo, cada una con su propio Claude**.

## 0. Antes de hacer nada

1. **Lee [`ESTADO.md`](ESTADO.md)**: qué está hecho, qué está en marcha, quién hace qué y qué decisiones hay tomadas.
2. Si la tarea toca algo que no conoces, mira [`docs/enunciado-resumen.md`](docs/enunciado-resumen.md)
   (requisitos y reglas) y [`docs/arquitectura.md`](docs/arquitectura.md).
3. Comprueba en `ESTADO.md` que **nadie más está trabajando en esa misma parte**. Si es así, avisa al usuario antes de tocarla.

## 1. El objetivo principal es APRENDER

Somos alumnos con **nivel básico** de programación, cloud e IA. Entregar algo que funcione no basta:
**cada miembro del grupo tiene que poder explicar cualquier parte en la exposición** (es una regla del enunciado).
Por eso:

- **Explica antes de escribir.** Antes de generar código nuevo, cuenta en 2–4 frases qué vas a hacer y por qué.
  Si aparece un concepto nuevo (OIDC, upsert, Function URL…), explícalo con palabras sencillas y, si hace falta,
  añádelo a [`docs/glosario.md`](docs/glosario.md).
- **Pasos pequeños.** Mejor varios cambios pequeños que se entienden que un bloque enorme. No generes ficheros
  de cientos de líneas de golpe.
- **Sin «magia».** Prefiere código simple y explícito a trucos avanzados (metaclases, decoradores propios,
  comprensiones anidadas, abstracciones innecesarias). Si algo avanzado es realmente necesario, explícalo.
- **Haz que el usuario participe.** Cuando sea razonable, propón que escriba él una parte o pregúntale si entiende
  lo que acabas de hacer. Al terminar una tarea, resume en lenguaje llano qué se ha hecho.
- **No ocultes errores.** Si algo falla o no lo has podido probar, dilo claramente.

## 2. Estilo de código

- **Idioma:** comentarios, docstrings, mensajes de log, documentación y commits **en español**.
  Nombres de variables y funciones en español también (`descargar_kid`, `fecha_descarga`), salvo nombres
  impuestos por librerías.
- **Python 3.11+**. Sigue PEP 8 a grandes rasgos; no hace falta ser purista.
- **Comentado a fondo** (más de lo habitual en un proyecto profesional, a propósito):
  - Cada fichero empieza con un docstring: qué hace, en qué fase del pipeline está, cómo se ejecuta.
  - Cada función tiene docstring con qué hace, parámetros y qué devuelve.
  - Los comentarios explican **el porqué**, no solo el qué. Ejemplo:

    ```python
    # Esperamos 1 segundo entre peticiones para no saturar la web de la gestora
    # (scraping responsable: tratamos su servidor como nos gustaría que trataran el nuestro).
    time.sleep(1)
    ```
  - Divide los scripts largos en secciones numeradas con comentarios (`# --- 1) Leer el manifiesto ---`).
- **Configuración por variables de entorno** (ver `.env.example`). Nada de valores de cuentas, ARNs o claves escritos en el código.
- Mensajes de error y logs comprensibles: que digan qué ha pasado y qué hacer.

## 3. Resultados: siempre interpretados

Cada vez que se produzca un resultado (nº de documentos descargados, precisión de la extracción, un gráfico,
una consulta), **acompáñalo de una interpretación en lenguaje sencillo**: qué significa, si es bueno o malo y por qué.
Incluye sus límites (p. ej. «con 20 fondos no podemos generalizar»). Las interpretaciones se recogen en
[`docs/resultados.md`](docs/resultados.md). En la app, cada gráfico lleva una frase explicativa.

## 4. Reglas OBLIGATORIAS del enunciado (no negociables)

1. **Salidas estructuradas de Bedrock.** La extracción usa un esquema JSON o una herramienta (tool) en modo estricto.
   **Prohibido** pedir «devuelve JSON» en el prompt y parsear el texto con `json.loads`.
2. **Sin credenciales en el repositorio — y el repositorio es PÚBLICO** (lo tiene que ver el profesor).
   Cualquier cosa que se suba la puede leer cualquiera, también en el historial. Detalle en [`docs/seguridad.md`](docs/seguridad.md).
   - Nunca escribas en ningún fichero del repo claves de AWS, contraseñas o tokens, ni siquiera «de prueba» o en un comentario.
   - Nunca añadas a Git `.env`, `*.tfstate`, `*.tfvars` con valores reales, ni uses `git add -f` para saltarte el `.gitignore`.
   - IDs de cuenta, ARNs y nombres de buckets: por variables de entorno (`.env`) o variables de GitHub, no fijos en el código.
   - GitHub Actions entra en AWS por **OIDC** (rol restringido a este repo y a `main`). Nunca propongas crear secretos
     `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`.
   - Antes de cada commit revisa `git diff --staged`. Si ves algo parecido a una credencial, **para y avisa**.
3. **Datos no públicos** salvo por la API y la app: bucket S3 privado, base de datos sin acceso público.
   Por eso **no se suben al repo** los PDF ni los datos extraídos (`.jsonl`, `.csv`…); en `docs/resultados.md`
   solo van números agregados y tablas de evaluación.
4. **Si un campo no aparece en el KID → `null`.** El modelo no debe inventar. El esquema vive en
   [`extraccion/esquema_kid.py`](extraccion/esquema_kid.py) y es la **fuente de verdad** de los campos:
   si lo cambias, avisa de que afecta a `base_datos/`, `api/` y `app/` y apúntalo en `ESTADO.md`.
5. **Sin duplicados** en la base de datos si un documento se procesa dos veces (upsert por SHA-256 del PDF).
6. **Scraping responsable:** respetar `robots.txt`, pausa entre peticiones, User-Agent genérico del proyecto, no re-descargar.

## 5. Pasos que hace una persona, no la IA

Hay pasos manuales (cuenta de AWS, bootstrap de OIDC, alerta de presupuesto, configuración de GitHub,
revisión manual de KIDs, entrega). Están en [`docs/pasos-manuales.md`](docs/pasos-manuales.md).
Puedes **guiar** al usuario en ellos, pero no introduzcas credenciales, no aceptes condiciones y no
cambies la configuración de la cuenta por él.

## 6. AWS cuesta dinero: cuidado

- **No ejecutes `terraform apply`, `terraform destroy` ni comandos que creen/borren recursos en AWS sin confirmación
  explícita del usuario.** `terraform plan`, `terraform validate` y `terraform fmt` sí se pueden lanzar.
- Antes de proponer un recurso nuevo, menciona si tiene coste fijo (p. ej. Aurora, ECS, NAT Gateway) y si hay alternativa más barata.
- No lances extracciones masivas con Bedrock sin avisar: primero 1–2 PDF de prueba.
- Recuerda al grupo hacer `terraform destroy` después de la exposición.

## 7. Cómo trabajamos en equipo (Git)

- `main` siempre debe funcionar. Cada tarea en su **rama**: `<nombre>/<tarea>` (p. ej. `ana/scraper-cobas`).
- Cambios a `main` mediante **pull request**; otra persona del grupo lo revisa (y así también aprende esa parte).
- Commits pequeños, en español, en imperativo: `Añade scraper de Azvalor`.
- No hagas `push --force` a `main` ni reescribas historia compartida.
- Si tu tarea necesita tocar la carpeta de otro compañero, díselo al usuario para que lo coordine.

## 8. Al terminar una tarea → actualiza ESTADO.md

Es la forma de que el resto del grupo (y sus Claudes) sepan por dónde vamos:

1. Marca la tarea en la tabla de fases (`⬜` pendiente → `🟡` en curso → `✅` hecha).
2. Añade una línea en la **Bitácora** (lo más nuevo arriba): fecha, quién, qué se hizo, qué queda.
3. Si se ha tomado una decisión de diseño, regístrala en [`docs/decisiones.md`](docs/decisiones.md) (con el porqué)
   y quítala de «Decisiones pendientes».

## 9. Mapa del repositorio

| Ruta | Contenido |
|---|---|
| `ESTADO.md` | Estado del proyecto, reparto de tareas, decisiones pendientes, bitácora |
| `README.md` | README de la **entrega** (arquitectura, decisiones, cómo desplegar, URLs, integrantes) |
| `docs/` | Resumen del enunciado, arquitectura, decisiones, glosario, resultados, **seguridad**, **pasos manuales** |
| `scraper/` | Fase 1–2: captura de KIDs y subida a S3 + manifiesto |
| `extraccion/` | Fase 3: extracción con Bedrock (`esquema_kid.py` = esquema del Anexo A) |
| `base_datos/` | Fase 4: esquema SQL y carga en PostgreSQL |
| `api/` | Fase 5: FastAPI en Lambda |
| `app/` | Fase 6: dashboard Streamlit |
| `infra/` | Fase 7: Terraform |
| `.github/workflows/` | GitHub Actions (despliegue) |
| `datos/` | Copias locales (PDF, manifiestos). **Ignorada por Git** |

## 10. Comandos útiles

```bash
# Entorno virtual e instalación (desde la raíz del repo)
python -m venv .venv
# Windows:  .venv\Scripts\activate      ·  macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt

# Probar el esquema del KID
python extraccion/esquema_kid.py

# Terraform (solo lectura; apply SOLO con confirmación)
cd infra && terraform fmt && terraform validate && terraform plan
```
