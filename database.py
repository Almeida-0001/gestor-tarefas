# database.py - Módulo de conexão e inicialização da base de dados SQLite

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "gestor_tarefas.db")


def get_connection():
    """Retorna uma conexão à base de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite aceder às colunas pelo nome
    return conn


def inicializar_bd():
    """Cria as tabelas da base de dados se não existirem."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de utilizadores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilizadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            criado_em TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # Tabela de categorias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            utilizador_id INTEGER NOT NULL,
            FOREIGN KEY (utilizador_id) REFERENCES utilizadores(id),
            UNIQUE (nome, utilizador_id)
        )
    """)

    # Tabela de tarefas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            data_limite TEXT,
            prioridade TEXT DEFAULT 'media' CHECK(prioridade IN ('alta','media','baixa')),
            concluida INTEGER DEFAULT 0,
            utilizador_id INTEGER NOT NULL,
            categoria_id INTEGER,
            criado_em TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (utilizador_id) REFERENCES utilizadores(id),
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    conn.commit()
    conn.close()
