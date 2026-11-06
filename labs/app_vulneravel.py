"""CONTROLE INSEGURO: somente laboratório local, nunca publicar como serviço.

Senhas e usuários usados nos testes são fictícios. A concatenação abaixo
é proposital para demonstrar SQL Injection e comparar com app.py.
"""


def login(db, username, password):
    query = (
        "SELECT id, username FROM users WHERE username = '" + username
        + "' AND password = '" + password + "'"
    )
    return db.execute(query).fetchone()
