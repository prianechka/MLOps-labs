FROM rust:1.57.0-slim-bullseye
FROM python:3.12.8-slim-bullseye

WORKDIR /webapp

COPY . .

RUN mv ./heart_diseases_detector/model.pkl /opt/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["heart_diseases_detector/__init__.py"]