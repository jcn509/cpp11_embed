find_package (Python COMPONENTS Interpreter)
# TODO: what to do if Python is not found?

add_custom_target(
    InstallPythonDependencies
    COMMAND ${Python_EXECUTABLE} -m pipenv sync --verbose
    COMMENT "Installing Python dependencies"
    SOURCES
        ${CMAKE_CURRENT_LIST_DIR}/Pipfile.lock
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
)

# TODO: write some CMake function like what catch2 has to register each
# test independently
# TODO: need the executable to be built before this can be run
add_test (NAME "End To End Tests"
  COMMAND ${Python_EXECUTABLE} -m pipenv run pytest tests --cpp11-embed-path $<TARGET_FILE:Cpp11Embed> -vv
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
)