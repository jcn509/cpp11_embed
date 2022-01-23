add_executable(Cpp11EmbedUnitTests
    Main.cpp
    LibTests.cpp    
)

target_link_libraries(Cpp11EmbedUnitTests PRIVATE
    Cpp11EmbedLib
    Catch2::Catch2
)

catch_discover_tests(
    Cpp11EmbedUnitTests
    TEST_PREFIX "Unit Test: ")
