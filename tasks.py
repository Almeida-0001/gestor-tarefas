# tasks.py - Módulo de gestão de tarefas (CRUD, filtros, pesquisa)

from database import get_connection


def _query_tarefas(utilizador_id: int, where_extra="", params_extra=()):
    """Query base para listar tarefas com JOIN à categoria."""
    sql = """
        SELECT t.*, c.nome AS categoria_nome
        FROM tarefas t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        WHERE t.utilizador_id = ?
    """
    if where_extra:
        sql += " AND " + where_extra
    sql += " ORDER BY CASE t.prioridade WHEN 'alta' THEN 1 WHEN 'media' THEN 2 ELSE 3 END, t.data_limite ASC"
    conn = get_connection()
    try:
        rows = conn.execute(sql, (utilizador_id,) + params_extra).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def listar_tarefas(utilizador_id: int) -> list:
    """Lista todas as tarefas do utilizador."""
    return _query_tarefas(utilizador_id)


def filtrar_tarefas(utilizador_id: int, estado: str = None, prioridade: str = None) -> list:
    """Filtra tarefas por estado e/ou prioridade."""
    conditions = []
    params = []
    if estado == "concluida":
        conditions.append("t.concluida = 1")
    elif estado == "pendente":
        conditions.append("t.concluida = 0")
    if prioridade in ("alta", "media", "baixa"):
        conditions.append("t.prioridade = ?")
        params.append(prioridade)
    where = " AND ".join(conditions) if conditions else ""
    return _query_tarefas(utilizador_id, where, tuple(params))


def pesquisar_tarefas(utilizador_id: int, palavra: str) -> list:
    """Pesquisa tarefas por palavra-chave na descrição."""
    return _query_tarefas(utilizador_id,
                          "(t.descricao LIKE ?)",
                          (f"%{palavra}%",))


def criar_tarefa(descricao: str, data_limite: str, prioridade: str,
                 utilizador_id: int, categoria_id=None) -> tuple[bool, str]:
    """Cria uma nova tarefa. Retorna (sucesso, mensagem)."""
    if len(descricao.strip()) < 2:
        return False, "A descrição deve ter pelo menos 2 caracteres."
    if prioridade not in ("alta", "media", "baixa"):
        prioridade = "media"
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO tarefas (descricao, data_limite, prioridade, utilizador_id, categoria_id)
               VALUES (?, ?, ?, ?, ?)""",
            (descricao.strip(), data_limite.strip() or None, prioridade, utilizador_id, categoria_id)
        )
        conn.commit()
        return True, "Tarefa adicionada com sucesso!"
    except Exception as e:
        return False, f"Erro ao criar tarefa: {e}"
    finally:
        conn.close()


def editar_tarefa(tarefa_id: int, utilizador_id: int,
                  descricao: str, data_limite: str,
                  prioridade: str, categoria_id=None) -> tuple[bool, str]:
    """Edita uma tarefa existente."""
    if prioridade not in ("alta", "media", "baixa"):
        prioridade = "media"
    conn = get_connection()
    try:
        result = conn.execute(
            """UPDATE tarefas SET descricao=?, data_limite=?, prioridade=?, categoria_id=?
               WHERE id=? AND utilizador_id=?""",
            (descricao.strip(), data_limite.strip() or None, prioridade,
             categoria_id, tarefa_id, utilizador_id)
        )
        conn.commit()
        if result.rowcount == 0:
            return False, "Tarefa não encontrada."
        return True, "Tarefa editada com sucesso!"
    finally:
        conn.close()


def concluir_tarefa(tarefa_id: int, utilizador_id: int) -> tuple[bool, str]:
    """Alterna o estado concluída/pendente de uma tarefa."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT concluida FROM tarefas WHERE id = ? AND utilizador_id = ?",
            (tarefa_id, utilizador_id)
        ).fetchone()
        if not row:
            return False, "Tarefa não encontrada."
        novo_estado = 0 if row["concluida"] else 1
        conn.execute(
            "UPDATE tarefas SET concluida = ? WHERE id = ? AND utilizador_id = ?",
            (novo_estado, tarefa_id, utilizador_id)
        )
        conn.commit()
        msg = "Tarefa marcada como concluída!" if novo_estado else "Tarefa marcada como pendente!"
        return True, msg
    finally:
        conn.close()


def eliminar_tarefa(tarefa_id: int, utilizador_id: int) -> tuple[bool, str]:
    """Elimina uma tarefa."""
    conn = get_connection()
    try:
        result = conn.execute(
            "DELETE FROM tarefas WHERE id = ? AND utilizador_id = ?",
            (tarefa_id, utilizador_id)
        )
        conn.commit()
        if result.rowcount == 0:
            return False, "Tarefa não encontrada."
        return True, "Tarefa removida com sucesso!"
    finally:
        conn.close()


def obter_tarefa(tarefa_id: int, utilizador_id: int):
    """Retorna uma tarefa pelo ID ou None."""
    conn = get_connection()
    try:
        row = conn.execute(
            """SELECT t.*, c.nome AS categoria_nome FROM tarefas t
               LEFT JOIN categorias c ON t.categoria_id = c.id
               WHERE t.id = ? AND t.utilizador_id = ?""",
            (tarefa_id, utilizador_id)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
