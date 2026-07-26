import os
from datetime import timedelta

from flask import Flask, jsonify, redirect, render_template, request, url_for
from psycopg.errors import UniqueViolation

from database import Database, DatabaseConfigurationError
from validators import (
    ValidationError,
    normalize_ranking_search,
    validate_checkin,
    validate_registration,
)


def create_app():
    app = Flask(__name__)
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
            return render_template("inscricao.html", form_data=form_data, error=str(error)), 400
        except UniqueViolation as error:
            message = "Esta matrícula STF já está cadastrada."
            if "participantes_cpf_key" in str(error):
                message = "Este CPF já está cadastrado."
            return render_template("inscricao.html", form_data=form_data, error=message), 409
        except DatabaseConfigurationError:
            return render_template(
                "inscricao.html",
                form_data=form_data,
                error="O banco de dados ainda não foi configurado.",
            ), 503

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
            return render_template("checkin.html", form_data=form_data, error=str(error)), 400
        except UniqueViolation:
            return render_template(
                "checkin.html",
                form_data=form_data,
                error="Este check-in já foi registrado para esta palestra.",
            ), 409
        except DatabaseConfigurationError:
            return render_template(
                "checkin.html", form_data=form_data, error="O banco de dados ainda não foi configurado."
            ), 503

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
            return jsonify({"error": str(error)}), 400
        except DatabaseConfigurationError:
            return jsonify({"error": "O banco de dados ainda não foi configurado."}), 503

        return jsonify({"ranking": rows})

    return app


app = create_app()
