import re
import json

def sanitize_json_config(config):
    if not isinstance(config, str):
        return ""

    try:
        # Step 1: Remove block comments (/* ... */)
        config = re.sub(r'/\*.*?\*/', '', config, flags=re.DOTALL)

        # Step 2: Remove line comments (//...)
        config = re.sub(r'//.*', '', config)

        # Step 3: Protect string literals
        string_regex = r'"(\\.|[^"\\])*"'
        string_literals = []
        def _extract_string(match):
            string_literals.append(match.group())
            return f'__STRING{len(string_literals)-1}__'
        
        config = re.sub(string_regex, _extract_string, config)

        # Step 4: Remove trailing commas before } or ]
        config = re.sub(r',\s*(?=[}\]])', '', config)

        # Step 5: Remove all whitespace
        config = re.sub(r'\s+', '', config)

        # Step 6: Restore strings
        for i, s in enumerate(string_literals):
            config = config.replace(f'__STRING{i}__', s)

        # Step 7: Validate
        json.loads(config)
        return config

    except:
        return ""
