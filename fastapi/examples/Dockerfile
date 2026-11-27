FROM python:3.15.2-slim
WORKDIR /app
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY . .
RUN useradd --uid 10001 --create-home relay && mkdir -p /app/.runtime && chown relay:relay /app/.runtime
USER relay
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
