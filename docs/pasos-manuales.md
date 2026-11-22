# Pasos manuales

Casi todo el pipeline se automatiza con código, Terraform y GitHub Actions, pero **hay cosas que tiene que
hacer una persona a mano**: unas porque son «el huevo y la gallina» (hay que crearlas antes de que la
automatización pueda funcionar), otras porque requieren decidir, revisar o entregar.

> Un asistente de IA **no** debe hacer estos pasos por nosotros cuando implican credenciales, pagos o
> aceptar condiciones. Los hace cada uno en su consola / navegador.

Marca cada paso al hacerlo y apunta quién lo hizo en la bitácora de [ESTADO.md](../ESTADO.md).

---

## A. Preparar el ordenador de cada integrante (cada uno, una vez)

- [ ] Instalar **Git**, **Python 3.11+**, **Terraform**, **AWS CLI v2**.
- [ ] Instalar **Docker Desktop** (solo quien construya la imagen de la app en local; en GitHub Actions no hace falta).
- [ ] Configurar Git para que **tu email personal no salga en los commits** (el repo es público):
      usa el email *noreply* de GitHub (Settings → Emails → «Keep my email addresses private»):
      ```bash
      git config --global user.email "<ID>+<usuario>@users.noreply.github.com"
      ```
- [ ] Configurar el acceso a AWS en local **sin guardar claves en el repo**: `aws configure sso`
      (si la cuenta usa IAM Identity Center) o `aws configure --profile b7` (se guarda en `~/.aws/`, fuera del repo).
- [ ] Copiar `.env.example` a `.env` y rellenarlo (el `.env` nunca se sube).

## B. AWS (lo hace una persona, en la cuenta que usemos)

- [ ] **Decidir la cuenta**: una compartida por el grupo o la de un integrante (ver ESTADO → decisiones pendientes).
- [ ] **Alerta de presupuesto** en *AWS Budgets* (p. ej. 10 €/mes con aviso por email). Lo primero de todo.
- [ ] Elegir **región** y comprobar en la consola de **Bedrock** que el modelo elegido está disponible y habilitado
      (para modelos de algunos proveedores, como Anthropic, la primera vez puede pedir rellenar un formulario de uso).
- [ ] **Arranque («bootstrap») de Terraform** — esto no lo puede hacer GitHub Actions porque es justo lo que le da acceso:
  - [ ] Bucket S3 para el **estado de Terraform** (privado, con versionado).
  - [ ] **Proveedor OIDC** de GitHub en IAM (`token.actions.githubusercontent.com`).
  - [ ] **Rol IAM** que asumirá GitHub Actions, con una política de confianza **restringida a nuestro repo y a la rama `main`**
        (condición `sub` = `repo:<usuario>/<repo>:ref:refs/heads/main`). Con el repo público esto es crítico:
        sin esa condición, workflows de otros repos podrían intentar asumir el rol.
  - Se puede hacer con clics en la consola o con un Terraform pequeño aplicado **una vez en local** (lo verá el profesor en el taller 1).

## C. GitHub (lo hace quien cree el repo)

- [ ] Crear el repositorio **público** y subir el código.
- [ ] Invitar como colaboradores a **Pietro** y **Raúl** (Settings → Collaborators).
- [ ] Comprobar que están activos **Secret scanning** y **Push protection** (Settings → Code security).
      En repos públicos vienen activados por defecto: bloquean un `push` que contenga una clave reconocible.
- [ ] Proteger la rama `main` (Settings → Branches): exigir pull request y que pase el workflow `secretos`.
- [ ] Guardar como **Variables** del repo (Settings → Secrets and variables → Actions → *Variables*) el ARN del rol,
      la región y el nombre del bucket de estado. No son contraseñas, pero así no quedan escritos en el código.
      **No** crear secretos `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`: con OIDC no hacen falta.

## D. Durante el desarrollo

- [ ] **Inspeccionar cada web a mano** con las herramientas de desarrollador del navegador (F12): dónde está el enlace
      al PDF, si el HTML lo trae o se carga con JavaScript, cuántos KID hay. Revisar `robots.txt`.
- [ ] Ejecutar el scraper y la extracción **la primera vez con 1–2 PDF** y revisar el resultado antes de lanzar el lote completo.
- [ ] **Revisar a mano 5–10 KID** (abrir el PDF y apuntar los valores reales) para medir la precisión del modelo.
      Es la «verdad de referencia» y no se puede automatizar. Guardar la tabla en `docs/resultados.md`
      (solo los valores de los campos, no los PDF).
- [ ] Escribir las **interpretaciones** de los resultados (lo hacemos nosotros; la IA puede ayudar, pero tenemos que entenderlas).

## E. Entrega y exposición

- [ ] Preguntar al profesor las dudas del enunciado (ver ESTADO → riesgos).
- [ ] Completar el README: integrantes, URLs, arquitectura, decisiones, cómo desplegar.
- [ ] **Entregar en el aula virtual** antes del **2/12/2026**: enlace al repo, URL de la app, URL de la API, nombres.
- [ ] Preparar y **ensayar** la exposición (5 min + demo en directo). Tener un plan B (capturas o vídeo) por si falla la red.
- [ ] Después de la exposición: **`terraform destroy`** y borrar a mano lo creado en el bootstrap, para no pagar de más.
