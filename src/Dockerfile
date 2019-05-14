FROM alpine

ENV FLASK_APP=service.py

RUN mkdir /usr/local/service; 

WORKDIR /usr/local/service

COPY service.py .

RUN apk add python3; \
    python3 -m pip install Flask;

# expose the flask http port
EXPOSE 5000/tcp

CMD ["flask", "run", "--host=0.0.0.0"]