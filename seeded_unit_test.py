import unittest
from sanitize_json_config import sanitize_json_config

class TestSanitizeJsonConfig(unittest.TestCase):
    def test_example1(self):
        config = '{ "name": "Alice", "age": 30, }'
        expected = '{"name":"Alice","age":30}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_example2(self):
        config = '/* initial config */\n{ "values": [1, 2, 3, ],\n  "nested": {"x": 1, }, }'
        expected = '{"values":[1,2,3],"nested":{"x":1}}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_example3(self):
        config = '{"empty": [], "obj": {}}'
        expected = '{"empty":[],"obj":{}}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_minimal_object(self):
        config = '   {   }   '
        expected = '{}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_minimal_array(self):
        config = ' [ ] '
        expected = '[]'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_nested_trailing_commas(self):
        config = '''
            {
                "level1": {
                    "level2": [10,20,30,],
                    "emptyObj": {},
                },
                "arr": [{},],
            }
        '''
        expected = '{"level1":{"level2":[10,20,30],"emptyObj":{}},"arr":[{}]}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_complex_nested_structure(self):
        config = '''
        /* Header comment */
        {
            "arr" : [ /* inline comment */ 5 , 6 , /*c*/ ],
            "obj" : {
                "k1" : 100, /* trailing */
                "k2" : [ ], 
            }, // end obj
        }
        '''
        expected = '{"arr":[5,6],"obj":{"k1":100,"k2":[]}}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_whitespace_in_strings_preserved(self):
        config = '{ "text": "  leading and trailing  ", "x":1, }'
        expected = '{"text":"  leading and trailing  ","x":1}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_tabs_and_newlines_outside_strings(self):
        config = '\t{\n\t"name"\t:\t"Alice"\n,\n\t"age"\n:\n30\t}\n'
        expected = '{"name":"Alice","age":30}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_no_modifications_needed(self):
        config = '{"a":1,"b":[2,3],"c":{"d":4}}'
        expected = '{"a":1,"b":[2,3],"c":{"d":4}}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_punctuation_in_keys(self):
        config = '{ "a,b:c": 1, "d:e,f":2, }'
        expected = '{"a,b:c":1,"d:e,f":2}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_comments_and_trailing_commas_mixed(self):
        config = '{"a":1 /* comment */ , "b":2, }'
        expected = '{"a":1,"b":2}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_block_comments_surround_json(self):
        config = '/* header */{"a":1,}/* footer */'
        expected = '{"a":1}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_string_value_with_comma(self):
        config = '{ "a": "abc,", "b":2, }'
        expected = '{"a":"abc,","b":2}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_large_numbers(self):
        config = '{ "zero": 0, "big": 1234567890, }'
        expected = '{"zero":0,"big":1234567890}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_adjacent_block_comments(self):
        config = '/*c1*//*c2*/{"a":1,}'
        expected = '{"a":1}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_single_line_comments_within_json(self):
        config = '{ "a":1, // comment here\n "b":2, }'
        expected = '{"a":1,"b":2}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_nested_arrays_deep(self):
        config = '[[[1,2,],],]'
        expected = '[[[1,2]]]'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_string_with_braces_and_commas(self):
        config = '{ "s": "{}[,]", }'
        expected = '{"s":"{}[,]"}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_crlf_line_endings(self):
        config = '/*comment*/{\r\n"a":1,\r\n"b":[2,3,],\r\n}\r\n'
        expected = '{"a":1,"b":[2,3]}'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_top_level_array(self):
        config = '[1,2,3,]'
        expected = '[1,2,3]'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_string_with_internal_curly_and_brackets(self):
        config = '{ "msg": "{[()]}", }'
        expected = '{"msg":"{[()]}" }'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_mixed_whitespace_and_comments(self):
        config = '  /*c*/ [ \n 10 , /*x*/ 20 , ] // end\n'
        expected = '[10,20]'
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_unclosed_brace(self):
        config = '{"a":1'
        expected = ''
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_unclosed_multiline_comment(self):
        config = '/* comment'
        expected = ''
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

    def test_invalid_key_token(self):
        config = '{a:1}'
        expected = ''
        result = sanitize_json_config(config)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
