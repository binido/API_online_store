# 📦 API Интернет-магазина

## 🚀 Быстрый старт

### 1️⃣ Создайте файл `.env` на основе `.env.example`

```bash
cp .env.example .env
```

🔎 Пример содержимого:

```
DB_HOST=db
DB_PORT=5432
DB_NAME=shop_db
DB_USER=postgres
DB_PASS=postgres

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### 2️⃣ Сборка и запуск проекта через Docker Compose

```bash
docker compose up --build
```

---

### 3️⃣ Доступ к приложению:

* 📜 **Swagger (документация):** [http://localhost:8000/docs](http://localhost:8000/docs)
* 📂 **OpenAPI JSON:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 🔐 Авторизация

1. Получите **токен** через эндпоинт `POST /auth/login`.
2. В Swagger (верхний правый угол) нажмите **`Authorize`** и вставьте токен.
3. Swagger автоматически добавит токен ко всем запросам, требующим авторизации.

---

## ⚙️ Стек технологий

* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy (async)**
* **Alembic** (migration)
* **Docker / Docker Compose**
* **Pydantic**
* **JWT** для авторизации

---

## 🛠️ Команды для разработки

* Применение миграций:

```bash
docker compose exec app alembic upgrade head
```

* Остановка контейнеров:

```bash
docker compose down
```
