#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from subprocess import check_output
import pprint
import json
import ast

pp = pprint.PrettyPrinter(indent=2)

PHRASE_APP_FILE = 'en-GB.json'
LOCAL_APP_FILE = 'locale-en.json'

PHRASE_WEB_FILE = 'phraseapp-web.php'
LOCAL_WEB_FILE = 'app.php'

phrase_app_key_list = []
local_file_key_list = []

phrase_web_key_list = []
local_web_key_list = []

def generate_app_key_list(filename, result_list):
    with open(filename) as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i].replace('"', '').strip()
            line = line.split(':')[0].rstrip()
            if line and line != '{' and line != '},' and line != '}' and not any(txt in line for txt in ['one', 'other', 'zero']):
                result_list.append(line)
    f.close()

def app_compare():
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

def generate_web_dict(filename):
    result = {}
    with open(filename) as f:
        lines = f.readlines()
    result = ast.literal_eval(parse_block(lines)[:-1])
    # print(type(result))
    pprint.pprint(result)
    f.close()

generate_web_dict(LOCAL_WEB_FILE)

def ordering_compare():
    print('ordering')

# app_compare()
