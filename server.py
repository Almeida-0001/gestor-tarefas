# server.py - Servidor Flask do Gestor de Tarefas
# Executa: python server.py
# Depois abre o browser em: http://localhost:5000

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, send_from_directory
import database
import auth
import tasks
import categories
import reports

app = Flask(__name__, static_folder='.')

# ─────────────────────────────────────────────
#  PÁGINA PRINCIPAL
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


# ─────────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────────

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    ok, msg = auth.registar(data.get('username',''), data.get('password',''))
    return jsonify({'ok': ok, 'msg': msg})


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    ok, msg = auth.login(data.get('username',''), data.get('password',''))
    if ok:
        u = auth.utilizador_atual()
        return jsonify({'ok': True, 'msg': msg, 'user': {'id': u['id'], 'username': u['username']}})
    return jsonify({'ok': False, 'msg': msg})


# ─────────────────────────────────────────────
#  TAREFAS
# ─────────────────────────────────────────────

@app.route('/api/tasks', methods=['GET'])
def api_tasks_list():
    uid = request.args.get('uid', type=int)
    estado    = request.args.get('estado')
    prioridade= request.args.get('prioridade')
    pesquisa  = request.args.get('q')

    if pesquisa:
        lista = tasks.pesquisar_tarefas(uid, pesquisa)
    elif estado or prioridade:
        lista = tasks.filtrar_tarefas(uid, estado, prioridade)
    else:
        lista = tasks.listar_tarefas(uid)

    return jsonify(lista)


@app.route('/api/tasks', methods=['POST'])
def api_tasks_create():
    d = request.json
    ok, msg = tasks.criar_tarefa(
        d.get('descricao',''),
        d.get('data_limite',''),
        d.get('prioridade','media'),
        d.get('utilizador_id'),
        d.get('categoria_id') or None
    )
    if ok:
        lista = tasks.listar_tarefas(d.get('utilizador_id'))
        new_task = lista[-1] if lista else {}
        return jsonify({'ok': True, 'msg': msg, 'task': new_task})
    return jsonify({'ok': False, 'msg': msg})


@app.route('/api/tasks/<int:tid>', methods=['PUT'])
def api_tasks_update(tid):
    d = request.json
    uid = d.get('utilizador_id')

    # Toggle concluída
    if 'toggle' in d:
        ok, msg = tasks.concluir_tarefa(tid, uid)
        task = tasks.obter_tarefa(tid, uid)
        return jsonify({'ok': ok, 'msg': msg, 'task': dict(task) if task else {}})

    # Editar campos
    ok, msg = tasks.editar_tarefa(
        tid, uid,
        d.get('descricao',''),
        d.get('data_limite',''),
        d.get('prioridade','media'),
        d.get('categoria_id') or None
    )
    task = tasks.obter_tarefa(tid, uid)
    return jsonify({'ok': ok, 'msg': msg, 'task': dict(task) if task else {}})


@app.route('/api/tasks/<int:tid>', methods=['DELETE'])
def api_tasks_delete(tid):
    uid = request.args.get('uid', type=int)
    ok, msg = tasks.eliminar_tarefa(tid, uid)
    return jsonify({'ok': ok, 'msg': msg})


# ─────────────────────────────────────────────
#  CATEGORIAS
# ─────────────────────────────────────────────

@app.route('/api/categories', methods=['GET'])
def api_cat_list():
    uid = request.args.get('uid', type=int)
    return jsonify(categories.listar_categorias(uid))


@app.route('/api/categories', methods=['POST'])
def api_cat_create():
    d = request.json
    ok, msg = categories.criar_categoria(d.get('nome',''), d.get('utilizador_id'))
    cats = categories.listar_categorias(d.get('utilizador_id'))
    return jsonify({'ok': ok, 'msg': msg, 'categories': cats})


@app.route('/api/categories/<int:cid>', methods=['DELETE'])
def api_cat_delete(cid):
    uid = request.args.get('uid', type=int)
    ok, msg = categories.eliminar_categoria(cid, uid)
    return jsonify({'ok': ok, 'msg': msg})


# ─────────────────────────────────────────────
#  RELATÓRIO
# ─────────────────────────────────────────────

@app.route('/api/reports', methods=['GET'])
def api_reports():
    uid = request.args.get('uid', type=int)
    return jsonify(reports.gerar_relatorio(uid))


# ─────────────────────────────────────────────
#  ARRANQUE
# ─────────────────────────────────────────────

if __name__ == '__main__':
    database.inicializar_bd()
    print("\n" + "="*50)
    print("  ✅  Gestor de Tarefas — Servidor iniciado!")
    print("="*50)
    print("  Abre o browser em:  http://localhost:5000")
    print("  Para parar:         CTRL + C")
    print("="*50 + "\n")
    app.run(debug=False, port=5000)
