-- =============================================================================
-- schema.sql — BORRADOR del modelo de datos (PostgreSQL)
-- =============================================================================
-- Estado: PROPUESTA. Revisar en grupo y ajustar a lo que haga el profesor en el
-- taller 2 antes de darlo por bueno (anotar la decisión en docs/decisiones.md).
--
-- Idea general: dos tablas.
--
--   documentos  -> un registro por PDF descargado ("de dónde viene y cuándo").
--                  Es el reflejo en base de datos del manifiesto del scraper.
--   kid         -> un registro por KID extraído con Bedrock (los campos del Anexo A).
--                  Cada fila de `kid` apunta al documento del que salió.
--
-- ¿Por qué separarlas? Porque son cosas distintas: el PDF (el fichero, su origen)
-- y los datos que contiene. Así, si repetimos la extracción con otro modelo,
-- no hace falta volver a descargar nada.
--
-- ¿Cómo evitamos DUPLICADOS (requisito del enunciado)?
--   * Cada PDF se identifica por su huella SHA-256 (un "DNI" del contenido del fichero:
--     si el fichero es idéntico, la huella es idéntica). Columna `sha256` UNIQUE.
--   * Cada documento solo puede tener una extracción: `kid.documento_id` UNIQUE.
--   * Al insertar usamos `INSERT ... ON CONFLICT ... DO UPDATE` (un "upsert"):
--     si ya existe, se actualiza en vez de crear otra fila. Ver ejemplo al final.
-- =============================================================================

CREATE TABLE IF NOT EXISTS documentos (
    id              BIGSERIAL PRIMARY KEY,           -- número autoincremental
    fuente          TEXT        NOT NULL,            -- 'bestinver', 'azvalor', 'cobas'...
    url_ficha       TEXT,                            -- página web del fondo donde estaba el enlace
    url_pdf         TEXT        NOT NULL,            -- URL exacta del PDF descargado
    s3_key          TEXT        NOT NULL,            -- ruta del PDF dentro del bucket S3
    sha256          CHAR(64)    NOT NULL UNIQUE,     -- huella del fichero -> evita duplicados
    fecha_descarga  TIMESTAMPTZ NOT NULL,            -- cuándo lo descargamos (con zona horaria)
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kid (
    id                           BIGSERIAL PRIMARY KEY,
    documento_id                 BIGINT NOT NULL UNIQUE      -- 1 extracción por documento
                                 REFERENCES documentos(id) ON DELETE CASCADE,

    -- Campos del Anexo A (mismos nombres que extraccion/esquema_kid.py)
    isin                         CHAR(12),
    nombre_producto              TEXT,
    nombre_clase                 TEXT,
    gestora                      TEXT,
    fecha_documento              DATE,
    sri                          SMALLINT CHECK (sri BETWEEN 1 AND 7),
    periodo_mantenimiento_anios  NUMERIC(4,1),
    gastos_corrientes_pct        NUMERIC(6,3),
    costes_entrada_pct           NUMERIC(6,3),
    costes_salida_pct            NUMERIC(6,3),

    -- Trazabilidad de la extracción (útil para comparar modelos, ampliación)
    modelo_bedrock               TEXT,                    -- id del modelo usado
    extraido_en                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Índice para buscar rápido por ISIN (la API lo usará mucho).
CREATE INDEX IF NOT EXISTS idx_kid_isin ON kid (isin);

-- -----------------------------------------------------------------------------
-- Ejemplo de "upsert" (insertar o actualizar) para un documento:
-- -----------------------------------------------------------------------------
-- INSERT INTO documentos (fuente, url_ficha, url_pdf, s3_key, sha256, fecha_descarga)
-- VALUES (:fuente, :url_ficha, :url_pdf, :s3_key, :sha256, :fecha_descarga)
-- ON CONFLICT (sha256) DO UPDATE SET fecha_descarga = EXCLUDED.fecha_descarga
-- RETURNING id;
--
-- Los ":nombre" son parámetros. Con la RDS Data API se pasan aparte (nunca
-- concatenando texto en la consulta, para evitar inyección SQL).
