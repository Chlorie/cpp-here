cmake_minimum_required(VERSION 3.14)

project(%project_name% LANGUAGES CXX VERSION %version%)

set(CMAKE_SCRIPTS "${PROJECT_SOURCE_DIR}/cmake")
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_SCRIPTS})

add_library(project_options INTERFACE)
include("cmake/ProjectSettings.cmake")
target_set_warnings(project_options INTERFACE)
target_set_options(project_options INTERFACE)

add_subdirectory(src)
