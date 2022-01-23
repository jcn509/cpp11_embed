
# You probably don't want to use this and instead
# you should use cpp11_embed_generate_header.
# This function is very generic but requires some
# extra work to be done for you to be able to use
# the headers you generate and ensure that they
# get built. See cpp11_embed_generate_header for
# details.
# Note: you must add the generated header
# to the source of some target to ensure that it
# actually gets generated (see 
# cpp11_embed_generate_header for an example)
function(cpp11_embed_generate_header_no_target
    INPUT_FILE_PATH
    IDENTIFIER_NAME
    OUTPUT_FILE_PATH
)
    cmake_parse_arguments(
        ""
        ""
        "BINARY_MODE;USE_HEADER_GUARD"
        ""
        ${ARGN}
    )

    list(APPEND CPP11_EMBED_ARGS "${INPUT_FILE_PATH}" "${IDENTIFIER_NAME}" -o "${OUTPUT_FILE_PATH}")
    if(_BINARY_MODE)
        list(APPEND CPP11_EMBED_ARGS "-b")
    endif()
    if(_USE_HEADER_GUARD)
        list(APPEND CPP11_EMBED_ARGS "-g")
    endif()
    add_custom_command(
        PRE_BUILD
        OUTPUT "${OUTPUT_FILE_PATH}"
        COMMAND "${CPP11_EMBED_EXECUTABLE_PATH}" ${CPP11_EMBED_ARGS}
        COMMENT "Generating header ${OUTPUT_FILE_PATH}"
        DEPENDS "${INPUT_FILE_PATH}"
    )
endfunction()