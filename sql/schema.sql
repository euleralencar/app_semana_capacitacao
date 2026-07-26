CREATE TABLE participantes (
    matricula VARCHAR(30) PRIMARY KEY,
    cpf CHAR(11) NOT NULL UNIQUE,
    nome VARCHAR(150) NOT NULL,
    secretaria VARCHAR(120) NOT NULL,
    data_cadastro TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE palestras (
    codigo_palestra VARCHAR(30) PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    pontos INTEGER NOT NULL CHECK (pontos >= 0)
);

CREATE TABLE registros_presenca (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    matricula VARCHAR(30) NOT NULL REFERENCES participantes (matricula),
    codigo_palestra VARCHAR(30) NOT NULL REFERENCES palestras (codigo_palestra),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (matricula, codigo_palestra)
);

CREATE INDEX registros_presenca_matricula_idx ON registros_presenca (matricula);

