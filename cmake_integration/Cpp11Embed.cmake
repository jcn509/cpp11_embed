function(cpp11_embed_generate_header 
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
        COMMAND Cpp11Embed ${CPP11_EMBED_ARGS}
        COMMENT "Generating header ${OUTPUT_FILE_PATH}"
        DEPENDS "${INPUT_FILE_PATH}"
    )
endfunction()