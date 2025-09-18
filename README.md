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

### 🔑 Key Changes for Scalability

* **`app/init_settings.py`** → encapsulates argument parsing and environment mode detection, exposing `global_settings`.
* **`app/lifespan.py`** → holds database initialization and seed logic in a single place using `@asynccontextmanager`.
* **`app/middleware.py`** → sets up CORS, session middleware, and doc-protect middleware in composable functions.
* **`app/routers.py`** → centralizes `include_router` calls to keep `main.py` clean.
* **`app/config.py`** → defines `Settings`, `DevSettings`, `ProdSettings` with computed `DB_URL`, `ASYNC_DB_URL`, and `API_BASE_URL`.
* **`api/v1` modules** → each concern has its own file (base, doc, message) for better separation.

This structure:

* Keeps `main.py` minimal (only FastAPI creation + `setup_routers`, `setup_cors`, `setup_session`, `add_doc_protect`, and lifespan import).
* Allows adding new API versions (`v2/`) without touching core logic.
* Makes middlewares and settings reusable for tests and CLI scripts.

---

Would you like me to generate **starter code templates** for `main.py`, `routers.py`, `middleware.py`, and `lifespan.py` so you can plug them in immediately?

---

## 🧱 Refined FastAPI `app/` & `api/` Structure

> Goal: make **settings**, **lifespan**, **middleware**, and **routers** first‑class, versionable modules with clean imports. Keep runtime‑agnostic code (agent, db, integrations) separate from web concerns.

```
src/
├─ app/
│  ├─ main.py                      # App entrypoint (creates FastAPI, mounts UI, includes routers)
│  ├─ core/
│  │  ├─ config.py                 # pydantic-settings (Dev/Prod) and get_settings()
│  │  ├─ init_settings.py          # CLI arg parsing, global_settings resolution
│  │  └─ logging.py                # structured logging config (uvicorn/stdlog)
│  ├─ lifecycle/
│  │  └─ lifespan.py               # @asynccontextmanager lifespan() (init DB, seed, warm caches)
│  ├─ middleware/
│  │  ├─ cors.py                   # setup_cors(app)
│  │  ├─ session.py                # setup_session(app)
│  │  └─ docs_guard.py             # add_doc_protect(app) + doc_protect_middleware
│  ├─ api/
│  │  ├─ routers.py                # setup_routers(app) — central include_router registry
│  │  ├─ deps.py                   # shared FastAPI dependencies (db session, clients)
│  │  └─ v1/
│  │     ├─ __init__.py
│  │     ├─ endpoints/
│  │     │  ├─ base.py             # health, root
│  │     │  ├─ doc.py              # doc/login helpers if any
│  │     │  └─ message.py          # /api/v1/message endpoints
│  │     └─ schemas.py             # request/response models for v1
│  └─ utils/
│     └─ responses.py              # common response helpers (errors/envelopes)
├─ api/                            # (optional) thin re-export facade if you want app-only imports
│  └─ __init__.py
```

### 🔗 Import Map (consistent and IDE‑friendly)

* **Routers registry**

  ```python
  # src/app/api/routers.py
  from fastapi import FastAPI
  from app.api.v1.endpoints import base, doc, message

  def setup_routers(app: FastAPI) -> None:
      app.include_router(base.router, prefix="", tags=["main"])
      app.include_router(doc.router, prefix="", tags=["doc"])
      app.include_router(message.router, prefix="/api/v1", tags=["message"])
  ```

* **Middleware modules** (single-responsibility per file)

  ```python
  # src/app/middleware/cors.py
  from fastapi.middleware.cors import CORSMiddleware
  from app.core.init_settings import global_settings

  def setup_cors(app):
      origins = [
          global_settings.API_BASE_URL,
          "http://localhost",
          "http://localhost:5000",
      ]
      app.add_middleware(
          CORSMiddleware,
          allow_origins=origins,
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
      )
  ```

  ```python
  # src/app/middleware/session.py
  from starlette.middleware.sessions import SessionMiddleware

  def setup_session(app):
      app.add_middleware(SessionMiddleware, secret_key="change_me", max_age=1800)
  ```

  ```python
  # src/app/middleware/docs_guard.py
  from fastapi import Request
  from fastapi.responses import RedirectResponse

  async def doc_protect_middleware(request: Request, call_next):
      if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
          if not request.session.get("authenticated"):
              return RedirectResponse(url="/login")
      return await call_next(request)

  def add_doc_protect(app):
      app.middleware("http")(doc_protect_middleware)
  ```

* **Lifespan** (DB init + seed)

  ```python
  # src/app/lifecycle/lifespan.py
  from contextlib import asynccontextmanager
  from fastapi import FastAPI
  from db.base import init_db, AsyncSessionLocal
  from db.seeds import models_data
  from db.crud import create_message_dict_async

  @asynccontextmanager
  async def lifespan(app: FastAPI):
      init_db()
      async with AsyncSessionLocal() as db:
          try:
              for raw in models_data:
                  await create_message_dict_async(db, raw)
          finally:
              await db.close()
      yield
  ```

* **Settings split** (config + initializer)

  ```python
  # src/app/core/config.py
  # (pydantic-settings: Settings, DevSettings, ProdSettings, get_settings)
  ```

  ```python
  # src/app/core/init_settings.py
  # (argparse + pytest-aware defaults). Exposes: global_settings
  ```

* **App entry** wires all pieces without circular imports:

  ```python
  # src/app/main.py
  from fastapi import FastAPI
  from app.lifecycle.lifespan import lifespan
  from app.api.routers import setup_routers
  from app.middleware.cors import setup_cors
  from app.middleware.session import setup_session
  from app.middleware.docs_guard import add_doc_protect

  app = FastAPI(lifespan=lifespan)
  setup_cors(app)
  setup_session(app)
  add_doc_protect(app)
  setup_routers(app)
  ```

### 🧭 Design Notes

* **Single responsibility modules** → clearer diffs, easier testing.
* **Flat, predictable import roots** (`app.*`, not `backend.fastapi.*`).
* **Versioned API** lives under `app/api/vX/` to scale.
* **No circulars**: settings are read only in `app/core/*` and referenced elsewhere.
* **Replaceable auth**: docs guard stays a separate middleware.
