# categories.py - Módulo de gestão de categorias

from database import get_connection


def listar_categorias(utilizador_id: int) -> list:
    """Lista todas as categorias do utilizador."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM categorias WHERE utilizador_id = ? ORDER BY nome",
            (utilizador_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def criar_categoria(nome: str, utilizador_id: int) -> tuple[bool, str]:
    """Cria uma nova categoria. Retorna (sucesso, mensagem)."""
    if len(nome.strip()) < 2:
        return False, "O nome da categoria deve ter pelo menos 2 caracteres."
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO categorias (nome, utilizador_id) VALUES (?, ?)",
            (nome.strip(), utilizador_id)
        )
        conn.commit()
        return True, f"Categoria '{nome}' criada com sucesso!"
    except Exception:
        return False, f"A categoria '{nome}' já existe."
    finally:
        conn.close()


def eliminar_categoria(categoria_id: int, utilizador_id: int) -> tuple[bool, str]:
    """Elimina uma categoria (as tarefas ficam sem categoria)."""
    conn = get_connection()
    try:
        # Verifica se é do utilizador
        row = conn.execute(
            "SELECT nome FROM categorias WHERE id = ? AND utilizador_id = ?",
            (categoria_id, utilizador_id)
        ).fetchone()
        if not row:
            return False, "Categoria não encontrada."
        # Remove a associação nas tarefas
        conn.execute(
            "UPDATE tarefas SET categoria_id = NULL WHERE categoria_id = ?",
            (categoria_id,)
        )
        conn.execute(
            "DELETE FROM categorias WHERE id = ?", (categoria_id,)
        )
        conn.commit()
        return True, f"Categoria '{row['nome']}' eliminada."
    finally:
        conn.close()


def obter_categoria_por_id(categoria_id: int, utilizador_id: int):
    """Retorna uma categoria pelo ID ou None."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM categorias WHERE id = ? AND utilizador_id = ?",
            (categoria_id, utilizador_id)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
