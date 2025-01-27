FROM python:3.13.1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# CMD ["gunicorn","--bind","0.0.0.0:80","app:create_app()"]
CMD ["/bin/bash","docker-entrypoint.sh"]