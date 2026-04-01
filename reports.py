# reports.py - Módulo de relatórios e estatísticas

from database import get_connection


def gerar_relatorio(utilizador_id: int) -> dict:
    """Gera estatísticas das tarefas do utilizador."""
    conn = get_connection()
    try:
        total = conn.execute(
            "SELECT COUNT(*) FROM tarefas WHERE utilizador_id = ?",
            (utilizador_id,)
        ).fetchone()[0]

        concluidas = conn.execute(
            "SELECT COUNT(*) FROM tarefas WHERE utilizador_id = ? AND concluida = 1",
            (utilizador_id,)
        ).fetchone()[0]

        por_prioridade = conn.execute(
            """SELECT prioridade, COUNT(*) as total
               FROM tarefas WHERE utilizador_id = ?
               GROUP BY prioridade""",
            (utilizador_id,)
        ).fetchall()

        por_categoria = conn.execute(
            """SELECT COALESCE(c.nome, 'Sem categoria') as categoria, COUNT(*) as total
               FROM tarefas t
               LEFT JOIN categorias c ON t.categoria_id = c.id
               WHERE t.utilizador_id = ?
               GROUP BY c.nome
               ORDER BY total DESC""",
            (utilizador_id,)
        ).fetchall()

        return {
            "total": total,
            "concluidas": concluidas,
            "pendentes": total - concluidas,
            "por_prioridade": {r["prioridade"]: r["total"] for r in por_prioridade},
            "por_categoria": [(r["categoria"], r["total"]) for r in por_categoria]
        }
    finally:
        conn.close()
