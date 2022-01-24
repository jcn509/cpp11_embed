# This tool should generate header files compatible with C++11
# regardless of what version of C++ it happens to be written in
set(CMAKE_CXX_STANDARD 11)

# Must be set before including Cpp11Embed.cmake.
# As we are building Cpp11Embed as part of this project
# we can set it to the target name.
# (Which should also ensure that cmake automatically adds
# it as a dependency as its used in add_custom_command.).
# If you are not building it as part of your project but
# instead you have the binary saved somewhere then set 
# CPP11_EMBED_EXECUTABLE_PATH to the full path to the binary
set(CPP11_EMBED_EXECUTABLE_PATH Cpp11Embed)
include("${CMAKE_CURRENT_LIST_DIR}/../../cmake_integration/Cpp11Embed.cmake")

# Add a target we can link against. Linking against this target
# will ensure that all the headers are generated and add them
# to the include path.
# You can define multiple targets each associated with different
# sets of headers.
add_cpp11_embed_target(Cpp11EmbedSelfTestsGeneratedHeaders)

set(TEST_FILES_DIR "${CMAKE_CURRENT_LIST_DIR}/../test_files")
cpp11_embed_generate_header(
    Cpp11EmbedSelfTestsGeneratedHeaders
    "${TEST_FILES_DIR}/two_lines.txt"
    "k_text_header"
    "TextHeader.h"
)

cpp11_embed_generate_header(
    Cpp11EmbedSelfTestsGeneratedHeaders
    "${TEST_FILES_DIR}/two_lines.txt"
    "k_text_header_with_header_guard"
    "TextHeaderWithHeaderGuard.h"
    USE_HEADER_GUARD TRUE
)

cpp11_embed_generate_header(
    Cpp11EmbedSelfTestsGeneratedHeaders
    "${TEST_FILES_DIR}/two_lines.txt"
    "k_binary_header"
    "BinaryHeader.h"
    BINARY_MODE TRUE
)

cpp11_embed_generate_header(
    Cpp11EmbedSelfTestsGeneratedHeaders
    "${TEST_FILES_DIR}/two_lines.txt"
    "k_binary_header_with_header_guard"
    "BinaryHeaderWithHeaderGuard.h"
    BINARY_MODE TRUE
    USE_HEADER_GUARD TRUE
)

cpp11_embed_generate_header(
    Cpp11EmbedSelfTestsGeneratedHeaders
    "${TEST_FILES_DIR}/one_line.txt"
    "k_text_header_in_a_subdirectory"
    "InASubDirectory/TextHeader2.h"
)

add_executable(Cpp11EmbedSelfTests
    Main.cpp
    SelfTests.cpp
)

target_link_libraries(Cpp11EmbedSelfTests PRIVATE
    Cpp11EmbedLib
    Catch2::Catch2
    # Make sure all the auto-generated headers get generated
    # before this target is built and that we can include them
    Cpp11EmbedSelfTestsGeneratedHeaders
)

catch_discover_tests(
    Cpp11EmbedSelfTests
    TEST_PREFIX "Self Test: "
)
