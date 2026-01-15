function (add_example TGT)
    add_executable(${TGT} "${TGT}.cpp")
    set_target_properties(${TGT} PROPERTIES FOLDER examples)
    target_config(${TGT})
    target_link_libraries(${TGT} PRIVATE %project_name%::%project_name%)
endfunction ()

add_example(playground)
