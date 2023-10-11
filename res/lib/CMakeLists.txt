add_library(%project_name%%if:is_header_only% INTERFACE%endif%)
add_library(%project_name%::%project_name% ALIAS %project_name%)

%if:is_linked%
set_target_properties(%project_name% PROPERTIES LINKER_LANGUAGE CXX)
target_set_output_dirs(%project_name%)

function (target_add_sources TGT PREFIX)
    set(srcs ${ARGN})
    list(TRANSFORM srcs PREPEND ${PREFIX})
    target_sources(${TGT} PRIVATE ${srcs})
endfunction ()

target_add_sources(%project_name% "include/%include_dir%/"
    # Header files here
    "export.h"
)

target_add_sources(%project_name% "src/"
    # Source files here (relative to ./src/)
    "dummy.cpp"
)

# find_package(fmt CONFIG REQUIRED)

target_set_options(%project_name% PRIVATE)
target_set_warnings(%project_name% PRIVATE)
target_set_cxx_std(%project_name%)

if (BUILD_SHARED_LIBS)
    target_compile_definitions(%project_name%
        PRIVATE %macro_namespace%_EXPORT_SHARED
        PUBLIC %macro_namespace%_BUILD_SHARED)
endif ()

target_include_directories(%project_name%
PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_link_libraries(%project_name%
PUBLIC
    # fmt::fmt
)
%endif%
%if:is_header_only%
target_include_directories(%project_name%
INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
%endif%

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${PROJECT_BINARY_DIR}/%project_name%ConfigVersion.cmake"
    VERSION ${PACKAGE_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(TARGETS %project_name%
    EXPORT %project_name%Targets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    PUBLIC_HEADER DESTINATION include
)

include(CMakePackageConfigHelpers)
configure_package_config_file(
    "${PROJECT_SOURCE_DIR}/cmake/%project_name%Config.cmake.in"
    "${PROJECT_BINARY_DIR}/%project_name%Config.cmake"
    INSTALL_DESTINATION lib/cmake/%project_name%
)

export(TARGETS %project_name% NAMESPACE %project_name%:: FILE %project_name%Config.cmake)
install(EXPORT %project_name%Targets NAMESPACE %project_name%:: DESTINATION lib/cmake/%project_name%)
install(FILES "${PROJECT_BINARY_DIR}/%project_name%ConfigVersion.cmake"
                "${PROJECT_BINARY_DIR}/%project_name%Config.cmake"
        DESTINATION lib/cmake/%project_name%)
install(DIRECTORY ${PROJECT_SOURCE_DIR}/lib/include/ DESTINATION include)
