## Plano — Semana da Capacitação 2026

### 1. Stack e hospedagem

- Aplicação web: **Flask + HTML + Tailwind CSS**
- Banco de dados: **Supabase (PostgreSQL)**
- Hospedagem: **Vercel**
- Atualização do ranking: consulta automática a cada poucos segundos.

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
└── README.md
```

### 5. Etapas de desenvolvimento

1. Criar o projeto Supabase e executar o esquema SQL.
2. Implementar conexão segura e consultas ao banco.
3. Desenvolver as telas de inscrição, check-in e ranking.
4. Aplicar validações de dados e mensagens de retorno.
5. Implementar busca de posição por matrícula.
6. Criar lista inicial de palestras e respectivas pontuações.
7. Configurar variáveis de ambiente e deploy na Vercel.
8. Testar cenários de cadastro repetido, código inválido, check-in duplicado, empate e busca no ranking.
