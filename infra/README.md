# infra/ — Fase 7: Infraestructura como código (Terraform)

**Qué hace:** describe en ficheros `.tf` todos los recursos de AWS (bucket S3, base de datos, Lambda,
contenedor de la app, permisos IAM…). En vez de crearlos a mano en la consola, Terraform los crea,
modifica o borra para que coincidan con lo escrito. Ventaja: es reproducible y queda en Git.

**Referencia del taller:** Terraform + **GitHub Actions** con **OIDC** y el **estado de Terraform en S3**.

## Conceptos clave (nivel básico)

- **Estado (`terraform.tfstate`)**: fichero donde Terraform apunta qué ha creado. Se guarda en un bucket S3
  (no en el repo, porque puede contener datos sensibles y porque lo compartimos entre todos).
- **`terraform plan`**: enseña qué va a cambiar **sin tocar nada**. Siempre antes de `apply`.
- **`terraform apply`**: aplica los cambios en AWS (crea recursos → **puede costar dinero**).
- **`terraform destroy`**: borra todo. Hacerlo **después de la exposición** para no pagar de más.
- **OIDC**: permite que GitHub Actions entre en AWS **sin guardar claves** en GitHub. AWS confía en GitHub
  y le da permisos temporales a un rol IAM. Así cumplimos la regla «sin credenciales en el repositorio».

## Orden de despliegue (según los talleres)

1. **Arranque manual (una vez):** bucket para el estado de Terraform + rol IAM de OIDC para GitHub.
2. **Taller 1:** bucket S3 de los PDF (privado) + base de datos Aurora PostgreSQL Serverless v2 (Data API activada).
3. **Taller 2:** Lambda de la API (con Function URL), servicio ECS de la app, permisos de Bedrock.

## Workflows de GitHub Actions (en `.github/workflows/`)

| Workflow | Cuándo | Qué hace | Estado |
|---|---|---|---|
| `terraform.yml` | Pull request → `plan`; push a `main` → `apply` | Despliega la infraestructura | ⬜ Pendiente |
| `deploy-api.yml` / `deploy-app.yml` | Push a `main` que toque `api/` o `app/` | Empaqueta y publica | ⬜ Pendiente (o dentro del anterior) |

## Ficheros

| Fichero | Estado |
|---|---|
| `main.tf`, `variables.tf`, `outputs.tf`, `backend.tf` | ⬜ Pendiente (taller 1) |

> ⚠️ Nunca subir `*.tfstate`, `*.tfvars` con secretos, ni la carpeta `.terraform/` (ya están en `.gitignore`).
