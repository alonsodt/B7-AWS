# Glosario (nivel básico)

Términos que salen en la práctica, explicados en una o dos frases. Si aparece uno nuevo, añadidlo.

## Finanzas / fondos

| Término | Qué es |
|---|---|
| **Fondo de inversión** | Bolsa común de dinero de muchos inversores que gestiona una gestora profesional. |
| **Gestora (SGIIC)** | La empresa que gestiona el fondo (Bestinver, Azvalor, Cobas…). En el KID aparece como «productor del PRIIP». |
| **Clase de un fondo** | Variante del mismo fondo con condiciones distintas (comisiones, inversión mínima). Cada clase tiene su ISIN y su KID. |
| **ISIN** | Código de 12 caracteres que identifica un valor/clase de forma única. Empieza por el país (ES, LU, IE…). |
| **KID / DFI / DFP** | Documento de Datos Fundamentales: resumen obligatorio de ~3 páginas con riesgo, costes y escenarios. |
| **PRIIP** | Nombre regulatorio europeo de los productos de inversión «empaquetados» para minoristas. El KID es el documento PRIIP. |
| **SRI** | Indicador resumido de riesgo: escala de 1 (menos riesgo) a 7 (más riesgo). |
| **Periodo de mantenimiento recomendado** | Cuánto tiempo aconseja la gestora mantener la inversión (p. ej. 5 años). |
| **Gastos corrientes** | Lo que cuesta cada año tener el fondo (comisión de gestión + otros gastos), en % del dinero invertido. |
| **Costes de entrada / salida** | Comisión que se cobra al invertir / al retirar el dinero. En muchos fondos es 0 %. |
| **UCITS** | Normativa europea de fondos armonizados. Antes usaban el KIID; desde 2023 usan el KID. |

## Datos e IA

| Término | Qué es |
|---|---|
| **Web scraping** | Programa que visita páginas web y extrae información (aquí, enlaces a PDF). |
| **robots.txt** | Fichero de cada web que indica qué partes pueden visitar los robots. Hay que respetarlo. |
| **Manifiesto** | Nuestro «inventario» de PDF descargados: de dónde viene cada uno y cuándo se bajó. |
| **Hash / SHA-256** | Huella digital de un fichero. Mismo contenido → misma huella. Sirve para detectar duplicados. |
| **LLM** | Modelo de lenguaje grande (como Claude). Lee texto/PDF y genera respuestas. |
| **Amazon Bedrock** | Servicio de AWS para usar LLMs de varios proveedores mediante una API. |
| **Converse API** | La forma unificada de «hablar» con cualquier modelo de Bedrock. |
| **Salida estructurada** | Hacer que el modelo responda siguiendo un esquema obligatorio, no texto libre. |
| **JSON Schema** | Estándar para describir cómo debe ser un JSON (campos, tipos, restricciones). |
| **Tool use (herramientas)** | El modelo «llama» a una función que definimos; los argumentos deben cumplir su esquema. Se usa para forzar salida estructurada. |

## AWS y despliegue

| Término | Qué es |
|---|---|
| **S3** | Almacenamiento de ficheros de AWS. Los ficheros («objetos») se guardan en «buckets». |
| **Aurora PostgreSQL Serverless v2** | Base de datos PostgreSQL gestionada por AWS que sube y baja de capacidad según la carga. |
| **RDS Data API** | Permite lanzar SQL a Aurora por HTTPS con permisos IAM, sin gestionar conexiones ni redes. |
| **Lambda** | Ejecuta código sin servidor propio: solo se paga mientras se ejecuta. |
| **Function URL** | URL HTTPS que invoca directamente una Lambda. |
| **FastAPI** | Librería de Python para crear APIs web de forma rápida. |
| **Streamlit** | Librería de Python para hacer dashboards web con poco código. |
| **ECS Express Mode** | Forma simplificada de ejecutar un contenedor Docker en AWS con una URL pública. |
| **IAM** | Sistema de usuarios, roles y permisos de AWS. |
| **Terraform** | Herramienta de «infraestructura como código»: describes los recursos en ficheros y ella los crea. |
| **GitHub Actions** | Automatizaciones que se ejecutan en GitHub al hacer push o pull request (CI/CD). |
| **OIDC** | Mecanismo para que GitHub Actions obtenga permisos temporales en AWS sin guardar claves. |
| **CI/CD** | Integración y despliegue continuos: probar y desplegar automáticamente cada cambio. |
