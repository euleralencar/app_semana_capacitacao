-- Script para popular palestras do evento
-- Data: 17, 18, 19 e 20 de agosto (segunda a quinta-feira)
-- Horário do evento: 9h30 às 17h50
-- Trilhas: Estágio, Jurídico, Integridade e Futuro

-- Segunda-feira (17 de agosto)
INSERT INTO palestras (codigo_palestra, data_palestra, horario_inicio, horario_fim, titulo, trilha, pontos) VALUES
('SEG-148', '2026-08-17', '09:30', '10:00', 'Palestra 148', NULL, 10),
('SEG-118', '2026-08-17', '10:05', '10:35', 'Palestra 118', NULL, 10),
('SEG-177', '2026-08-17', '10:40', '11:10', 'Palestra 177', NULL, 10),
('SEG-144', '2026-08-17', '11:15', '11:45', 'Palestra 144', NULL, 10),
('SEG-171', '2026-08-17', '11:50', '12:20', 'Palestra 171', NULL, 10),
('SEG-118A', '2026-08-17', '14:30', '15:00', 'Carreira em Construção: do estágio às oportunidades', 'Estágio', 15),
('SEG-193', '2026-08-17', '15:05', '15:35', 'Saúde Mental e Estágio: conciliação entre estágio e estudos', 'Estágio', 15),
('SEG-128', '2026-08-17', '15:40', '16:10', 'Inclusão no estágio: acolhimento e acessibilidade', 'Estágio', 15),
('SEG-137', '2026-08-17', '16:40', '17:10', 'Histórias que inspiram', 'Estágio', 15),
('SEG-132', '2026-08-17', '17:15', '17:45', 'Carreira e Imagem', 'Estágio', 15);

-- Terça-feira (18 de agosto)
INSERT INTO palestras (codigo_palestra, data_palestra, horario_inicio, horario_fim, titulo, trilha, pontos) VALUES
('TER-218', '2026-08-18', '09:30', '10:00', 'Palestra 218', NULL, 10),
('TER-212', '2026-08-18', '10:05', '10:35', 'Palestra 212', NULL, 10),
('TER-220', '2026-08-18', '10:40', '11:10', 'Além do mito centralista: O papel descentralizador do STF nos Conflitos Federativos em Ações Cíveis Originárias', 'Jurídico', 20),
('TER-262', '2026-08-18', '11:15', '11:45', 'Decisões Estruturantes de Natureza Penal: Um Estudo de Caso Sobre a Determinação do Uso de Câmeras Corporais em Operações Policiais', 'Jurídico', 20),
('TER-268', '2026-08-18', '11:50', '12:20', 'ADPF 635: Estudo de Caso sobre Obstáculos e Avanços no Combate à Violência Policial e o Racismo', 'Jurídico', 20),
('TER-297', '2026-08-18', '14:00', '14:30', 'Carreira em Construção: do estágio às oportunidades', 'Estágio', 15),
('TER-219', '2026-08-18', '14:35', '15:05', 'Saúde Mental e Estágio: conciliação entre estágio e estudos', 'Estágio', 15),
('TER-272', '2026-08-18', '15:10', '15:40', 'Inclusão no estágio: acolhimento e acessibilidade', 'Estágio', 15),
('TER-269', '2026-08-18', '16:10', '16:40', 'Histórias que inspiram', 'Estágio', 15),
('TER-234', '2026-08-18', '16:45', '17:15', 'Carreira e Imagem', 'Estágio', 15);

-- Quarta-feira (19 de agosto)
INSERT INTO palestras (codigo_palestra, data_palestra, horario_inicio, horario_fim, titulo, trilha, pontos) VALUES
('QUA-326', '2026-08-19', '09:30', '10:00', 'Palestra 326', NULL, 10),
('QUA-399', '2026-08-19', '10:05', '10:35', 'Palestra 399', NULL, 10),
('QUA-373', '2026-08-19', '10:40', '11:10', 'Os Impactos do Habeas Corpus Coletivo N.º 143.641/SP no Desencarceramento das Mulheres e na Construção de Políticas Públicas por Meio do Julgamento de Litígios Estruturais', 'Jurídico', 20),
('QUA-311', '2026-08-19', '11:15', '11:45', 'O Poder Judiciário e a Intervenção em Políticas Públicas: Análise dos Juízos de Retratação no Tema 698', 'Jurídico', 20),
('QUA-389', '2026-08-19', '11:50', '12:20', 'Deferência Judicial: Um Estudo Empírico no Âmbito do Supremo Tribunal Federal sobre o Controle das Agências Reguladoras', 'Jurídico', 20),
('QUA-328', '2026-08-19', '14:00', '14:30', 'Governança e Integridade: como cada papel protege o STF', 'Integridade e Futuro', 15),
('QUA-340', '2026-08-19', '14:35', '15:05', 'Ética Aplicada: dilemas rápidos do dia a dia', 'Integridade e Futuro', 15),
('QUA-350', '2026-08-19', '15:10', '15:40', 'Segurança da Informação sem Mistério', 'Integridade e Futuro', 15),
('QUA-374', '2026-08-19', '16:10', '16:40', 'IA generativa com responsabilidade no serviço público', 'Integridade e Futuro', 15),
('QUA-333', '2026-08-19', '16:45', '17:15', 'LGPD na Prática: rotina e riscos', 'Integridade e Futuro', 15),
('QUA-339', '2026-08-19', '17:20', '17:50', 'Desinformação e reputação institucional', 'Integridade e Futuro', 15);

-- Quinta-feira (20 de agosto)
INSERT INTO palestras (codigo_palestra, data_palestra, horario_inicio, horario_fim, titulo, trilha, pontos) VALUES
('QUI-430', '2026-08-20', '09:30', '10:00', 'Palestra 430', NULL, 10),
('QUI-476', '2026-08-20', '10:05', '10:35', 'Palestra 476', NULL, 10),
('QUI-463', '2026-08-20', '10:40', '11:10', 'Palestra 463', NULL, 10),
('QUI-460', '2026-08-20', '11:15', '11:45', 'A Judicialização da Prescrição das Pretensões Ressarcitória e Punitiva do TCU no STF', 'Jurídico', 20),
('QUI-429', '2026-08-20', '11:50', '12:20', 'Justiça Plural e Conflitos Territoriais: A Atuação do Núcleo de Conciliação do STF em Causas Indígenas', 'Jurídico', 20),
('QUI-427', '2026-08-20', '14:00', '14:55', 'ECA Digital: Justiça, Tecnologia e Proteção no Ambiente Virtual', 'Integridade e Futuro', 20),
('QUI-417', '2026-08-20', '15:00', '15:30', 'ECA Digital e Uso Seguro da Tecnologia', 'Integridade e Futuro', 15),
('QUI-488', '2026-08-20', '15:35', '16:05', 'Prevenção de Riscos no Ambiente Digital', 'Integridade e Futuro', 15),
('QUI-411', '2026-08-20', '16:30', '17:10', 'Protocolo para Julgamento com Perspectiva de Gênero', 'Integridade e Futuro', 15),
('QUI-467', '2026-08-20', '17:15', '17:45', 'Protocolo para Julgamento com Perspectiva Racial', 'Integridade e Futuro', 15);
