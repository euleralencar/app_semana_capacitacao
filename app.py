import logging
import os
import re
from datetime import timedelta
from pathlib import Path

from dotenv import dotenv_values, find_dotenv
from flask import Flask, jsonify, make_response, redirect, render_template, request, url_for
from psycopg.errors import IntegrityError

from database import Database, DatabaseConfigurationError
from validators import (
    SECRETARIA_OPTIONS,
    ValidationError,
    normalize_cpf,
    normalize_ranking_search,
    validate_checkin,
    validate_registration,
)

# Configurar logging
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
env_path = find_dotenv(usecwd=True) or BASE_DIR / ".env"
if env_path:
    for key, value in dotenv_values(env_path).items():
        if value is not None:
            os.environ[key] = value


def create_app():
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.config.update(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "desenvolvimento-altere-esta-chave"),
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    )

    def database():
        return Database.from_environment()

    @app.get("/")
    def home():
        return redirect(url_for("inscricao"))

    @app.route("/inscricao", methods=["GET", "POST"])
    def inscricao():
        form_data = {"nome": "", "matricula": "", "cpf": "", "secretaria": ""}
        if request.method == "GET":
            return render_template(
                "inscricao.html",
                form_data=form_data,
                secretarias=SECRETARIA_OPTIONS,
            )

        form_data.update(request.form.to_dict())
        try:
            participant = validate_registration(form_data)
            database().execute(
                """
                INSERT INTO participantes (matricula, cpf, nome, secretaria)
                VALUES (%(matricula)s, %(cpf)s, %(nome)s, %(secretaria)s)
                """,
                participant,
            )
        except ValidationError as error:
            logger.warning(f"Validation error in registration: {str(error)}")
            return render_template(
                "inscricao.html",
                form_data=form_data,
                secretarias=SECRETARIA_OPTIONS,
                error=str(error),
            ), 400
        except IntegrityError as error:
            message = (
                "Esta matrícula STF já está cadastrada. Procure a equipe da organização "
                "se precisar alterar alguma informação da inscrição."
            )
            if error.diag.constraint_name == "participantes_cpf_key":
                message = (
                    "Este CPF já está cadastrado. Procure a equipe da organização "
                    "se precisar alterar alguma informação da inscrição."
                )
                logger.warning(f"Duplicate CPF attempt: {form_data.get('cpf')[:3]}***")
            else:
                logger.warning(f"Duplicate matricula attempt: {form_data.get('matricula')}")
            return render_template(
                "inscricao.html",
                form_data=form_data,
                secretarias=SECRETARIA_OPTIONS,
                error=message,
            ), 409
        except DatabaseConfigurationError:
            logger.error("Database not configured in registration")
            return render_template(
                "inscricao.html",
                form_data=form_data,
                secretarias=SECRETARIA_OPTIONS,
                error="O banco de dados ainda não foi configurado.",
            ), 503
        except Exception as error:
            logger.exception("Unexpected error in registration")
            return render_template(
                "inscricao.html",
                form_data=form_data,
                secretarias=SECRETARIA_OPTIONS,
                error=f"Erro interno do servidor: {error}",
            ), 500

        return render_template(
            "inscricao.html",
            form_data={"nome": "", "matricula": "", "cpf": "", "secretaria": ""},
            secretarias=SECRETARIA_OPTIONS,
            success="Inscrição realizada com sucesso!",
        )

    @app.route("/checkin", methods=["GET", "POST"])
    def checkin():
        form_data = {"cpf": "", "codigo_palestra": ""}
        if request.method == "GET":
            return render_template("checkin.html", form_data=form_data)

        form_data.update(request.form.to_dict())
        try:
            attendance = validate_checkin(form_data)
            db = database()
            participant_exists = db.fetch_one(
                """
                SELECT matricula, nome, cpf
                FROM participantes
                WHERE LPAD(REGEXP_REPLACE(cpf::text, '\\D', '', 'g'), 11, '0') = %(cpf)s
                ORDER BY data_cadastro DESC, matricula DESC
                LIMIT 1
                """,
                attendance,
            )
            if not participant_exists:
                raise ValidationError("CPF não encontrado. Faça a inscrição antes do check-in.")

            session_exists = db.fetch_one(
                "SELECT 1 FROM palestras WHERE codigo_palestra = %(codigo_palestra)s", attendance
            )
            if not session_exists:
                raise ValidationError("Código de palestra inválido.")

            attendance["matricula"] = participant_exists["matricula"]

            # Inserção defensiva para concorrência: se duas requisições chegarem ao mesmo tempo
            # para o mesmo participante e palestra, a restrição UNIQUE do banco evita duplicidade.
            inserted = db.fetch_one(
                """
                INSERT INTO registros_presenca (matricula, codigo_palestra)
                VALUES (%(matricula)s, %(codigo_palestra)s)
                ON CONFLICT (matricula, codigo_palestra) DO NOTHING
                RETURNING id
                """,
                attendance,
            )
            if not inserted:
                return render_template(
                    "checkin.html",
                    form_data=form_data,
                    error="Este check-in já foi registrado para esta palestra.",
                ), 409
        except ValidationError as error:
            logger.warning(f"Validation error in check-in: {str(error)}")
            return render_template("checkin.html", form_data=form_data, error=str(error)), 400
        except DatabaseConfigurationError:
            logger.error("Database not configured in check-in")
            return render_template(
                "checkin.html", form_data=form_data, error="O banco de dados ainda não foi configurado."
            ), 503
        except Exception as error:
            logger.exception("Unexpected error in check-in")
            return render_template(
                "checkin.html",
                form_data=form_data,
                error=f"Erro interno do servidor: {error}",
            ), 500

        return render_template("checkin.html", form_data={"cpf": "", "codigo_palestra": ""}, success="Check-in registrado com sucesso!")

    @app.route("/consulta-cursos", methods=["GET", "POST"])
    def consulta_cursos():
        form_data = {"cpf": ""}
        if request.method == "GET":
            return render_template("consulta_cursos.html", form_data=form_data)

        form_data.update(request.form.to_dict())
        try:
            cpf = normalize_cpf(form_data.get("cpf", ""))
            db = database()
            participant = db.fetch_one(
                """
                SELECT matricula, cpf, nome
                FROM participantes
                WHERE LPAD(REGEXP_REPLACE(cpf::text, '\\D', '', 'g'), 11, '0') = %(cpf)s
                ORDER BY data_cadastro DESC, matricula DESC
                LIMIT 1
                """,
                {"cpf": cpf},
            )
            if not participant:
                raise ValidationError("Nenhum participante encontrado para este CPF.")

            cursos = db.fetch_all(
                """
                SELECT rp.codigo_palestra, p.titulo, p.trilha, p.pontos, rp.timestamp
                FROM registros_presenca rp
                JOIN palestras p ON p.codigo_palestra = rp.codigo_palestra
                WHERE rp.matricula = %(matricula)s
                ORDER BY rp.timestamp ASC, p.titulo ASC
                """,
                {"matricula": participant["matricula"]},
            )
        except ValidationError as error:
            logger.warning(f"Validation error in course lookup: {str(error)}")
            return render_template("consulta_cursos.html", form_data=form_data, error=str(error)), 400
        except DatabaseConfigurationError:
            logger.error("Database not configured in course lookup")
            return render_template(
                "consulta_cursos.html",
                form_data=form_data,
                error="O banco de dados ainda não foi configurado.",
            ), 503
        except Exception as error:
            logger.exception("Unexpected error in course lookup")
            return render_template(
                "consulta_cursos.html",
                form_data=form_data,
                error=f"Erro interno do servidor: {error}",
            ), 500

        total_pontos = sum(curso.get("pontos", 0) for curso in cursos)
        return render_template(
            "consulta_cursos.html",
            form_data={"cpf": cpf},
            result={
                "nome": participant["nome"],
                "cpf": participant["cpf"],
                "matricula": participant["matricula"],
                "cursos": cursos,
                "total_pontos": total_pontos,
            },
        )

    @app.get("/ranking")
    def ranking():
        return render_template("ranking.html")

    @app.get("/api/ranking")
    def ranking_api():
        search_term = request.args.get("matricula", "").strip()
        try:
            if search_term:
                search_term = normalize_ranking_search(search_term)
            rows = database().fetch_all(
                """
                WITH pontuacao AS (
                    SELECT
                        rp.matricula,
                        LPAD(REGEXP_REPLACE(pa.cpf::text, '\\D', '', 'g'), 11, '0') AS cpf,
                        SUM(p.pontos)::integer AS pontos,
                        MIN(rp.timestamp) AS primeiro_checkin
                    FROM registros_presenca rp
                    JOIN participantes pa ON pa.matricula = rp.matricula
                    JOIN palestras p ON p.codigo_palestra = rp.codigo_palestra
                    GROUP BY rp.matricula, pa.cpf
                ), ranking AS (
                    SELECT
                        ROW_NUMBER() OVER (
                            ORDER BY pontos DESC, primeiro_checkin ASC, matricula ASC
                        ) AS posicao,
                        matricula,
                        cpf,
                        CONCAT(
                            SUBSTRING(cpf, 1, 3),
                            '.***.***-',
                            SUBSTRING(cpf, 10, 2)
                        ) AS cpf_mascarado,
                        pontos
                    FROM pontuacao
                )
                SELECT posicao, matricula, cpf_mascarado, pontos
                FROM ranking
                WHERE (
                    %(search_term)s = ''
                    OR matricula ILIKE CONCAT('%%', %(search_term)s, '%%')
                )
                ORDER BY posicao
                """,
                {
                    "search_term": search_term,
                },
            )
        except ValidationError as error:
            logger.warning(f"Validation error in ranking API: {str(error)}")
            return jsonify({"error": str(error)}), 400
        except DatabaseConfigurationError:
            logger.error("Database not configured in ranking API")
            return jsonify({"error": "O banco de dados ainda não foi configurado."}), 503
        except Exception as error:
            logger.exception("Unexpected error in ranking API")
            return jsonify({"error": f"Erro interno do servidor: {error}"}), 500

        # Adicionar cache headers para reduzir requisições desnecessárias
        response = make_response(jsonify({"ranking": rows}))
        response.headers["Cache-Control"] = "max-age=2, public"
        return response

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
