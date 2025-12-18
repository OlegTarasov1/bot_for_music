init_user:
	sh /app/raw/init_user.sh "test_user" "test_password"

makemigrations:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

start-app:
	make makemigrations && make migrate && python3 main.py
