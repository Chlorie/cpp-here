from typing import Union, Dict, Tuple
import re


ConfigVars = Dict[str, Union[str, bool]]


_cond_pattern = re.compile(r"%if:(\w*)%([^%]*)%endif%")
_var_pattern = re.compile(r"%((?!endif)\w*)%")


def config_template(template: str, config_vars: ConfigVars) -> str:
    def replace_conditional(match: re.Match[str]) -> str:
        var = match.group(1).strip()
        content = match.group(2).strip("\r\n")
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
    
    while True:
        sub = re.sub(_cond_pattern, replace_conditional, template)
        sub = re.sub(_var_pattern, replace_var, sub)
        if sub == template:
            return sub
        template = sub
