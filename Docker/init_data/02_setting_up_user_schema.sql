CREATE SCHEMA IF NOT EXISTS "user";

SET search_path TO "user";


-- Cria uma função para atualizar o campo last_update
CREATE OR REPLACE FUNCTION prevent_manually_creation()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.creation IS DISTINCT FROM OLD.creation THEN
        RAISE EXCEPTION 'Cannot modify the creation timestamp.';
    END IF;
    
    IF OLD.creation IS NULL THEN
    NEW.creation = CURRENT_TIMESTAMP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_manually_changes_on_timestamp_fields()
RETURNS TRIGGER AS $$
BEGIN
    -- Preventing manually set creation
    IF NEW.creation IS DISTINCT FROM OLD.creation THEN
        RAISE EXCEPTION 'Cannot modify the creation timestamp.';
    END IF;

    IF OLD.creation IS NULL THEN
    NEW.creation = CURRENT_TIMESTAMP;
    END IF;

    -- Preventing manually set last_update
    IF NEW.last_update IS DISTINCT FROM OLD.last_update THEN
        RAISE EXCEPTION 'Cannot modify the last_update timestamp.';
    END IF;

    NEW.last_update = CURRENT_TIMESTAMP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Tabela de usuários
CREATE TABLE IF NOT EXISTS "tb_user" (
    id_user UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    birthdate DATE NOT NULL,
    language VARCHAR(6) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    last_update TIMESTAMP,
    creation TIMESTAMP 
);

CREATE TRIGGER prevent_user_set_user_creation_field_on_insert
BEFORE INSERT ON "tb_user"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_user_set_user_creation_field_on_update
BEFORE UPDATE ON "tb_user"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();


