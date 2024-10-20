# Используем официальный образ Python в качестве базового
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (или только нужные файлы) в рабочую директорию контейнера
COPY . .

# Указываем команду для запуска приложения
# Для Flask:
# CMD ["flask", "run", "--host=0.0.0.0"]
# Для FastAPI с uvicorn:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Указываем, на каком порту будет слушать приложение
EXPOSE 8000
