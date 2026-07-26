INSERT INTO palestras (codigo_palestra, titulo, pontos) VALUES
    ('CAP-101', 'Abertura: Inovação no Serviço Público', 10),
    ('CAP-102', 'Transformação Digital', 15),
    ('CAP-103', 'Comunicação e Colaboração', 10),
    ('CAP-104', 'Gestão de Projetos', 20)
ON CONFLICT (codigo_palestra) DO UPDATE
SET titulo = EXCLUDED.titulo, pontos = EXCLUDED.pontos;

