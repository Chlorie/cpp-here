add_executable(%project_name%)

target_sources(%project_name% PRIVATE
    "main.cpp"
)

target_config(%project_name%)

# find_package(fmt CONFIG REQUIRED)

target_link_libraries(%project_name% PRIVATE
    # fmt::fmt
)
