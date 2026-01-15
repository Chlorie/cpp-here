function (_prepend_paths PATHS PARENT)
    string(REGEX REPLACE "/$" "" PARENT "${PARENT}")
	list(TRANSFORM ${PATHS} PREPEND "${PARENT}/")
    return(PROPAGATE ${PATHS})
endfunction ()

function (target_public_headers TGT BASE_DIR PARENT)
    set(srcs ${ARGN})
    _prepend_paths(srcs ${PARENT})
    target_sources(${TGT}
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${BASE_DIR}
        FILES ${srcs}
    )
endfunction ()

function (target_private_headers TGT BASE_DIR PARENT)
    set(srcs ${ARGN})
    _prepend_paths(srcs ${PARENT})
    target_sources(${TGT}
    PRIVATE
        FILE_SET private_headers TYPE HEADERS
        BASE_DIRS ${BASE_DIR}
        FILES ${srcs}
    )
endfunction ()

function (target_public_modules TGT BASE_DIR PARENT)
    set(srcs ${ARGN})
    _prepend_paths(srcs ${PARENT})
    target_sources(${TGT} PUBLIC
        FILE_SET CXX_MODULES
        BASE_DIRS ${BASE_DIR}
        FILES ${srcs}
    )
endfunction ()

function (target_private_modules TGT PARENT)
    set(srcs ${ARGN})
    _prepend_paths(srcs ${PARENT})
    target_sources(${TGT} PRIVATE
        FILE_SET private_modules TYPE CXX_MODULES
        FILES ${srcs}
    )
endfunction ()

function (target_implementations TGT PARENT)
    set(srcs ${ARGN})
    _prepend_paths(srcs ${PARENT})
    target_sources(${TGT} PRIVATE ${srcs})
endfunction ()
