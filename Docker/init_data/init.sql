
-- Cria uma função para atualizar o campo last_update
CREATE OR REPLACE FUNCTION update_last_update_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_update = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS "tb_user" (
    id_user UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    language VARCHAR(6) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    password VARCHAR(80) NOT NULL,
    birthdate DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE TRIGGER update_user_last_update
BEFORE UPDATE ON "tb_user"
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();

-- Tabela de default_category
CREATE TABLE IF NOT EXISTS "tb_default_category" (
    id_default_category SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE TRIGGER update_default_category_last_update
BEFORE UPDATE ON "tb_default_category"
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();

-- Tabela de unit_type
CREATE TABLE IF NOT EXISTS "tb_unit_type" (
    id_unit_type SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    abbreviation VARCHAR(10) NOT NULL UNIQUE,
    base_calc INTEGER NOT NULL,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE TRIGGER update_unit_type_last_update
BEFORE UPDATE ON "tb_unit_type"
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();

-- Tabela de default_products
CREATE TABLE IF NOT EXISTS "tb_default_product" (
    id_default_products SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    cd_unit_type INTEGER REFERENCES "tb_unit_type"(id_unit_type) NOT NULL,
    cd_default_category INTEGER REFERENCES "tb_default_category"(id_default_category) NOT NULL,
    image_url TEXT,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE TRIGGER update_default_products_last_update
BEFORE UPDATE ON "tb_default_product"
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();

-- Tabela de market
CREATE TABLE IF NOT EXISTS "tb_market" (
    id_market UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE CASCADE,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT unique_market_per_user UNIQUE (name, cd_user)
);
CREATE TRIGGER update_market_last_update
BEFORE UPDATE ON "tb_market"
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();

-- Tabela user category
CREATE TABLE IF NOT EXISTS "tb_user_category" (
    id_user_category UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE CASCADE,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT unique_category_per_user UNIQUE (name, cd_user)
);
CREATE TRIGGER update_user_category_last_update
BEFORE UPDATE ON "tb_user_category"
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();

-- Tabela user product
CREATE TABLE IF NOT EXISTS "tb_user_product" (
    id_user_product UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    cd_unit_type INTEGER NOT NULL REFERENCES "tb_unit_type"(id_unit_type) ON DELETE CASCADE,
    price MONEY NOT NULL,
    cd_price_unit_type INTEGER NOT NULL REFERENCES "tb_unit_type"(id_unit_type) ON DELETE CASCADE,
    cd_user_category UUID NOT NULL REFERENCES "tb_user_category"(id_user_category) ON DELETE CASCADE,
    notes TEXT,
    barcode VARCHAR(50),
    image_url TEXT,
    cd_user UUID NOT NULL REFERENCES "tb_user"(id_user) ON DELETE CASCADE,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE TRIGGER update_user_product_last_update
BEFORE UPDATE ON "tb_user_product"
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();

-- Popula a tabela de default_category
INSERT INTO "tb_default_category" ("id_default_category", "name") VALUES
(1, 'Laticínios'),
(2, 'Frios'),
(3, 'Carnes'),
(4, 'Condimentos'),
(5, 'Hortifrúti'),
(6, 'Bazar'),
(7, 'Bebidas'),
(8, 'Limpeza'),
(9, 'Higiene Pessoal'),
(10, 'Padaria'),
(11, 'Enlatados'),
(12, 'Cereais'),
(13, 'Outros');

-- Popula a tabela de unit_type
INSERT INTO "tb_unit_type" ("id_unit_type", "name", "abbreviation", "base_calc") VALUES
(1, 'Gramas', 'g', 1),
(2, 'Kilos', 'Kg', 1000),
(3, 'Pacote', 'Pac', 1),
(4, 'Unidade', 'Un', 1),
(5, 'Litros', 'L', 1000),
(6, 'Mililitros', 'ml', 1),
(7, 'Caixa', 'Cx', 1),
(8, 'Galão', 'Gal', 1),
(9, 'Bandeja', 'Bdj', 1);

-- Popula a tabela de default_products
INSERT INTO "tb_default_product" ("name", "cd_unit_type", "cd_default_category") VALUES 
('Pão', 1, 10),
('Arroz', 2, 12),
('Feijão', 2, 12),
('Creme dental', 4, 9),
('Escova de dentes', 4, 9),
('Enxaguante bucal', 4, 9),
('Desodorante', 4, 9),
('Cotonete', 4, 9),
('Creme de pentear', 4, 9),
('Esponja de banho', 4, 9),
('Sabonete', 4, 9),
('Shampoo', 4, 9),
('Condicionador', 4, 9),
('Papel higiênico', 3, 9),
('Mostarda', 4, 4),
('Ketchup', 4, 4),
('Molho de pimenta', 4, 4),
('Sal', 1, 4),
('Óleo', 5, 4),
('Salsicha', 3, 3),
('Linguiça', 2, 3),
('Peixe', 2, 3),
('Atum', 2, 3),
('Sardinha', 2, 3),
('Carne', 2, 3),
('Frango', 2, 3),
('Margarina', 4, 1),
('Manteiga', 4, 1),
('Iogurte', 4, 1),
('Geléia', 4, 1),
('Leite', 5, 1),
('Queijo', 1, 1),
('Presunto', 1, 1),
('Leite condensado', 4, 1),
('Creme de leite', 4, 1),
('Gelatina', 4, 1),
('Ricota', 4, 1),
('Requeijão', 4, 1),
('Cereal', 4, 6),
('Granola', 2, 6),
('Aveia', 2, 6),
('Biscoitos', 4, 6),
('Bolacha', 4, 6),
('Chocolate', 4, 6),
('Balas', 4, 6),
('Chiclete', 4, 6),
('Pipoca', 4, 6),
('Amendoim', 4, 6),
('Castanhas', 4, 6),
('Nozes', 4, 6),
('Pistache', 4, 6),
('Ovos', 7, 6),
('Farinha de trigo', 2, 6),
('Macarrão', 3, 6),
('Geleia real', 4, 6),
('Mel', 4, 6),
('Creme de avelã', 4, 6),
('Pasta de amendoim', 4, 6),
('Marshmallows', 4, 6),
('Açúcar mascavo', 4, 6),
('Adoçante', 4, 6),
('Melado', 4, 6),
('Chantilly', 4, 6),
('Açucar', 4, 6),
('Cerveja', 4, 7),
('Vinho', 4, 7),
('Espumante', 4, 7),
('Vodka', 4, 7),
('Whisky', 4, 7),
('Tequila', 4, 7),
('Rum', 4, 7),
('Martini', 4, 7),
('Campari', 4, 7),
('Licor', 4, 7),
('Suco', 5, 7),
('Refrigerante', 5, 7),
('Suco de pozinho', 4, 7),
('Água', 4, 7),
('Água com gáz', 4, 7),
('Chá', 4, 7),
('Achocolatado', 4, 7),
('Café', 4, 7),
('Vinagre', 5, 7),
('Azeitonas', 4, 11),
('Molho de tomate', 4, 11),
('Picles', 4, 11),
('Frutas em calda', 4, 11),
('Patê', 4, 11),
('Manga', 2, 5),
('Banana', 2, 5),
('Maçã', 2, 5),
('Laranja', 2, 5),
('Cebola', 2, 5),
('Alho', 1, 5),
('Batata', 2, 5),
('Uva', 2, 5),
('Tomate', 2, 5),
('Pano de limpeza', 4, 8),
('Sabão em pó', 2, 8),
('Esponja de cozinha', 4, 8),
('Detergente', 4, 8),
('Amaciante', 4, 8),
('Desinfectante', 4, 8),
('Alvejante', 4, 8),
('Limpador multiúso', 4, 8);
