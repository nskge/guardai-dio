"""Login didático local. Dados fictícios; não é autenticação para produção."""


def login(db, username, password):
    """Retorna (id, username) ou None, separando os dados do SQL."""
    return db.execute(
        'SELECT id, username FROM users WHERE username = ? AND password = ?',
        (username, password),
    ).fetchone()
