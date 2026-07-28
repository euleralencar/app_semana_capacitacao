-- Script para popular palestras do evento
-- Data: 17, 18, 19 e 20 de agosto (segunda a quinta-feira)
-- Horário do evento: 9h30 às 17h50
-- Trilhas: Estágio, Jurídico, Integridade e Futuro
-- Pontuação: 25 pontos por palestra

-- Segunda-feira (17 de agosto)
INSERT INTO palestras (codigo_palestra, data_palestra, horario_inicio, horario_fim, titulo, trilha, pontos) VALUES
('148', '2026-08-17', '09:30', '10:00', 'Palestra 148', NULL, 25),
('118', '2026-08-17', '10:05', '10:35', 'Palestra 118', NULL, 25),
('177', '2026-08-17', '10:40', '11:10', 'Palestra 177', NULL, 25),
('144', '2026-08-17', '11:15', '11:45', 'Palestra 144', NULL, 25),
('171', '2026-08-17', '11:50', '12:20', 'Palestra 171', NULL, 25),
('156', '2026-08-17', '14:30', '15:00', 'Carreira em Construção: do estágio às oportunidades', 'Estágio', 25),
('193', '2026-08-17', '15:05', '15:35', 'Saúde Mental e Estágio: conciliação entre estágio e estudos', 'Estágio', 25),
('128', '2026-08-17', '15:40', '16:10', 'Inclusão no estágio: acolhimento e acessibilidade', 'Estágio', 25),
('137', '2026-08-17', '16:40', '17:10', 'Histórias que inspiram', 'Estágio', 25),
('132', '2026-08-17', '17:15', '17:45', 'Carreira e Imagem', 'Estágio', 25);

-- Terça-feira (18 de agosto)
INSERT INTO palestras (codigo_palestra, data_palestra, horario_inicio, horario_fim, titulo, trilha, pontos) VALUES
('218', '2026-08-18', '09:30', '10:00', 'Palestra 218', NULL, 25),
('212', '2026-08-18', '10:05', '10:35', 'Palestra 212', NULL, 25),
('220', '2026-08-18', '10:40', '11:10', 'Além do mito centralista: O papel descentralizador do STF nos Conflitos Federativos em Ações Cíveis Originárias', 'Jurídico', 25),
('262', '2026-08-18', '11:15', '11:45', 'Decisões Estruturantes de Natureza Penal: Um Estudo de Caso Sobre a Determinação do Uso de Câmeras Corporais em Operações Policiais', 'Jurídico', 25),
('268', '2026-08-18', '11:50', '12:20', 'ADPF 635: Estudo de Caso sobre Obstáculos e Avanços no Combate à Violência Policial e o Racismo', 'Jurídico', 25),
('297', '2026-08-18', '14:00', '14:30', 'Carreira em Construção: do estágio às oportunidades', 'Estágio', 25),
('219', '2026-08-18', '14:35', '15:05', 'Saúde Mental e Estágio: conciliação entre estágio e estudos', 'Estágio', 25),
('272', '2026-08-18', '15:10', '15:40', 'Inclusão no estágio: acolhimento e acessibilidade', 'Estágio', 25),
('269', '2026-08-18', '16:10', '16:40', 'Histórias que inspiram', 'Estágio', 25),
('234', '2026-08-18', '16:45', '17:15', 'Carreira e Imagem', 'Estágio', 25);

-- Quarta-feira (19 de agosto)
INSERT INTO palestras (codigo_palestra, data_palestra, horario_inicio, horario_fim, titulo, trilha, pontos) VALUES
('326', '2026-08-19', '09:30', '10:00', 'Palestra 326', NULL, 25),
('399', '2026-08-19', '10:05', '10:35', 'Palestra 399', NULL, 25),
('373', '2026-08-19', '10:40', '11:10', 'Os Impactos do Habeas Corpus Coletivo N.º 143.641/SP no Desencarceramento das Mulheres e na Construção de Políticas Públicas por Meio do Julgamento de Litígios Estruturais', 'Jurídico', 25),
('311', '2026-08-19', '11:15', '11:45', 'O Poder Judiciário e a Intervenção em Políticas Públicas: Análise dos Juízos de Retratação no Tema 698', 'Jurídico', 25),
('389', '2026-08-19', '11:50', '12:20', 'Deferência Judicial: Um Estudo Empírico no Âmbito do Supremo Tribunal Federal sobre o Controle das Agências Reguladoras', 'Jurídico', 25),
('328', '2026-08-19', '14:00', '14:30', 'Governança e Integridade: como cada papel protege o STF', 'Integridade e Futuro', 25),
('340', '2026-08-19', '14:35', '15:05', 'Ética Aplicada: dilemas rápidos do dia a dia', 'Integridade e Futuro', 25),
('350', '2026-08-19', '15:10', '15:40', 'Segurança da Informação sem Mistério', 'Integridade e Futuro', 25),
('374', '2026-08-19', '16:10', '16:40', 'IA generativa com responsabilidade no serviço público', 'Integridade e Futuro', 25),
('333', '2026-08-19', '16:45', '17:15', 'LGPD na Prática: rotina e riscos', 'Integridade e Futuro', 25),
('339', '2026-08-19', '17:20', '17:50', 'Desinformação e reputação institucional', 'Integridade e Futuro', 25);

-- Quinta-feira (20 de agosto)
INSERT INTO palestras (codigo_palestra, data_palestra, horario_inicio, horario_fim, titulo, trilha, pontos) VALUES
('430', '2026-08-20', '09:30', '10:00', 'Palestra 430', NULL, 25),
('476', '2026-08-20', '10:05', '10:35', 'Palestra 476', NULL, 25),
('463', '2026-08-20', '10:40', '11:10', 'Palestra 463', NULL, 25),
('460', '2026-08-20', '11:15', '11:45', 'A Judicialização da Prescrição das Pretensões Ressarcitória e Punitiva do TCU no STF', 'Jurídico', 25),
('429', '2026-08-20', '11:50', '12:20', 'Justiça Plural e Conflitos Territoriais: A Atuação do Núcleo de Conciliação do STF em Causas Indígenas', 'Jurídico', 25),
('427', '2026-08-20', '14:00', '14:55', 'ECA Digital: Justiça, Tecnologia e Proteção no Ambiente Virtual', 'Integridade e Futuro', 25),
('417', '2026-08-20', '15:00', '15:30', 'ECA Digital e Uso Seguro da Tecnologia', 'Integridade e Futuro', 25),
('488', '2026-08-20', '15:35', '16:05', 'Prevenção de Riscos no Ambiente Digital', 'Integridade e Futuro', 25),
('411', '2026-08-20', '16:30', '17:10', 'Protocolo para Julgamento com Perspectiva de Gênero', 'Integridade e Futuro', 25),
('467', '2026-08-20', '17:15', '17:45', 'Protocolo para Julgamento com Perspectiva Racial', 'Integridade e Futuro', 25);
