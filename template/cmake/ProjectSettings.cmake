option(ENABLE_IPO "Enable interprocedural optimization (LTO) for non-debug builds" ON)
option(WARNINGS_AS_ERRORS "Treat compiler warnings as errors" ON)
option(ENABLE_CXX_EXTENSIONS "Enable C++ language extensions" OFF)
option(USE_STATIC_MSVC_RUNTIME "Use -MT(d) instead of -MD(d) for MSVC builds" OFF)

if (ENABLE_IPO)
    include(CheckIPOSupported)
    check_ipo_supported(
        RESULT ipo_supported
        OUTPUT ipo_output)
    if (ipo_supported)
        set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_RELEASE ON)
        set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_RELWITHDEBINFO ON)
        set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_MINSIZEREL ON)
    else ()
        message(WARNING "IPO is not supported: ${ipo_output}")
    endif ()
endif ()

set(CMAKE_CXX_EXTENSIONS ${ENABLE_CXX_EXTENSIONS})

if (USE_STATIC_MSVC_RUNTIME)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
endif ()

function (target_set_warnings TGT ACCESS)
    set(MSVC_WARNINGS
        /W4 # Highest reasonable value
        /w14242 /w14254 /w14263 /w14265 /w14287
        /we4289 /w14296 /w14311 /w14545 /w14546
        /w14547 /w14549 /w14555 /w14619 /w14640
        /w14826 /w14905 /w14906 /w14928)

    set(MSVC_SUPPRESS_EXTERNAL_WARNINGS
        # Ignore warnings from external includes
        /external:W0 /external:anglebrackets /external:templates-)

    set(CLANG_WARNINGS
        -Wall -Wextra -Wpedantic
        -Wnon-virtual-dtor -Wold-style-cast -Wcast-align
        -Wunused -Woverloaded-virtual -Wconversion -Wsign-conversion
        -Wnull-dereference -Wdouble-promotion -Wformat=2)

    if (WARNINGS_AS_ERRORS)
        set(MSVC_WARNINGS ${MSVC_WARNINGS} /WX)
        set(CLANG_WARNINGS ${CLANG_WARNINGS} -Werror)
    endif ()

    set(GCC_WARNINGS
        ${CLANG_WARNINGS}
        -Wmisleading-indentation -Wduplicated-cond
        -Wduplicated-branches -Wlogical-op)

    if (MSVC) # MSVC-like
        if (CMAKE_CXX_COMPILER_ID STREQUAL "Clang") # clang-cl
            target_compile_options(${TGT} ${ACCESS} ${MSVC_WARNINGS})
        else () # Real MSVC
            target_compile_options(${TGT} ${ACCESS} ${MSVC_WARNINGS} ${MSVC_SUPPRESS_EXTERNAL_WARNINGS})
        endif ()
    elseif (CMAKE_CXX_COMPILER_ID STREQUAL "Clang") # clang
        target_compile_options(${TGT} ${ACCESS} ${CLANG_WARNINGS})
    elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU") # gcc
        target_compile_options(${TGT} ${ACCESS} ${GCC_WARNINGS})
    else ()
        message(AUTHOR_WARNING "No compiler warnings set for '${CMAKE_CXX_COMPILER_ID}' compiler.")
    endif ()
endfunction ()

function (target_set_options TGT ACCESS)
    # Asio requires _WIN32_WINNT to be set; target Windows 10 or later
    if (WIN32)
        string(TOUPPER ${ACCESS} ACCESS)
        if (ACCESS STREQUAL "INTERFACE")
            target_compile_definitions(${TGT} INTERFACE _WIN32_WINNT=0x0A00)
        else ()
            target_compile_definitions(${TGT} PUBLIC _WIN32_WINNT=0x0A00)
        endif ()
    endif ()

    if (MSVC) # Visual Studio
        if (NOT CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
            target_compile_options(${TGT} ${ACCESS}
                /utf-8
                /permissive- /Zc:__cplusplus /Zc:externConstexpr /Zc:preprocessor # Conformance settings
            )
        endif ()
    elseif (CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        target_compile_options(${TGT} ${ACCESS}
            -stdlib=libc++
            -fcolor-diagnostics
            -ftemplate-backtrace-limit=32
            -fvisibility=hidden)
        target_link_options(${TGT} ${ACCESS} -stdlib=libc++)
    elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
        target_compile_options(${TGT}
            ${ACCESS}
            -fdiagnostics-color=always
            -fconcepts-diagnostics-depth=16
            -ftemplate-backtrace-limit=32
            -fvisibility=hidden)
    endif ()
endfunction ()

function (target_set_output_dirs TGT)
    set_target_properties(${TGT} PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/out"
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/out"
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/out"
        VS_DEBUGGER_WORKING_DIRECTORY "$<TARGET_FILE_DIR:${TGT}>"
        VS_DEBUGGER_COMMAND "$<TARGET_FILE:${TGT}>"
    )
endfunction ()

function (target_set_cxx_std TGT)
    # PUBLIC so that consumers of a library also get the required standard
    target_compile_features(${TGT} PUBLIC cxx_std_20)
endfunction ()

function (target_config TGT)
    target_set_warnings(${TGT} PRIVATE)
    target_set_options(${TGT} PRIVATE)
    target_set_output_dirs(${TGT})
    target_set_cxx_std(${TGT})
endfunction ()
