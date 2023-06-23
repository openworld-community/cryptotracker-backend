FROM archlinux:latest

RUN pacman -Syu python
RUN mkdir -f /app
COPY . /app
WORKDIR /app/app
RUN python -m ensurepip --upgrade
RUN python -m pip install -r requirements.txt
CMD ["uvicorn" "main:app" "--reload"]
