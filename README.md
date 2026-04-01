# Gestor de Tarefas

Aplicação web para gestão de tarefas pessoais, desenvolvida em Python com Flask e SQLite.  
Projeto desenvolvido no âmbito da **UFCD 5425 — Projeto de Tecnologias e Programação de Sistemas de Informação**.

**Autor:** Tiago Almeida  
**Data:** Abril 2026

---

## Funcionalidades

- Registo e autenticação de utilizadores (password com hash SHA-256)
- Criar, editar, eliminar e listar tarefas
- Marcar tarefas como concluídas
- Filtrar por estado (pendente/concluída) e prioridade (alta/média/baixa)
- Pesquisar tarefas por palavra-chave
- Gerir categorias personalizadas
- Dashboard com estatísticas de produtividade

---

## Tecnologias

| Componente | Tecnologia |
|---|---|
| Linguagem | Python 3.10+ |
| Framework | Flask |
| Base de Dados | SQLite |
| Frontend | HTML5 + CSS3 + JavaScript |
| Controlo de Versões | Git + GitHub |

---

## Estrutura do Projeto

```
gestor-tarefas/
├── server.py        # Servidor Flask — rotas e API REST
├── database.py      # Inicialização da base de dados SQLite
├── auth.py          # Autenticação: registo, login, logout
├── tasks.py         # CRUD de tarefas, filtros e pesquisa
├── categories.py    # Gestão de categorias
├── reports.py       # Estatísticas e dashboard
├── index.html       # Interface web (frontend)
├── requirements.txt # Dependências Python
└── README.md        # Este ficheiro
```

---

## Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior
- pip

### Passos

**1. Clonar o repositório**
```bash
git clone https://github.com/TiagoAlmeida/gestor-tarefas.git
cd gestor-tarefas
```

**2. Instalar dependências**
```bash
pip install -r requirements.txt
```

**3. Executar a aplicação**
```bash
python server.py
```

**4. Abrir no browser**
```
http://localhost:5000
```

---

## API REST

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/register` | Registar utilizador |
| POST | `/api/login` | Autenticar utilizador |
| GET | `/api/tasks?uid=` | Listar tarefas |
| POST | `/api/tasks` | Criar tarefa |
| PUT | `/api/tasks/<id>` | Editar / concluir tarefa |
| DELETE | `/api/tasks/<id>` | Eliminar tarefa |
| GET | `/api/categories?uid=` | Listar categorias |
| POST | `/api/categories` | Criar categoria |
| DELETE | `/api/categories/<id>` | Eliminar categoria |
| GET | `/api/reports?uid=` | Estatísticas |

---

## Metodologia

Projeto desenvolvido com a framework **Scrum**, organizado em **7 sprints** semanais:

| Sprint | Aula | Objetivos |
|---|---|---|
| Sprint 1 | Aula 4 | Setup, ambiente e autenticação |
| Sprint 2 | Aula 5 | CRUD de tarefas |
| Sprint 3 | Aula 6 | Filtros, pesquisa e categorias |
| Sprint 4 | Aula 7 | Dashboard e relatórios |
| Sprint 5 | Aula 8 | Testes e qualidade |
| Sprint 6 | Aula 9 | Relatório e documentação |
| Sprint 7 | Aula 10 | Apresentação e deployment |

---

## Licença

Projeto académico — UFCD 5425 © 2026 Tiago Almeida
