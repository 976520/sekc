cmake_minimum_required(VERSION 3.10)
project(sekc_runner)

set(CMAKE_CXX_STANDARD 17)

include_directories(../runtime)

add_executable(sekc_runner main.cpp)
