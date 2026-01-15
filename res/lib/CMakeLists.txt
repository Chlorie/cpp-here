add_library(%project_name%%if:is_header_only% INTERFACE%endif%)
add_library(%project_name%::%project_name% ALIAS %project_name%)

%if:is_linked%
set_target_properties(%project_name% PROPERTIES
    LINKER_LANGUAGE CXX
    SOVERSION ${PROJECT_VERSION_MAJOR}
	VERSION ${PROJECT_VERSION}
)
target_config(%project_name%)

if (BUILD_SHARED_LIBS)
    target_compile_definitions(%project_name%
        PRIVATE %macro_namespace%_EXPORT_SHARED
        PUBLIC %macro_namespace%_BUILD_SHARED
    )
endif ()

target_public_headers(%project_name% "${CMAKE_CURRENT_SOURCE_DIR}/include" "include/%include_dir%"
    # Header files here
    "export.h"
)

target_implementations(%project_name% "src"
    # Source files here (relative to ./src)
    "dummy.cpp"
)

# find_package(fmt CONFIG REQUIRED)

target_link_libraries(%project_name%
PUBLIC
    # fmt::fmt
)
%endif%
%if:is_header_only%
target_public_headers(%project_name% "${CMAKE_CURRENT_SOURCE_DIR}/include" "include/%include_dir%"
    # Header files here
    "export.h"
)
%endif%

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${PROJECT_BINARY_DIR}/%project_name%ConfigVersion.cmake"
    VERSION ${PACKAGE_VERSION}
    COMPATIBILITY SameMajorVersion
)

include(GNUInstallDirs)
set(%upper_project_name%_INSTALL_CMAKEDIR
    ${CMAKE_INSTALL_LIBDIR}/cmake/%project_name%
    CACHE STRING "Path to %project_title% cmake files"
)

install(TARGETS %project_name%
    EXPORT %project_name%Targets
    LIBRARY
        DESTINATION ${CMAKE_INSTALL_LIBDIR}
        COMPONENT Runtime
        NAMELINK_COMPONENT Development
    ARCHIVE
        DESTINATION ${CMAKE_INSTALL_LIBDIR}
        COMPONENT Development
    RUNTIME
        DESTINATION ${CMAKE_INSTALL_BINDIR}
        COMPONENT Runtime
    FILE_SET HEADERS
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        COMPONENT Development
    FILE_SET CXX_MODULES
        DESTINATION ${%upper_project_name%_INSTALL_CMAKEDIR}
        COMPONENT Development
)

include(CMakePackageConfigHelpers)
configure_package_config_file(
    "${PROJECT_SOURCE_DIR}/cmake/%project_name%Config.cmake.in"
    "${PROJECT_BINARY_DIR}/%project_name%Config.cmake"
    INSTALL_DESTINATION ${%upper_project_name%_INSTALL_CMAKEDIR}
)

export(TARGETS %project_name% NAMESPACE %project_name%:: FILE %project_name%Config.cmake)
install(EXPORT %project_name%Targets
    NAMESPACE %project_name%::
    DESTINATION ${%upper_project_name%_INSTALL_CMAKEDIR}
)
install(
    FILES
        "${PROJECT_BINARY_DIR}/%project_name%ConfigVersion.cmake"
        "${PROJECT_BINARY_DIR}/%project_name%Config.cmake"
        DESTINATION ${%upper_project_name%_INSTALL_CMAKEDIR}
)
