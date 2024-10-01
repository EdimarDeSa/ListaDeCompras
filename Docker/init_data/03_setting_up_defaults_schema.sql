CREATE SCHEMA IF NOT EXISTS "defaults";

SET search_path TO "defaults";

-- Tabela de default_category
CREATE TABLE IF NOT EXISTS "tb_default_category" (
    id_default_category SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);


-- Tabela de unit_type
CREATE TABLE IF NOT EXISTS "tb_default_unit_type" (
    id_unit_type SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    abbreviation VARCHAR(10) NOT NULL UNIQUE,
    base_calc INTEGER NOT NULL DEFAULT 1
);


-- Tabela de default_products
CREATE TABLE IF NOT EXISTS "tb_default_product" (
    id_default_products SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    cd_unit_type INTEGER REFERENCES "tb_default_unit_type"(id_unit_type) NOT NULL,
    cd_default_category INTEGER REFERENCES "tb_default_category"(id_default_category) NOT NULL,
    image_url TEXT
);
