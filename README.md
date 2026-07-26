# Semana da Capacitação 2026

Aplicação Flask para inscrição, check-in de palestras e ranking público, usando Supabase PostgreSQL e Vercel.

## Executar localmente

1. Crie um projeto no Supabase e, no SQL Editor, execute primeiro [`sql/schema.sql`](sql/schema.sql) e depois [`sql/seed_palestras.sql`](sql/seed_palestras.sql).
2. Copie `.env.example` para `.env` e informe a `DATABASE_URL` do pooler do Supabase e uma `FLASK_SECRET_KEY` aleatória.
3. Instale as dependências e execute a aplicação:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   flask --app app run --debug
   ```

Abra `http://127.0.0.1:5000`.

## Deploy na Vercel

1. Importe este repositório na Vercel.
2. Em **Settings → Environment Variables**, cadastre `DATABASE_URL` e `FLASK_SECRET_KEY`.
3. Faça o deploy. O arquivo `vercel.json` encaminha as rotas para a aplicação Flask em `api/index.py`.

## Regras implementadas

- Matrícula e CPF são únicos; o CPF é validado antes do cadastro.
- Check-in valida participante e palestra, registra data/hora e bloqueia duplicidade por palestra.
- O ranking não exibe nome ou secretaria, soma os pontos e resolve empates pelo primeiro check-in.
- A busca por matrícula preserva a posição global no ranking e a tabela é atualizada a cada cinco segundos.
