# scraper/ — Fase 1: Captura de los KID

**Qué hace:** recorre las webs de las gestoras, encuentra los enlaces a los PDF de los KID,
los descarga, los sube a S3 y apunta en un **manifiesto** de dónde viene cada uno y cuándo se bajó.

**Referencia del taller:** Python + `requests` + `BeautifulSoup`.

## Fuentes

| Gestora | Entrada | Pista para encontrar el KID | Dificultad | Responsable |
|---|---|---|---|---|
| Bestinver | https://www.bestinver.es/fondos-de-inversion/ | Ficha del fondo → enlace «Datos fundamentales» | Baja | _por asignar_ |
| Azvalor | https://www.azvalor.com/fondos/ | Ficha → «Folleto simplificado (DFP)». El nombre del PDF lleva fecha: leer la URL del HTML, no adivinarla | Media | _por asignar_ |
| Cobas AM | https://www.cobasam.com/productos/ | Ficha con un bloque por clase (A–D), cada una con ISIN y «PRIIP pdf» | Media-alta | _por asignar_ |

Mínimo exigido: **2 fuentes y 15 documentos**. Antes de programar, contad cuántos KID hay en cada web
(paso de «inspección»): así sabremos si con dos gestoras llegamos a 15.

## Scraping responsable (checklist)

- [ ] Leer el `robots.txt` de cada web (`https://<dominio>/robots.txt`) y respetarlo.
- [ ] Enviar un `User-Agent` que identifique el proyecto (genérico, sin datos personales).
- [ ] Esperar entre peticiones (`time.sleep(1)` o más). No lanzar peticiones en paralelo.
- [ ] No volver a descargar lo que ya tenemos (comparar URL / huella SHA-256).
- [ ] Gestionar errores: si una web cambia y no encontramos el enlace, avisar claramente en el log en vez de fallar en silencio.

## Formato del manifiesto (propuesta)

Un fichero **JSON Lines** (`manifiesto.jsonl`): una línea = un PDF. Se guarda en S3 junto a los PDF
(y opcionalmente en local en `datos/`, que está en `.gitignore`).

```json
{"fuente": "bestinver", "url_ficha": "https://...", "url_pdf": "https://...pdf", "s3_key": "kid/bestinver/2026-11-22/<sha256>.pdf", "sha256": "ab12...", "fecha_descarga": "2026-11-22T10:15:00+01:00", "isin_web": null}
```

- `isin_web`: si la web muestra el ISIN junto al enlace (caso Cobas), lo guardamos. Luego sirve para
  **comprobar** lo que extrae el modelo (si no coinciden, algo va mal).

## Organización en S3 (propuesta)

```
s3://<bucket>/kid/<fuente>/<fecha_descarga>/<sha256>.pdf
s3://<bucket>/manifiestos/<fecha_descarga>.jsonl
```

Bucket **privado** (bloqueo de acceso público activado). Los datos solo salen por la API y la app.
