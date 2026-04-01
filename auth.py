# auth.py - Módulo de autenticação (registo, login, logout)

import hashlib
import os
from database import get_connection

# Utilizador atualmente autenticado (sessão em memória)
_sessao_utilizador = None


def _hash_password(password: str) -> str:
    """Gera um hash SHA-256 da password com salt."""
    salt = "ufcd5425_gestor"  # salt fixo simples para o projeto
    return hashlib.sha256((salt + password).encode()).hexdigest()


def registar(username: str, password: str) -> tuple[bool, str]:
    """Regista um novo utilizador. Retorna (sucesso, mensagem)."""
    if len(username.strip()) < 3:
        return False, "O username deve ter pelo menos 3 caracteres."
    if len(password) < 4:
        return False, "A password deve ter pelo menos 4 caracteres."

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO utilizadores (username, password_hash) VALUES (?, ?)",
            (username.strip(), _hash_password(password))
        )
        conn.commit()
        return True, f"Utilizador '{username}' registado com sucesso!"
    except Exception:
        return False, f"Erro: o username '{username}' já existe."
    finally:
        conn.close()


def login(username: str, password: str) -> tuple[bool, str]:
    """Autentica o utilizador. Retorna (sucesso, mensagem)."""
    global _sessao_utilizador
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM utilizadores WHERE username = ? AND password_hash = ?",
            (username.strip(), _hash_password(password))
        ).fetchone()

        if row:
            _sessao_utilizador = dict(row)
            return True, f"Bem-vindo, {username}!"
        else:
            return False, "Username ou password incorretos."
    finally:
        conn.close()


def logout():
    """Termina a sessão do utilizador atual."""
    global _sessao_utilizador
    nome = _sessao_utilizador["username"] if _sessao_utilizador else ""
    _sessao_utilizador = None
    return nome


def utilizador_atual():
    """Retorna o utilizador autenticado ou None."""
    return _sessao_utilizador


def requer_login():
    """Retorna True se há utilizador autenticado."""
    return _sessao_utilizador is not None
