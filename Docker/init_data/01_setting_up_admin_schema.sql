CREATE SCHEMA IF NOT EXISTS "admin";

SET search_path TO "admin";

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


CREATE TABLE IF NOT EXISTS "tb_admin" (
    id_admin UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    birthdate DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    last_update TIMESTAMP,
    creation TIMESTAMP
);

CREATE TRIGGER prevent_admin_set_admin_creation_field_on_insert
BEFORE INSERT ON "tb_admin"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_admin_set_admin_creation_field_on_update
BEFORE UPDATE ON "tb_admin"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();


CREATE TABLE IF NOT EXISTS "tb_admin_event_type" (
    id_admin_event_type SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS "tb_admin_event" (
    id_admin_event SERIAL PRIMARY KEY,
    cd_admin UUID NOT NULL REFERENCES "tb_admin"(id_admin) ON DELETE CASCADE,
    cd_admin_event_type INTEGER NOT NULL REFERENCES "tb_admin_event_type"(id_admin_event_type) ON DELETE CASCADE,
    comment JSONB DEFAULT '{}'::JSONB,
    creation TIMESTAMP
);

CREATE TRIGGER prevent_admin_set_event_creation_field_on_insert
BEFORE INSERT ON "tb_admin_event"
FOR EACH ROW
EXECUTE FUNCTION prevent_manually_creation();

CREATE TRIGGER prevent_admin_set_event_creation_field_on_update
BEFORE UPDATE ON "tb_admin_event"
FOR EACH ROW
EXECUTE FUNCTION prevent_manually_creation();


INSERT INTO "tb_admin" ("name", "email", "birthdate", "is_active") VALUES
('System', 'system@localhost.com', CURRENT_DATE, true),
('Admin', 'admin@localhost.com', CURRENT_DATE, true);

INSERT INTO "tb_admin_event_type" ("id_admin_event_type", "name") VALUES
(1, 'create'),
(2, 'update'),
(3, 'delete');

INSERT INTO "tb_admin_event" ("cd_admin", "cd_admin_event_type", "comment") VALUES
((SELECT id_admin FROM "tb_admin" WHERE name = 'System'), 1, '{"msg": "System user created"}'),
((SELECT id_admin FROM "tb_admin" WHERE name = 'System'), 1, '{"msg": "Admin user created"}');