add_subdirectory(libs/catch2)

add_executable(Cpp11EmbedTests
    Main.cpp
    LibTests.cpp    
)

#target_include_directories(Cpp11EmbedTests SYSTEM PRIVATE
#    ${CMAKE_CURRENT_LIST_DIR}/libs/catch2/single_include)

target_link_libraries(Cpp11EmbedTests PRIVATE
    Cpp11EmbedLib
    Catch2::Catch2
)

include(CTest)
include(${CMAKE_CURRENT_LIST_DIR}/libs/catch2/contrib/Catch.cmake)
catch_discover_tests(Cpp11EmbedTests)