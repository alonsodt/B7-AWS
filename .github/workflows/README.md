# .github/workflows/

Aquí van los ficheros `.yml` de GitHub Actions (se crean en los talleres 1 y 2).
Plan y estado en [infra/README.md](../../infra/README.md#workflows-de-github-actions-en-githubworkflows).

Recordatorio: el acceso a AWS se hace por **OIDC** (`aws-actions/configure-aws-credentials` con `role-to-assume`).
**Nunca** guardar `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` en los secretos del repositorio.
