# Seguridad: el repositorio es PÚBLICO

El profesor tiene que poder verlo, así que el repo es **público**: cualquiera en Internet puede leer
**todo** lo que subamos, **incluido el historial**. Hay robots que rastrean GitHub buscando claves de AWS
y las usan en minutos (por ejemplo, para minar criptomonedas a nuestra costa).

> **Idea clave:** borrar una clave en un commit nuevo **no la elimina**: sigue en el historial.
> Si una clave llega a subirse, se da por comprometida → **desactivarla en AWS de inmediato** y crear otra.

## Qué NUNCA se sube

| Qué | Por qué | Dónde va en su lugar |
|---|---|---|
| Claves de AWS (`AKIA...`, secret keys) | Dan acceso a la cuenta (y a la tarjeta) | No se usan: local con `aws configure sso`/perfil; GitHub con **OIDC** |
| `.env` | Configuración personal | Cada uno en su ordenador (`.env.example` sí se sube, vacío) |
| `*.tfstate` | Terraform guarda ahí datos sensibles (p. ej. contraseñas de la BD) | Bucket S3 de estado (privado) |
| `*.tfvars` con valores reales | Pueden contener secretos | Variables de GitHub / `.tfvars` local ignorado |
| Contraseñas de la base de datos | Obvio | **AWS Secrets Manager** (Aurora la genera y guarda sola) |
| PDF de los KID y datos extraídos (`.jsonl`, `.csv`…) | Regla del enunciado: los datos solo se exponen por la API y la app | S3 y PostgreSQL |
| Tu email personal en los commits | Es público y se rastrea para spam | Email *noreply* de GitHub ([pasos manuales §A](pasos-manuales.md#a-preparar-el-ordenador-de-cada-integrante-cada-uno-una-vez)) |

Todo esto ya está en [`.gitignore`](../.gitignore), pero `.gitignore` no protege de un `git add -f` ni de
pegar una clave dentro de un `.py`.

## Las 4 capas de protección que tenemos

1. **No hay claves que filtrar (OIDC).** GitHub Actions pide a AWS permisos temporales (duran minutos) para un rol
   concreto. No existe una clave permanente guardada en ningún sitio.
2. **`.gitignore`**: evita subir por despiste los ficheros peligrosos de la tabla.
3. **Push protection de GitHub**: en repos públicos, GitHub rechaza un `push` que contenga una clave reconocible.
4. **Workflow [`secretos.yml`](../.github/workflows/secretos.yml)** con *gitleaks*: en cada push y pull request revisa
   el código y el historial buscando secretos. Si encuentra algo, el check sale en rojo.

## Cuidados extra por ser público

- **Rol de OIDC restringido** a nuestro repo y a la rama `main` (condición `sub` en la política de confianza).
  Si no, en teoría otro repo podría pedir ese mismo rol.
- **Permisos mínimos** en el rol y en las Lambdas: solo lo que necesitan (p. ej. la API solo lee de la BD).
- En los workflows **no usar `pull_request_target`**, y el `apply` solo en `push` a `main`: así un pull request
  de un desconocido (alguien que hace *fork* del repo) no puede desplegar en nuestra cuenta.
- Los identificadores de la cuenta (ID de cuenta, ARNs) no son contraseñas, pero mejor **en variables de GitHub o
  `.env`** que escritos en el código.
- La API es pública: que sea **solo de lectura** y no devuelva enlaces directos a S3.

## Antes de cada commit (30 segundos)

```bash
git status            # ¿hay algún fichero que no esperaba?
git diff --staged     # ¿qué voy a subir exactamente?
```

Si ves algo como `AKIA`, `aws_secret_access_key`, `password=` o un `.env`: **para** y no hagas commit.

## Si se sube una clave por error

1. **Desactivarla en AWS ya** (IAM → usuario → Credenciales → Desactivar/Eliminar). Esto es lo urgente.
2. Avisar al grupo.
3. Revisar en AWS (CloudTrail / facturación) si alguien la ha usado.
4. Limpiar el historial es secundario: la clave ya está quemada.
