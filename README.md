# Task Manager

Простой менеджер задач на **FastAPI** с асинхронным SQLAlchemy и PostgreSQL.  

---

# Код
[SQLAlchemy ORM модели](https://github.com/BykovskiiEgor/test_task_manager/blob/main/src/task_manager/adapters/models/task_model.py)  
[Репозиторий для работы с БД](https://github.com/BykovskiiEgor/test_task_manager/blob/main/src/task_manager/adapters/repository/task_repository.py)  
[Бизнес-логика для задач](https://github.com/BykovskiiEgor/test_task_manager/blob/main/src/task_manager/applications/use_cases/task_crud.py)  
[FastAPI роутеры](https://github.com/BykovskiiEgor/test_task_manager/blob/main/src/task_manager/adapters/fapi/tasks/routers.py)  


---

# Запуск через Docker
Для запуска приложения и базы данных используйте `docker-compose`:

```
docker-compose up -d
```

---

# Использование
Отправить запрос можно через [Swagger UI](http://localhost:8000/docs)

---
