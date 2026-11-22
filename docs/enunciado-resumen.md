# Resumen del enunciado — Práctica B7 (Módulo Cloud)

> **Pipeline de datos de fondos: del KID al dashboard en AWS**
>
> Este fichero es un resumen con nuestras palabras. El enunciado original está en el aula virtual
> (`Practica_KID_AWS.docx`). Si hay dudas, manda el original.

## Datos básicos

| Qué | Detalle |
|---|---|
| Tipo | Práctica **por grupos** |
| Talleres | T1 y T2: el profesor construye una solución de referencia paso a paso. T3: exposición |
| Entrega | **2/12/2026**, por el aula virtual |
| Exposición | Taller 3: 5 min de exposición + 5 min de preguntas, **con demo en directo** |

**Qué se entrega:**

1. Enlace al repositorio de GitHub (compartido con el profesor) con la solución desplegada en AWS.
   El README debe explicar **arquitectura, decisiones tomadas y cómo desplegar**.
2. URL de la aplicación web y URL de la API.
3. Nombres de las personas del grupo.
4. La exposición en el taller 3 (demo + reflexión sobre decisiones y dificultades).

## Objetivo (lo que tenemos que saber hacer al final)

1. Descargar documentos de forma automatizada y **responsable** (web scraping).
2. Guardarlos en la nube con una organización y metadatos coherentes.
3. Extraer datos de un PDF con un LLM de **Amazon Bedrock usando salidas estructuradas** (la respuesta cumple un esquema).
4. Modelar y cargar los datos en **PostgreSQL en AWS**.
5. Servir los datos con una **API** y verlos en una **aplicación web**.
6. Definir la infraestructura con **Terraform** y desplegarla desde **GitHub Actions**.

## El problema

Cada clase de un fondo vendido a minoristas en la UE publica un **KID** (Documento de Datos Fundamentales,
~3 páginas). Algunas gestoras españolas lo siguen llamando «DFI» o «datos fundamentales».
Contiene: nombre del producto y clase, ISIN, gestora, indicador de riesgo SRI (1–7), periodo de
mantenimiento recomendado, escenarios de rentabilidad y costes. La información está «encerrada» en
PDFs con formatos distintos en cada web. Hay que automatizar: **capturar → extraer con IA → base de
datos → API → dashboard**.

## Fuentes propuestas

| Gestora | Punto de entrada | Dónde está el KID | Dificultad |
|---|---|---|---|
| Bestinver | https://www.bestinver.es/fondos-de-inversion/ | Ficha de cada fondo → enlace «Datos fundamentales». Una clase por ficha | Baja |
| Azvalor | https://www.azvalor.com/fondos/ | Ficha → «Folleto simplificado (DFP)». El nombre del PDF lleva la fecha: **hay que leer la URL del HTML** | Media |
| Cobas AM | https://www.cobasam.com/productos/ | Ficha con un bloque por clase (A, B, C, D), cada una con su ISIN y enlace «PRIIP pdf» | Media-alta |

Se pueden usar otras fuentes públicas (otras gestoras, plataformas, CNMV). Las webs pueden cambiar:
detectarlo y adaptarse es parte de la práctica.

## Tareas obligatorias (requisitos mínimos)

| # | Fase | Requisito |
|---|---|---|
| 1 | Captura | KIDs de **al menos 2 fuentes** y **mínimo 15 documentos**. Guardar de dónde viene cada uno y cuándo se descargó |
| 2 | Almacenamiento | PDFs en **Amazon S3** |
| 3 | Extracción IA | Como mínimo los campos del Anexo A, con **Bedrock + salidas estructuradas** |
| 4 | Base de datos | **PostgreSQL en AWS**, **sin duplicados** si un documento se procesa dos veces |
| 5 | API | API HTTP que exponga los datos |
| 6 | Visualización | Web que muestre los datos y permita explorarlos |
| 7 | IaC | Infraestructura en **Terraform**, desplegada desde **GitHub Actions** |

> En el documento original los números «2» y «15» aparecen entre dobles corchetes (`[[2]]`, `[[15]]`),
> como si fueran variables de plantilla. Conviene confirmar con el profesor que son los valores definitivos.

### Ampliaciones (suman nota)

- Webs que necesitan JavaScript (Playwright).
- Arquitectura por eventos (S3 → Lambda).
- Comparar la calidad de extracción de varios modelos.
- Medir la precisión con un conjunto de KIDs revisados a mano.
- Tests y validaciones en el pipeline de GitHub.
- Alertas cuando cambia un KID.
- Buscador en lenguaje natural sobre los datos.

## Reglas (las únicas obligatorias)

1. **Salidas estructuradas de Bedrock** (esquema JSON o herramientas en modo estricto).
   **Prohibido** pedir «devuélveme JSON» en el prompt y parsear el texto. El modelo es libre.
2. **Sin credenciales en el repositorio.**
3. Datos y documentos **no públicos**, salvo a través de la API y la aplicación.
4. Se permite Claude Code y similares, **pero cada uno debe poder explicar cualquier parte**.

Todo lo demás (lenguaje, librerías, servicios, diseño) es libre si se justifica.

## Arquitectura de referencia de los talleres

| Capa | Referencia | Alternativas válidas |
|---|---|---|
| Captura | Python + requests + BeautifulSoup | Scrapy, Playwright, otros lenguajes |
| Almacenamiento | Amazon S3 | — |
| Extracción | Bedrock (Converse API) con salidas estructuradas, script por lotes | Lambda disparada por S3, Step Functions, otro modelo |
| Base de datos | Aurora PostgreSQL Serverless v2 + RDS Data API | RDS PostgreSQL, conexión directa por VPC |
| API | FastAPI en AWS Lambda con Function URL | API Gateway, Flask, contenedor en ECS |
| Visualización | Streamlit en Amazon ECS Express Mode | Dash, Panel, React, otro despliegue |
| Despliegue | Terraform + GitHub Actions (OIDC, estado en S3) | Estructura de módulos y flujos libre |

### Talleres

- **Taller 1 – Captura e infraestructura base:** inspección de webs, scraper, manifiesto, repo plantilla,
  conexión GitHub–AWS, primer despliegue con Terraform (bucket + base de datos).
- **Taller 2 – IA, datos y aplicación:** extracción con Bedrock, carga en PostgreSQL, API y app desplegadas desde GitHub Actions.
- **Taller 3 – Exposición.**

## Anexo A — Campos mínimos a extraer de cada KID

Si un campo no aparece en el documento → `null`. **El modelo no debe inventarlo.**
Se pueden añadir más campos (escenarios, distribución de activos, objetivo, divisa…).

| Campo | Tipo | Descripción |
|---|---|---|
| `isin` | texto (12 caracteres) | Código ISIN de la clase |
| `nombre_producto` | texto | Nombre del fondo tal y como aparece en el KID |
| `nombre_clase` | texto (opcional) | Clase o serie («Clase C», «P Acc EUR»…) |
| `gestora` | texto | Productor del PRIIP / sociedad gestora |
| `fecha_documento` | fecha (opcional) | Fecha de validez del KID |
| `sri` | entero 1–7 | Indicador resumido de riesgo |
| `periodo_mantenimiento_anios` | número (opcional) | Periodo de mantenimiento recomendado, en años |
| `gastos_corrientes_pct` | número (opcional) | Comisiones de gestión y otros costes, % anual |
| `costes_entrada_pct` | número (opcional) | Costes de entrada, % |
| `costes_salida_pct` | número (opcional) | Costes de salida, % |

La implementación de este esquema está en [`extraccion/esquema_kid.py`](../extraccion/esquema_kid.py).
