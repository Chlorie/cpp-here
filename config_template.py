from typing import Union, Dict
import re


ConfigVars = Dict[str, Union[str, bool]]


_cond_pattern = re.compile(r"%if:(\w*)%\r?\n?([^%]*)%endif%\r?\n?")
_var_pattern = re.compile(r"%((?!endif)\w*)%")


def config_template(template: str, config_vars: ConfigVars) -> str:
    def replace_conditional(match: re.Match[str]) -> str:
        var = match.group(1).strip()
        content = match.group(2)
        if var in config_vars and config_vars[var] == True:
            return content
        return ""
    
    def replace_var(match: re.Match[str]) -> str:
        full_var = match.group(1)
        var = full_var.strip()
        if var in config_vars and isinstance(value := config_vars[var], str):
            return value
        else:
            return ""
    
    curr = template
    while True:
        prev = curr
        curr = re.sub(_cond_pattern, replace_conditional, curr)
        if curr != prev:
            continue
        curr = re.sub(_var_pattern, replace_var, curr)
        if curr != prev:
            continue
        return curr
