# Pipeline de datos de fondos: del KID al dashboard en AWS

Práctica B7 · Módulo Cloud · Máster

> 🚧 **En construcción.** Este README es el de la **entrega final** y se irá completando.
> El estado del trabajo está en [ESTADO.md](ESTADO.md). Las normas para trabajar (personas y Claudes) en [CLAUDE.md](CLAUDE.md).

## Integrantes

- Alonso _(apellidos)_
- Pietro _(apellidos)_
- Raúl _(apellidos)_

## URLs

| Servicio | URL |
|---|---|
| Aplicación web | _pendiente_ |
| API | _pendiente_ (documentación interactiva en `<url>/docs`) |

## Qué hace

Descarga automáticamente los KID (Documentos de Datos Fundamentales) de fondos de varias gestoras españolas,
extrae sus datos clave (ISIN, riesgo SRI, costes…) con un modelo de IA de Amazon Bedrock usando salidas
estructuradas, los guarda en PostgreSQL y los ofrece mediante una API y un dashboard web.
Toda la infraestructura se define con Terraform y se despliega desde GitHub Actions.

## Arquitectura

Ver [docs/arquitectura.md](docs/arquitectura.md) (diagrama y recorrido de un KID paso a paso).

| Capa | Tecnología |
|---|---|
| Captura | Python + requests + BeautifulSoup |
| Almacenamiento | Amazon S3 (privado) |
| Extracción | Amazon Bedrock (Converse API) con salidas estructuradas |
| Base de datos | Aurora PostgreSQL Serverless v2 + RDS Data API |
| API | FastAPI en AWS Lambda (Function URL) |
| Visualización | Streamlit en Amazon ECS Express Mode |
| Despliegue | Terraform + GitHub Actions (OIDC, estado en S3) |

## Decisiones tomadas

Resumen aquí; detalle y justificación en [docs/decisiones.md](docs/decisiones.md).

- _pendiente_

## Seguridad

El repositorio es público: no contiene credenciales ni datos. GitHub Actions accede a AWS mediante OIDC
(credenciales temporales) y un workflow con gitleaks revisa cada cambio. Detalle en [docs/seguridad.md](docs/seguridad.md).

## Cómo desplegar

_pendiente — se completará tras los talleres 1 y 2._

1. Requisitos previos (cuenta AWS, acceso al modelo de Bedrock, Terraform, Python).
2. Arranque manual: bucket del estado de Terraform y rol OIDC para GitHub.
3. Configurar en GitHub las variables del repositorio (sin secretos de AWS gracias a OIDC).
4. Push a `main` → GitHub Actions ejecuta Terraform y despliega.
5. Ejecutar el scraper y la extracción.
6. **Limpieza:** `terraform destroy` para no generar costes.

## Resultados

Ver [docs/resultados.md](docs/resultados.md).

## Estructura del repositorio

```
├── CLAUDE.md            Normas para trabajar en el repo (personas y asistentes de IA)
├── ESTADO.md            Estado, reparto, decisiones pendientes y bitácora
├── docs/                Enunciado, arquitectura, decisiones, glosario, resultados, seguridad, pasos manuales
├── scraper/             Captura de KIDs → S3 + manifiesto
├── extraccion/          Extracción con Bedrock (esquema del Anexo A)
├── base_datos/          Esquema SQL y carga
├── api/                 FastAPI en Lambda
├── app/                 Dashboard Streamlit
├── infra/               Terraform
└── .github/workflows/   GitHub Actions
```
