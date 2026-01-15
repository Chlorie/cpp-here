cmake_minimum_required(VERSION 3.25)

project(%project_name% LANGUAGES CXX VERSION %version%)

set(CMAKE_SCRIPTS "${PROJECT_SOURCE_DIR}/cmake")
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_SCRIPTS})
set_property(GLOBAL PROPERTY USE_FOLDERS ON)
include("cmake/ProjectSettings.cmake")
include("cmake/TargetSourceExtensions.cmake")

%if:is_lib%
option(BUILD_SHARED_LIBS "Build library as shared library" OFF)

add_subdirectory(lib)

option(%upper_project_name%_BUILD_EXAMPLES "Build code examples" ON)
if (%upper_project_name%_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif ()

%endif%
%if:is_app%
add_subdirectory(src)

%endif%
%if:test_enabled%
option(%upper_project_name%_BUILD_TESTS "Build unit tests" OFF)
if (%upper_project_name%_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif ()

%endif%