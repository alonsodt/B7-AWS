# extraccion/ — Fase 3: Extracción con IA (Amazon Bedrock)

**Qué hace:** para cada PDF del manifiesto, se lo envía a un modelo de Amazon Bedrock y obtiene
los campos del Anexo A **con salida estructurada**, es decir, el modelo está obligado a responder
siguiendo el esquema de [`esquema_kid.py`](esquema_kid.py).

**Referencia del taller:** Bedrock **Converse API**, en un script por lotes (procesa todos los PDF de una vez).

## La regla clave del enunciado

> ❌ NO vale: escribir en el prompt «devuélveme un JSON con estos campos» y luego hacer `json.loads(texto)`.
>
> ✅ SÍ vale: usar la **salida estructurada** de Bedrock: pasar un esquema JSON o definir una
> «herramienta» (tool) en modo estricto cuyo `inputSchema` sea nuestro esquema y forzar al modelo a usarla.

¿Por qué? Con un prompt el modelo *suele* hacer caso, pero puede devolver texto extra, claves mal
escritas o tipos incorrectos. Con salida estructurada la respuesta **cumple el esquema por diseño**.

## Pasos previos en AWS

- [ ] Activar el acceso al modelo elegido en la consola de Bedrock (región que usemos).
- [ ] Comprobar en la documentación de Bedrock que ese modelo soporta salidas estructuradas / tool use estricto
      y si admite documentos PDF directamente en la Converse API.

## Ficheros

| Fichero | Qué es | Estado |
|---|---|---|
| `esquema_kid.py` | Esquema JSON del Anexo A + validación en Python | ✅ Borrador listo |
| `extraer.py` | Script por lotes: lee manifiesto → llama a Bedrock → guarda resultados | ⬜ Pendiente (taller 2) |

Prueba rápida del esquema (necesita `pip install jsonschema`):

```bash
python extraccion/esquema_kid.py
```

## Evaluar la calidad (resultados interpretados)

Cuando tengamos extracciones, revisar a mano 5–10 KID y anotar en `docs/resultados.md`:
qué campos acierta siempre, cuáles falla y **por qué creemos que falla** (explicado de forma sencilla).
Esto además es una de las ampliaciones que puntúan.
