CREATE TABLE participantes (
    matricula VARCHAR(30) PRIMARY KEY,
    cpf CHAR(11) NOT NULL UNIQUE,
    nome VARCHAR(150) NOT NULL,
    secretaria VARCHAR(120) NOT NULL,
    data_cadastro TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE palestras (
    codigo_palestra VARCHAR(30) PRIMARY KEY,
    data_palestra DATE NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    palestrante VARCHAR(500),
    cargo VARCHAR(255),
    instituicao VARCHAR(150),
    disciplina VARCHAR(150),
    trilha VARCHAR(100),
    pontos INTEGER NOT NULL CHECK (pontos >= 0) DEFAULT 25,
    data_criacao TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE registros_presenca (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    matricula VARCHAR(30) NOT NULL REFERENCES participantes (matricula),
    codigo_palestra VARCHAR(30) NOT NULL REFERENCES palestras (codigo_palestra),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (matricula, codigo_palestra)
);

-- Índices para melhor performance em queries
CREATE INDEX palestras_data_idx ON palestras (data_palestra);
CREATE INDEX palestras_trilha_idx ON palestras (trilha);
CREATE INDEX registros_presenca_matricula_idx ON registros_presenca (matricula);
CREATE INDEX registros_presenca_codigo_palestra_idx ON registros_presenca (codigo_palestra);
CREATE INDEX registros_presenca_matricula_palestra_idx ON registros_presenca (matricula, codigo_palestra);
