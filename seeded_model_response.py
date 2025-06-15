import re

def sanitize_json_config(config):
    try:
        # Remove single-line comments
        config = re.sub(r'//.*', '', config)
        
        # Remove multi-line comments (including adjacent ones)
        config = re.sub(r'/\*.*?\*/', '', config, flags=re.DOTALL)
        
        # Remove trailing commas
        config = re.sub(r',\s*([}\]])', r'\1', config)
        
        # Remove unnecessary whitespace outside strings
        # First preserve strings
        string_matches = list(re.finditer(r'"[^"]*"', config))
        # Remove all whitespace
        config = re.sub(r'\s+', '', config)
        # Restore strings with their original content
        for match in reversed(string_matches):
            start, end = match.span()
            original_string = match.group(0)
            config = config[:start] + original_string + config[end:]
        
        # Try to parse the JSON to validate it
        import json
        json.loads(config)
        
        return config
    except:
        return ""

