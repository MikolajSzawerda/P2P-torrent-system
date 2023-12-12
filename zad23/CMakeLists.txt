cmake_minimum_required(VERSION 3.26)
project(lab_repo C)


set(CMAKE_C_STANDARD 17)

add_executable(server server.c)

add_executable(client client.c)
