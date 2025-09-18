# 🦝 Off-the-Shelf AI Agent (Python • FastAPI • Gradio • Railway • PostgreSQL)

A production-ready template for building and deploying tool-using AI agents. It emphasizes **dependency compatibility**, **clean architecture**, and **straightforward deployment** to **Railway** using **Docker**. Dev UX is powered by **uv** and **ruff**.

---

## 📁 Project Structure (Revised for FastAPI)

```
.
├─ src/
│  ├─ app/
│  │  ├─ main.py                 # App entrypoint, creates FastAPI instance
│  │  ├─ core/
│  │  │  ├─ config.py            # Settings classes (DevSettings, ProdSettings)
│  │  │  ├─ init_settings.py     # CLI arg parsing, mode selection, settings initialization
│  │  │  ├─ container.py         # Dependency injection container (engines, sessions, clients)
│  │  │  └─ logging.py           # Structured logging setup
│  │  ├─ lifecycle/
│  │  │  └─ lifespan.py          # Lifespan context manager (startup/shutdown hooks)
│  │  ├─ middleware/
│  │  │  ├─ cors.py              # CORS middleware setup
│  │  │  ├─ session.py           # Session middleware setup
│  │  │  └─ docs_guard.py        # Documentation protection middleware
│  │  └─ api/
│  │     ├─ routers.py           # Collects and mounts all routers
│  │     ├─ deps.py              # Dependencies for API routes (db session, auth, container)
│  │     └─ v1/
│  │        ├─ __init__.py
│  │        ├─ endpoints/
│  │        │  ├─ base.py        # Health, root endpoints
│  │        │  ├─ doc.py         # Documentation-related endpoints
│  │        │  └─ message.py     # Message-related endpoints
│  │        └─ schemas.py        # Request/response models for v1
│  │
│  ├─ ui/
│  │  └─ gradio_app.py           # Gradio Blocks UI mounted under /ui
│  │
│  ├─ agent/
│  │  ├─ tools/
│  │  ├─ memory/
│  │  ├─ prompt/                 # Prompt templates & utils
│  │  │  ├─ base_prompt.yaml
│  │  │  ├─ tool_use.yaml
│  │  │  └─ utils.py
│  │  ├─ schemas.py
│  │  └─ runtime.py
│  │
│  ├─ db/
│  │  ├─ database.py             # Database engines, sessions, dependency injection
│  │  ├─ models.py               # SQLAlchemy models
│  │  ├─ crud.py                 # Database operations
│  │  └─ migrations/             # Alembic migration files
│  │     └─ versions/
│  │
│  └─ integrations/
│     └─ openai_client.py        # OpenAI client configuration
│
└─ tests/
   ├─ test_health.py
   └─ test_agent.py
```
