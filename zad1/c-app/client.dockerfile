FROM gcc:latest
COPY . /client/
WORKDIR /client/
RUN gcc -o client client.c
