"""Testes locais: somente SQLite em memória e credenciais fictícias."""
import importlib.util
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_login(relative):
    path = ROOT / relative
    if not path.exists():
        raise AssertionError(f'Implementação ausente: {relative}')
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.login


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
        self.db.executemany('INSERT INTO users (username, password) VALUES (?, ?)', [
            ('alice', 'senha-ficticia'), ("d\'avila", 'outra-ficticia')])

    def test_login_legitimo(self):
        login = load_login('app.py')
        self.assertIsNotNone(login, 'Implementar app.py com login(db, username, password)')
        self.assertEqual(login(self.db, 'alice', 'senha-ficticia'), (1, 'alice'))

    def test_controle_vulneravel_permite_bypass(self):
        login = load_login('labs/app_vulneravel.py')
        self.assertIsNotNone(login, 'Criar controle positivo vulnerável isolado')
        self.assertEqual(login(self.db, "alice' -- ", 'errada'), (1, 'alice'))

    def test_corrigido_rejeita_senha_errada(self):
        self.assertIsNone(load_login('app.py')(self.db, 'alice', 'errada'))

    def test_corrigido_rejeita_usuario_inexistente(self):
        self.assertIsNone(load_login('app.py')(self.db, 'ninguem', 'senha-ficticia'))

    def test_corrigido_preserva_apostrofo_legitimo(self):
        self.assertEqual(load_login('app.py')(self.db, "d'avila", 'outra-ficticia'), (2, "d'avila"))

    def test_corrigido_bloqueia_payloads_usuario(self):
        for payload in ["alice' -- ", "' OR 1=1 -- ", "' OR '1'='1' -- "]:
            with self.subTest(payload=payload):
                self.assertIsNone(load_login('app.py')(self.db, payload, 'errada'))

    def test_corrigido_bloqueia_payload_senha(self):
        self.assertIsNone(load_login('app.py')(self.db, 'alice', "' OR 1=1 -- "))

    def test_corrigido_rejeita_vazios(self):
        self.assertIsNone(load_login('app.py')(self.db, '', ''))

    def test_corrigido_nao_executa_segundo_comando(self):
        self.assertIsNone(load_login('app.py')(self.db, "'; DROP TABLE users; -- ", 'errada'))
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM users').fetchone()[0], 2)


if __name__ == '__main__':
    unittest.main()
