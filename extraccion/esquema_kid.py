"""
esquema_kid.py — El "contrato" de datos de un KID.

¿Qué es esto?
-------------
Es la definición, en formato JSON Schema, de los campos que queremos sacar de cada
PDF de un KID (los campos mínimos del Anexo A del enunciado).

¿Por qué es tan importante?
---------------------------
Este esquema lo usan TODAS las piezas del proyecto, así que es la "fuente de verdad":

  1. Extracción: se lo pasamos a Amazon Bedrock para que el modelo esté OBLIGADO a
     responder con exactamente estos campos y tipos (eso es una "salida estructurada").
  2. Base de datos: las columnas de la tabla `kid` (base_datos/schema.sql) siguen estos campos.
  3. API y app: devuelven / muestran estos mismos campos.

⚠️  Si cambias algo aquí (añadir, renombrar o quitar un campo), AVISA al grupo y apúntalo
    en ESTADO.md, porque probablemente haya que tocar también la base de datos, la API y la app.

¿Qué es JSON Schema?
--------------------
Un estándar para describir "cómo tiene que ser" un JSON: qué claves tiene, de qué tipo
es cada una (texto, número, entero...) y qué restricciones cumple (p. ej. un SRI entre 1 y 7).
Más info: https://json-schema.org/learn/getting-started-step-by-step

Decisiones de diseño (explicadas)
---------------------------------
* TODOS los campos admiten `null`.
  El enunciado dice: "si un campo no aparece en el documento debe quedar vacío (null):
  el modelo no debe inventarlo". Si obligáramos a que, por ejemplo, `sri` fuera siempre un
  entero, en un PDF raro el modelo se vería forzado a inventarse un número. Preferimos que
  diga `null` y luego detectarlo nosotros (ver `CAMPOS_IMPRESCINDIBLES` más abajo).

* TODOS los campos están en `required`.
  Parece contradictorio con lo anterior, pero no lo es: `required` obliga a que la CLAVE
  aparezca en la respuesta; `null` permite que su VALOR esté vacío. Así el modelo tiene que
  "pronunciarse" sobre cada campo (o lo encuentra, o dice explícitamente null).
  Además, los modos estrictos de salida estructurada suelen exigir que todo esté en `required`.

* `additionalProperties: False`.
  El modelo no puede añadir claves que no hemos pedido.

* Las restricciones `pattern`, `minimum`, `maximum`...
  Algunos modelos / modos estrictos de Bedrock NO admiten todas las palabras clave de
  JSON Schema. Si Bedrock da error con el esquema, prueba a quitar esas restricciones del
  esquema que se envía al modelo y compruébalas después en Python (función `validar_kid`).
  → Comprobar en la documentación actual de Bedrock qué soporta el modelo elegido.

* Porcentajes como número "en puntos porcentuales".
  "1,25 %" se guarda como 1.25 (no como 0.0125). Lo decimos en la descripción del campo
  porque el modelo LEE esas descripciones y las usa como instrucciones.
"""

# ---------------------------------------------------------------------------
# 1) El esquema JSON
# ---------------------------------------------------------------------------
# Truco: la "description" de cada campo no es solo documentación para nosotros.
# El modelo de lenguaje también la lee, así que escribirla bien mejora la extracción.

ESQUEMA_KID = {
    "type": "object",
    "properties": {
        "isin": {
            # ["string", "null"] significa: "puede ser texto o puede ser null".
            "type": ["string", "null"],
            "description": (
                "Código ISIN de la clase del fondo: 12 caracteres, 2 letras de país "
                "seguidas de 9 caracteres alfanuméricos y 1 dígito de control. "
                "Ejemplo de formato: ES0000000000. null si no aparece."
            ),
            # Expresión regular que describe un ISIN válido (formato, no dígito de control).
            "pattern": "^[A-Z]{2}[A-Z0-9]{9}[0-9]$",
        },
        "nombre_producto": {
            "type": ["string", "null"],
            "description": "Nombre del fondo tal y como aparece en el KID, sin la clase.",
        },
        "nombre_clase": {
            "type": ["string", "null"],
            "description": (
                "Clase o serie de participación, p. ej. 'Clase C' o 'P Acc EUR'. "
                "null si el documento no menciona ninguna clase."
            ),
        },
        "gestora": {
            "type": ["string", "null"],
            "description": "Productor del PRIIP / sociedad gestora del fondo.",
        },
        "fecha_documento": {
            "type": ["string", "null"],
            "description": (
                "Fecha de validez o de elaboración del KID en formato ISO AAAA-MM-DD. "
                "null si no aparece."
            ),
            # "format": "date" lo entienden algunos validadores; es orientativo.
            "format": "date",
        },
        "sri": {
            "type": ["integer", "null"],
            "description": (
                "Indicador resumido de riesgo (SRI): número entero del 1 (riesgo más bajo) "
                "al 7 (riesgo más alto). Suele aparecer como una escala de 1 a 7 con "
                "una casilla marcada."
            ),
            "minimum": 1,
            "maximum": 7,
        },
        "periodo_mantenimiento_anios": {
            "type": ["number", "null"],
            "description": (
                "Período de mantenimiento recomendado, expresado en años "
                "(p. ej. '5 años' -> 5). null si no aparece."
            ),
        },
        "gastos_corrientes_pct": {
            "type": ["number", "null"],
            "description": (
                "Comisiones de gestión y otros costes administrativos o de funcionamiento, "
                "en % anual expresado en puntos porcentuales (1,25 % -> 1.25). null si no aparece."
            ),
        },
        "costes_entrada_pct": {
            "type": ["number", "null"],
            "description": (
                "Costes de entrada en % (puntos porcentuales; 0 % -> 0). "
                "null si el documento no lo indica."
            ),
        },
        "costes_salida_pct": {
            "type": ["number", "null"],
            "description": (
                "Costes de salida en % (puntos porcentuales; 0 % -> 0). "
                "null si el documento no lo indica."
            ),
        },
    },
    # Todas las claves deben aparecer en la respuesta (aunque sea con valor null).
    "required": [
        "isin",
        "nombre_producto",
        "nombre_clase",
        "gestora",
        "fecha_documento",
        "sri",
        "periodo_mantenimiento_anios",
        "gastos_corrientes_pct",
        "costes_entrada_pct",
        "costes_salida_pct",
    ],
    # No se permiten claves extra.
    "additionalProperties": False,
}


