# Allow spaces and special characters in test names.
cmake_policy(SET CMP0110 NEW)

add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/libs/catch2)
include(${CMAKE_CURRENT_LIST_DIR}/libs/catch2/contrib/Catch.cmake)

# Order determines what order tests run
add_subdirectory(unit_tests)
add_subdirectory(end_to_end_tests)
add_subdirectory(self_tests)
