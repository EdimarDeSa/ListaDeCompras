-- Cria uma função para atualizar o campo last_update
CREATE OR REPLACE FUNCTION update_last_update_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_update = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS "user" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    language VARCHAR(25) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(80) NOT NULL,
    birthdate DATE NOT NULL,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TRIGGER update_user_last_update
BEFORE UPDATE ON "user"
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();
CREATE TABLE IF NOT EXISTS default_category (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TRIGGER update_default_category_last_update
BEFORE UPDATE ON default_category
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();


-- Tabela de unity_type
CREATE TABLE IF NOT EXISTS unity_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    abbreviation VARCHAR(10) NOT NULL UNIQUE,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    base_calc INTEGER NOT NULL
);

CREATE TRIGGER update_unity_type_last_update
BEFORE UPDATE ON unity_type
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();

-- Tabela de default_products
CREATE TABLE IF NOT EXISTS default_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    unit_type_id UUID REFERENCES unity_type(id) NOT NULL,
    default_category_id UUID REFERENCES default_category(id) NOT NULL,
    image_url TEXT
);

CREATE TRIGGER update_default_products_last_update
BEFORE UPDATE ON default_products
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();


-- Tabela de market
CREATE TABLE IF NOT EXISTS market (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
);