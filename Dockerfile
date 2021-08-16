FROM python:3
ENV PYTHONBUFFERED=1
RUN apt-get update && apt-get install -y zsh tig peco

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN chsh -s /bin/zsh

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
