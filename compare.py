#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from subprocess import check_output
import pprint
import json
import ast
import pandokia.helpers.filecomp as filecomp

pp = pprint.PrettyPrinter(indent=2)

PHRASE_APP_FILE = 'en-GB.json'
LOCAL_APP_FILE = 'locale-en.json'

PHRASE_WEB_FILE = 'phraseapp-web.php'
LOCAL_WEB_FILE = 'app.php'

PHRASE_ORDER_FILE = 'phraseapp-ordering.php'
LOCAL_ORDER_FILE = 'orders.php'

ONE_BLOCK_FILE = 'one-block.php'

# phrase_app_key_list = []
# local_file_key_list = []

# phrase_web_key_dict = {}
# local_web_key_dict = {}

def generate_app_key_list(filename, result_list):
    with open(filename) as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i].replace('"', '').strip()
            line = line.split(':')[0].rstrip()
            if line and line != '{' and line != '},' and line != '}' and not any(txt in line for txt in ['one', 'other', 'zero']):
                result_list.append(line)
    f.close()

def app_list_compare():
    generate_app_key_list(PHRASE_APP_FILE, phrase_app_key_list)
    generate_app_key_list(LOCAL_APP_FILE, local_file_key_list)
    # compare two lists
    key_result = []
    value_result = []
    for i in local_file_key_list:
        if i not in phrase_app_key_list:
            key_result.append(i)
    pp.pprint(key_result)

def parse_block(lines):
    result = '{'
    for i in range(0, len(lines)):
        line = lines[i].strip()
        if line and not any(line.startswith(txt) for txt in ['return [', '<?php', '/*', '|', '*/', '//']):
            if '=>' in line:
                if line.endswith('['):
                    result += '\'' + line.split('=>')[0].strip().lstrip('\'').rstrip(',').rstrip('\'') + '\': {'
                else:
                    if 'date' in line:
                        result += '\'' + line.split('=>')[0].strip().lstrip('\'').rstrip(',').rstrip('\'') + '\'' + ': \'' + line.split('=>')[1].split('.')[0].strip().lstrip('\'').rstrip(',').rstrip('\'') + '\', '
                    else:
                        result += '\'' + line.split('=>')[0].strip().lstrip('\'').rstrip(',').rstrip('\'') + '\'' + ': \'' + line.split('=>')[1].strip().lstrip('\'').rstrip(',').rstrip('\'') + '\', '
            elif line.startswith(']'):
                    result += '},'
            else:
                print('what else [' + str(i +1) + ']:\t' + line)

    return result

def generate_local_dict(filename, result):
    with open(filename) as f:
        lines = f.readlines()

    result = ast.literal_eval(parse_block(lines)[:-1])
    # print(type(result))
    # pprint.pprint(result)
    f.close()
    return result

def generate_web_dict(filename, result):
    with open(filename) as f:
        lines = f.readlines()

    new_lines = []
    for i in range(0, len(lines)):
        line = lines[i].strip()
        # replace 'array (' to '['; replace ')' to ']'
        if 'array(' in line:
            line = line.replace('array(', '[')
        if ')' in line:
            line = line.replace(')', ']')
        if ("'") in line:
            line = line.replace("'", "\\\'")

        line = line.replace('\"', '\'')
        new_lines.append(line)
    # print(lines)
    # print('\n\n\n\n\n')
    # print(new_lines)
    result = ast.literal_eval(parse_block(new_lines)[:-1])
    # pprint.pprint(result)
    f.close()
    return result

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    return modified

def web_dict_compare(local_file, phraseapp_file):
    local_web_key_dict = {}
    phrase_web_key_dict = {}
    local_web_key_dict = generate_local_dict(local_file, local_web_key_dict)
    phrase_web_key_dict = generate_web_dict(phraseapp_file, phrase_web_key_dict)
    # compare two dicts, converted to JSON
    dump_local_web_key_dict = json.dumps(local_web_key_dict, sort_keys=True, indent=2)
    dump_phrase_web_key_dict = json.dumps(phrase_web_key_dict, sort_keys=True, indent=2)
    # print(dump_local_web_key_dict)
    # print('\n\n'+'*'*80+'\n\n')
    # print(dump_phrase_web_key_dict)
    pprint.pprint(filecomp.diffjson(dump_local_web_key_dict, dump_phrase_web_key_dict))

# app_list_compare()
# web_dict_compare(LOCAL_WEB_FILE, PHRASE_WEB_FILE)
# web_dict_compare(LOCAL_ORDER_FILE, PHRASE_ORDER_FILE)

def convert_dict_to_string(adict, flatten_str):
    for k, v in adict.items():
        flatten_str += k + '.'
        if isinstance(v, (list,)):
            for i in v:
                if isinstance(i, (dict,)):
                    convert_dict_to_string(i, flatten_str)
        else:
            flatten_str += '\t' + v
    if '\t' in flatten_str:
        print(flatten_str)

def flatten_array(filename):
    result = ''
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines)):
        line = lines[i].strip()
        if line:
            if '=>' in line and line.endswith('['):
                # print(line.split('=>')[0].strip().lstrip('\'').rstrip(',').rstrip('\''))
                result += '{\'' + line.split('=>')[0].strip().lstrip('\'').rstrip(',').rstrip('\'') + '\': ['
            elif line.endswith('],') or line.endswith(']'):
                result += ']},'
            else:
                result += '{\'' + line.split('=>')[0].strip().lstrip('\'').rstrip(',').rstrip('\'') + '\': \'' + line.split('=>')[1].strip().lstrip('\'').rstrip(',').rstrip('\'') + '\'},'
    result = result[:-1]
    result = ast.literal_eval(result)
    # print(result)
    flatten_str = ''
    convert_dict_to_string(result, flatten_str)


flatten_array(ONE_BLOCK_FILE)
