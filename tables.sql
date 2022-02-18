-- DROP TABLE IF EXISTS [SCHEMA].[TABLENAME];
CREATE TABLE IF NOT EXISTS [SCHEMA].[TABLENAME] (
    field1                      varchar(512)
    created_at                  timestamp DEFAULT now()
);

DROP TABLE IF EXISTS [SCHEMA].[TABLENAME]_staging;
CREATE TABLE IF NOT EXISTS [SCHEMA].[TABLENAME]_staging (
    field1                      varchar(512)
    created_at                  timestamp DEFAULT now()
);
