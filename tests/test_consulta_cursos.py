import unittest
from unittest.mock import patch

from app import create_app


class ConsultaCursosRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True

    def test_invalid_cpf_shows_validation_error(self):
        with self.app.test_client() as client:
            response = client.post("/consulta-cursos", data={"cpf": "123"})

        self.assertEqual(response.status_code, 400)
        self.assertIn("CPF", response.get_data(as_text=True))

    def test_valid_cpf_lists_registered_courses(self):
        class FakeDatabase:
            def fetch_one(self, query, params=None):
                return {"nome": "Ana Maria", "cpf": "12345678909", "matricula": "MAT-001"}

            def fetch_all(self, query, params=None):
                return [
                    {
                        "codigo_palestra": "CAP-101",
                        "titulo": "Introdução ao Direito",
                        "pontos": 25,
                        "timestamp": "2026-07-29T10:00:00",
                    }
                ]

        with patch("app.Database.from_environment", return_value=FakeDatabase()):
            with self.app.test_client() as client:
                response = client.post(
                    "/consulta-cursos",
                    data={"cpf": "123.456.789-09"},
                )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ana Maria", response.get_data(as_text=True))
        self.assertIn("Introdução ao Direito", response.get_data(as_text=True))
        self.assertIn("25 pontos", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
