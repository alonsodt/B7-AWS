# Registro de decisiones

El enunciado permite seguir la solución de referencia o cambiar piezas **siempre que se justifique**,
y el README final debe explicar las decisiones. Aquí las vamos apuntando según las tomamos
(así en la exposición tenemos la «reflexión sobre decisiones y dificultades» ya escrita).

**Formato:** una entrada por decisión. Lo más nuevo arriba. Explicado de forma que lo entienda alguien
que no estaba en la conversación.

---

## D-005 · Repositorio público con defensa en capas contra fugas de secretos · 2026-11-22 · _decidida_

- **Contexto:** el profesor tiene que ver el repositorio, así que será **público**. Cualquiera puede leer el código y
  todo su historial, y hay robots que buscan claves de AWS en GitHub.
- **Decisión:** (1) OIDC para GitHub Actions, sin claves permanentes; (2) `.gitignore` que excluye credenciales, estado de
  Terraform y datos; (3) push protection de GitHub; (4) workflow `secretos.yml` con gitleaks en cada push/PR;
  (5) commits con el email *noreply* de GitHub. Detalle en [seguridad.md](seguridad.md).
- **Por qué:** una sola medida puede fallar (un `git add -f`, una clave pegada en un `.py`); varias juntas hacen muy difícil
  que una fuga pase desapercibida. Además, el workflow de gitleaks cuenta como «validaciones en el pipeline de GitHub» (ampliación).

## D-004 · Todos los campos del esquema admiten `null` · 2026-11-22 · _propuesta_

- **Contexto:** el Anexo A exige que, si un dato no aparece, quede vacío y el modelo no lo invente.
- **Decisión:** en `extraccion/esquema_kid.py` todos los campos son `tipo | null` y todos están en `required`.
  Los imprescindibles (`isin`, `nombre_producto`, `gestora`, `sri`) se revisan después en Python y, si salen
  a `null`, se marcan para revisión manual.
- **Por qué:** si forzamos un tipo sin `null`, ante un PDF raro el modelo tendría que inventarse un valor.
- **Alternativa descartada:** hacer obligatorios (sin null) los imprescindibles.

## D-003 · Evitar duplicados con la huella SHA-256 del PDF · 2026-11-22 · _propuesta_

- **Contexto:** requisito «evitar duplicados si un documento se procesa dos veces».
- **Decisión:** cada PDF se identifica por el SHA-256 de su contenido (`UNIQUE` en la tabla `documentos`)
  y se inserta con `INSERT ... ON CONFLICT`. Borrador en `base_datos/schema.sql`.
- **Por qué:** la URL puede cambiar aunque el PDF sea el mismo (y al revés: misma URL con un PDF nuevo).
  El contenido es lo que de verdad identifica al documento.

## D-002 · Manifiesto en formato JSON Lines · 2026-11-22 · _propuesta_

- **Decisión:** un `manifiesto.jsonl` con una línea por PDF (formato en `scraper/README.md`).
- **Por qué:** es fácil de leer, de añadir líneas y de cargar con pandas (`pd.read_json(..., lines=True)`).

## D-001 · Seguimos la arquitectura de referencia de los talleres · 2026-11-22 · _propuesta_

- **Decisión:** Python + requests/BS4 → S3 → Bedrock (Converse) → Aurora PostgreSQL Serverless v2 (Data API)
  → FastAPI en Lambda → Streamlit en ECS Express → Terraform + GitHub Actions (OIDC).
- **Por qué:** el objetivo principal es aprender; seguir lo que explica el profesor nos permite entender cada
  pieza y pedir ayuda en clase. Solo nos desviaremos si encontramos un motivo claro (y lo apuntaremos aquí).

---

## Decisiones pendientes

Las decisiones abiertas se listan en [ESTADO.md](../ESTADO.md#decisiones-pendientes).
