import logging
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, redirect, render_template, request, url_for
from psycopg.errors import IntegrityError

from database import Database, DatabaseConfigurationError
from validators import (
    ValidationError,
    normalize_ranking_search,
    validate_checkin,
    validate_registration,
)

# Configurar logging
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


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
            return render_template("inscricao.html", form_data=form_data)

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
            return render_template("inscricao.html", form_data=form_data, error=str(error)), 400
        except IntegrityError as error:
            message = "Esta matrícula STF já está cadastrada."
            if error.diag.constraint_name == "participantes_cpf_key":
                message = "Este CPF já está cadastrado."
                logger.warning(f"Duplicate CPF attempt: {form_data.get('cpf')[:3]}***")
            else:
                logger.warning(f"Duplicate matricula attempt: {form_data.get('matricula')}")
            return render_template("inscricao.html", form_data=form_data, error=message), 409
        except DatabaseConfigurationError:
            logger.error("Database not configured in registration")
            return render_template(
                "inscricao.html",
                form_data=form_data,
                error="O banco de dados ainda não foi configurado.",
            ), 503
        except Exception as error:
            logger.exception("Unexpected error in registration")
            return render_template(
                "inscricao.html",
                form_data=form_data,
                error=f"Erro interno do servidor: {error}",
            ), 500

        return render_template("inscricao.html", form_data={}, success="Inscrição realizada com sucesso!")

    @app.route("/checkin", methods=["GET", "POST"])
    def checkin():
        form_data = {"matricula": "", "codigo_palestra": ""}
        if request.method == "GET":
            return render_template("checkin.html", form_data=form_data)

        form_data.update(request.form.to_dict())
        try:
            attendance = validate_checkin(form_data)
            db = database()
            participant_exists = db.fetch_one(
                "SELECT 1 FROM participantes WHERE matricula = %(matricula)s", attendance
            )
            if not participant_exists:
                raise ValidationError("Matrícula STF não encontrada. Faça a inscrição antes do check-in.")

            session_exists = db.fetch_one(
                "SELECT 1 FROM palestras WHERE codigo_palestra = %(codigo_palestra)s", attendance
            )
            if not session_exists:
                raise ValidationError("Código de palestra inválido.")

            db.execute(
                """
                INSERT INTO registros_presenca (matricula, codigo_palestra)
                VALUES (%(matricula)s, %(codigo_palestra)s)
                """,
                attendance,
            )
        except ValidationError as error:
            logger.warning(f"Validation error in check-in: {str(error)}")
            return render_template("checkin.html", form_data=form_data, error=str(error)), 400
        except IntegrityError as error:
            if error.diag.constraint_name == "registros_presenca_matricula_codigo_palestra_key":
                logger.warning(f"Duplicate check-in attempt: {form_data.get('matricula')} - {form_data.get('codigo_palestra')}")
                return render_template(
                    "checkin.html",
                    form_data=form_data,
                    error="Este check-in já foi registrado para esta palestra.",
                ), 409
            raise
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

        return render_template("checkin.html", form_data={}, success="Check-in registrado com sucesso!")

    @app.get("/ranking")
    def ranking():
        return render_template("ranking.html")

    @app.get("/api/ranking")
    def ranking_api():
        matricula = request.args.get("matricula", "").strip()
        try:
            if matricula:
                matricula = normalize_ranking_search(matricula)
            rows = database().fetch_all(
                """
                WITH pontuacao AS (
                    SELECT
                        rp.matricula,
                        SUM(p.pontos)::integer AS pontos,
                        MIN(rp.timestamp) AS primeiro_checkin
                    FROM registros_presenca rp
                    JOIN palestras p ON p.codigo_palestra = rp.codigo_palestra
                    GROUP BY rp.matricula
                ), ranking AS (
                    SELECT
                        ROW_NUMBER() OVER (
                            ORDER BY pontos DESC, primeiro_checkin ASC, matricula ASC
                        ) AS posicao,
                        matricula,
                        pontos
                    FROM pontuacao
                )
                SELECT posicao, matricula, pontos
                FROM ranking
                WHERE (%(matricula)s = '' OR matricula = %(matricula)s)
                ORDER BY posicao
                """,
                {"matricula": matricula},
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