# ---------------------------------------------------------------------------
# 2) Campos que, aunque el esquema permita null, esperamos encontrar SIEMPRE
# ---------------------------------------------------------------------------
# En el Anexo A no son "opcionales". Si salen a null, el documento merece una
# revisión a mano (puede que el PDF sea raro o que la extracción haya fallado).
CAMPOS_IMPRESCINDIBLES = ["isin", "nombre_producto", "gestora", "sri"]


# ---------------------------------------------------------------------------
# 3) Validación en Python (segunda comprobación, después de Bedrock)
# ---------------------------------------------------------------------------
def validar_kid(datos: dict) -> list[str]:
    """
    Comprueba un KID ya extraído y devuelve una lista de avisos (vacía si todo está bien).

    ¿Por qué validar otra vez si Bedrock ya usa el esquema?
      - Por si hemos tenido que quitar restricciones (pattern, minimum...) del esquema
        enviado al modelo porque no las soportaba.
      - Para detectar campos imprescindibles que han salido a null.
      - Porque "confía, pero verifica" es buena práctica en cualquier pipeline de datos.

    Parámetros
    ----------
    datos : dict
        Diccionario con los campos del KID (la respuesta del modelo).

    Devuelve
    --------
    list[str]
        Mensajes de aviso en español. Lista vacía = sin problemas.
    """
    # Importamos aquí dentro para que el resto del módulo funcione aunque
    # no esté instalada la librería (solo hace falta para validar).
    import jsonschema  # pip install jsonschema

    avisos = []

    # 3.1) ¿Cumple el esquema (tipos, rangos, formato del ISIN...)?
    validador = jsonschema.Draft202012Validator(ESQUEMA_KID)
    for error in validador.iter_errors(datos):
        # error.path indica en qué campo está el problema.
        campo = ".".join(str(p) for p in error.path) or "(raíz)"
        avisos.append(f"Esquema: campo '{campo}': {error.message}")

    # 3.2) ¿Faltan campos imprescindibles?
    for campo in CAMPOS_IMPRESCINDIBLES:
        if datos.get(campo) is None:
            avisos.append(f"Revisar a mano: el campo imprescindible '{campo}' ha salido vacío (null)")

    return avisos


# ---------------------------------------------------------------------------
# 4) Prueba rápida: `python extraccion/esquema_kid.py`
# ---------------------------------------------------------------------------
# Este bloque solo se ejecuta si lanzas el fichero directamente (no al importarlo).
if __name__ == "__main__":
    import json

    # Ejemplo INVENTADO (no es un fondo real) solo para ver cómo funciona la validación.
    ejemplo_correcto = {
        "isin": "ES0000000001",
        "nombre_producto": "Fondo de Ejemplo FI",
        "nombre_clase": None,
        "gestora": "Gestora de Ejemplo SGIIC",
        "fecha_documento": "2026-01-01",
        "sri": 4,
        "periodo_mantenimiento_anios": 5,
        "gastos_corrientes_pct": 1.25,
        "costes_entrada_pct": 0,
        "costes_salida_pct": 0,
    }
    # Mismo ejemplo con dos errores: SRI fuera de rango y sin gestora.
    ejemplo_con_errores = {**ejemplo_correcto, "sri": 9, "gestora": None}

    print("Esquema que se enviará a Bedrock:")
    print(json.dumps(ESQUEMA_KID, indent=2, ensure_ascii=False))
    # (Sin emojis en los print: la consola de Windows a veces no sabe mostrarlos y da error.)
    print("\nAvisos del ejemplo correcto:", validar_kid(ejemplo_correcto) or "ninguno (OK)")
    print("Avisos del ejemplo con errores:")
    for aviso in validar_kid(ejemplo_con_errores):
        print("  -", aviso)
