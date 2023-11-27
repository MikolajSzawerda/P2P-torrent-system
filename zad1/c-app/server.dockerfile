FROM gcc:latest
COPY . /server/
WORKDIR /server/
RUN gcc -o server server.c
CMD ["./server", "8888"]