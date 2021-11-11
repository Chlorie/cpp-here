function (add_example TGT)
    add_executable(${TGT} "${TGT}.cpp")
    target_set_output_dirs(${TGT})
    target_link_libraries(${TGT} PRIVATE project_options %project_name%::%project_name%)
    target_set_cxx20(${TGT})
endfunction ()

add_example(playground)
