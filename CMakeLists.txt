cmake_minimum_required(VERSION 3.0)
project(Cpp11Embed)

set(CMAKE_CXX_STANDARD 14)

if(MSVC)
  add_compile_options(/W4 /WX)
else()
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

add_library(Cpp11EmbedLib STATIC ${CMAKE_CURRENT_LIST_DIR}/src/Lib.cpp)
target_include_directories(Cpp11EmbedLib PUBLIC ${CMAKE_CURRENT_LIST_DIR}/src)

add_executable(Cpp11Embed
    ${CMAKE_CURRENT_LIST_DIR}/src/Main.cpp
)

target_link_libraries(Cpp11Embed PRIVATE Cpp11EmbedLib)