-- Tabela de tipoes de eventos
CREATE TABLE IF NOT EXISTS "tb_user_event_type" (
    id_user_event_type SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela de eventos
CREATE TABLE IF NOT EXISTS "tb_user_event" (
    id_user_event SERIAL PRIMARY KEY,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE SET NULL,
    cd_user_event_type INTEGER NOT NULL REFERENCES "tb_user_event_type"(id_user_event_type) ON DELETE SET NULL,
    comment JSONB DEFAULT '{}'::JSONB,
    creation TIMESTAMP 
);

CREATE TRIGGER prevent_user_set_event_creation_field_on_insert
BEFORE INSERT ON "tb_user_event"
FOR EACH ROW
EXECUTE FUNCTION prevent_manually_creation();

CREATE TRIGGER prevent_user_set_event_creation_field_on_update
BEFORE UPDATE ON "tb_user_event"
FOR EACH ROW
EXECUTE FUNCTION prevent_manually_creation();


-- Tabela de unit_type
CREATE TABLE IF NOT EXISTS "tb_user_unit_type" (
    id_user_unit_type UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL,
    base_calc INTEGER NOT NULL,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE CASCADE,
    last_update TIMESTAMP,
    creation TIMESTAMP,
    CONSTRAINT unique_unit_type_name_per_user UNIQUE (name, cd_user),
    CONSTRAINT unique_unit_type_abbreviation_per_user UNIQUE (abbreviation, cd_user)
);

CREATE TRIGGER prevent_user_set_unit_type_creation_field_on_insert
BEFORE INSERT ON "tb_user_unit_type"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_user_set_unit_type_creation_field_on_update
BEFORE UPDATE ON "tb_user_unit_type"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();


-- Tabela de market
CREATE TABLE IF NOT EXISTS "tb_user_market" (
    id_user_market UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE CASCADE,
    preference BOOLEAN NOT NULL DEFAULT FALSE,
    last_update TIMESTAMP,
    creation TIMESTAMP,
    CONSTRAINT unique_market_per_user UNIQUE (name, cd_user)
);

CREATE TRIGGER prevent_user_set_market_creation_field_on_insert
BEFORE INSERT ON "tb_user_market"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_user_set_market_creation_field_on_update
BEFORE UPDATE ON "tb_user_market"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();


-- Tabela user category
CREATE TABLE IF NOT EXISTS "tb_user_category" (
    id_user_category UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE CASCADE,
    last_update TIMESTAMP,
    creation TIMESTAMP,
    CONSTRAINT unique_category_per_user UNIQUE (name, cd_user)
);

CREATE TRIGGER prevent_user_set_category_creation_field_on_insert
BEFORE INSERT ON "tb_user_category"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_user_set_category_creation_field_on_update
BEFORE UPDATE ON "tb_user_category"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();


-- Tabela user product
CREATE TABLE IF NOT EXISTS "tb_user_product" (
    id_user_product UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    cd_user_unit_type UUID NOT NULL REFERENCES "tb_user_unit_type"(id_user_unit_type) ON DELETE CASCADE,
    price MONEY NOT NULL,
    cd_price_unit_type UUID NOT NULL REFERENCES "tb_user_unit_type"(id_user_unit_type) ON DELETE CASCADE,
    cd_user_category UUID NOT NULL REFERENCES "tb_user_category"(id_user_category) ON DELETE CASCADE,
    notes TEXT,
    barcode VARCHAR(50),
    image_url TEXT,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE CASCADE,
    last_update TIMESTAMP,
    creation TIMESTAMP,
    CONSTRAINT unique_product_per_user UNIQUE (name, cd_user)
);

CREATE TRIGGER prevent_user_set_product_creation_field_on_insert
BEFORE INSERT ON "tb_user_product"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_user_set_product_creation_field_on_update
BEFORE UPDATE ON "tb_user_product"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();


-- Tabela de shopping list
CREATE TABLE IF NOT EXISTS "tb_user_shopping_list" (
    id_user_shopping_list UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE CASCADE,
    final_value MONEY NOT NULL,
    unique_itens INTEGER NOT NULL DEFAULT 0,
    total_itens INTEGER NOT NULL DEFAULT 0,
    last_update TIMESTAMP,
    creation TIMESTAMP,
    CONSTRAINT unique_shopping_list_per_user UNIQUE (name, cd_user)
);

CREATE TRIGGER prevent_user_set_shopping_list_creation_field_on_insert
BEFORE INSERT ON "tb_user_shopping_list"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_user_set_shopping_list_creation_field_on_update
BEFORE UPDATE ON "tb_user_shopping_list"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();


-- Tabela de product list
CREATE TABLE IF NOT EXISTS "tb_product_list" (
    id_product_list UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cd_user_shopping_list UUID NOT NULL REFERENCES "tb_user_shopping_list"(id_user_shopping_list) ON DELETE CASCADE,
    cd_user_product UUID NOT NULL REFERENCES "tb_user_product"(id_user_product) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1,
    price MONEY NOT NULL DEFAULT 0,
    total MONEY NOT NULL DEFAULT 0,
    on_cart BOOLEAN NOT NULL DEFAULT FALSE,
    last_update TIMESTAMP,
    creation TIMESTAMP,
    CONSTRAINT unique_product_list_per_shopping_list UNIQUE (cd_user_shopping_list, cd_user_product)
);

CREATE TRIGGER prevent_user_set_product_list_creation_field_on_insert
BEFORE INSERT ON "tb_product_list"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_user_set_product_list_creation_field_on_update
BEFORE UPDATE ON "tb_product_list"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();


-- tabela de shopping log
CREATE TABLE IF NOT EXISTS "tb_user_shopping_log" (
    id_user_shopping_log UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shopping_date DATE NOT NULL DEFAULT CURRENT_DATE,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE CASCADE,
    cd_user_shopping_list UUID NOT NULL REFERENCES "tb_user_shopping_list"(id_user_shopping_list) ON DELETE CASCADE,
    cd_user_market UUID NOT NULL REFERENCES "tb_user_market"(id_market) ON DELETE CASCADE,
    last_update TIMESTAMP,
    creation TIMESTAMP,
    CONSTRAINT unique_shopping_log_per_user_per_market UNIQUE (cd_user, cd_user_shopping_list, cd_user_market)
);

CREATE TRIGGER prevent_user_set_shopping_log_creation_field_on_insert
BEFORE INSERT ON "tb_user_shopping_log"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_user_set_shopping_log_creation_field_on_update
BEFORE UPDATE ON "tb_user_shopping_log"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();
