## Plano — Semana da Capacitação 2026

### 1. Stack e hospedagem

- Aplicação web: **Flask + HTML + Tailwind CSS**
- Banco de dados: **Supabase (PostgreSQL)**
- Hospedagem: **Vercel**
- Atualização do ranking: consulta automática a cada poucos segundos.
- Configuração local: arquivo `.env` carregado com `python-dotenv`; credenciais não são versionadas.

### 2. Funcionalidades

**Inscrição**

Campos:

- Nome completo
- Matrícula STF
- CPF
- Secretaria

Regras:

- Matrícula STF única.
- CPF validado antes do envio.
- Confirmação clara após o cadastro.
- Secretaria mantida apenas para controle administrativo.

**Check-in**

Campos:

- Matrícula STF
- Código da palestra, por exemplo `CAP-101`

Regras:

- Confere se participante e palestra existem.
- Registra data e horário da presença.
- Não permite dois check-ins da mesma matrícula na mesma palestra.
- Cada palestra possui uma pontuação configurada.

**Ranking**

Ranking público com:

| Posição | Matrícula STF | Pontos |
|---:|---|---:|

Regras:

- Não exibe nomes ou secretarias.
- Ordenação por maior pontuação.
- Empates são resolvidos pelo horário do primeiro check-in.
- Campo de busca por matrícula para a pessoa localizar rapidamente sua posição e pontuação.

### 3. Estrutura do banco

```text
participantes
- matricula (PK)
- cpf (único)
- nome
- secretaria
- data_cadastro

palestras
- codigo_palestra (PK)
- titulo
- pontos

registros_presenca
- id (PK)
- matricula (FK → participantes)
- codigo_palestra (FK → palestras)
- timestamp
- UNIQUE(matricula, codigo_palestra)
```

### 4. Estrutura de arquivos

```text
semana-capacitacao-2026/
├── api/
│   └── index.py
├── app.py
├── database.py
├── validators.py
├── templates/
│   ├── base.html
│   ├── inscricao.html
│   ├── checkin.html
│   └── ranking.html
├── static/
│   ├── css/app.css
│   └── js/ranking.js
├── sql/
│   ├── schema.sql
│   └── seed_palestras.sql
├── requirements.txt
├── vercel.json
├── .env.example
├── .gitignore
├── agents.MD
└── README.md
```

### 5. Andamento do desenvolvimento

- [x] Criar o projeto Supabase e executar o esquema SQL.
- [x] Criar a lista inicial de palestras e respectivas pontuações.
- [x] Implementar conexão segura e consultas ao banco por `DATABASE_URL`.
- [x] Desenvolver as telas de inscrição, check-in e ranking.
- [x] Aplicar validações de CPF, matrícula, palestra e mensagens de retorno.
- [x] Implementar busca de posição por matrícula e atualização automática do ranking a cada 5 segundos.
- [x] Configurar ambiente local, validar dependências e testar a aplicação localmente.
- [x] Inicializar o Git e publicar a base do projeto no GitHub.
- [ ] Configurar as variáveis `DATABASE_URL` e `FLASK_SECRET_KEY` na Vercel e realizar o deploy.
- [ ] Executar os testes finais: cadastro repetido, código inválido, check-in duplicado, empate e busca no ranking.
