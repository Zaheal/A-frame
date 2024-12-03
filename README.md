Если не изменяет память, действия такие (Dockerfile хоть и есть, но он не рабочий):
1. Виртуальное окружение
2. pip install requirements.txt
3. docker-compose up -d
4. alembic upgrade head
5. uvicorn main:app --reload
Вроде всё
