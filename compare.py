#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from subprocess import check_output
import pprint
import json

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
    result_list = []
    i = 0
    while i < len(lines) - 1:
        line = lines[i].strip()
        # print(str(i+1)+'\t'+line)
        if line and not any(line.startswith(txt) for txt in ['return [', '<?php', '/*', '|', '*/']) and '=>' in line:
            if line.endswith('['):
                block_list = []
                block_list.append(line.split(' => ')[0].strip('\''))
                sub_block_list = []
                for j in range(i+1, len(lines)):
                    block_line = lines[j].strip()
                    if block_line and not any(block_line.startswith(txt) for txt in ['return [', '<?php', '/*', '|', '*']) and '=>' in block_line:
                        sub_block_list.append(block_line.split(' => ')[0].strip('\''))
                    if block_line and block_line.startswith(']'):
                        i = j
                        block_list.append(sub_block_list)
                        break
                result_list.append(block_list)
            else:
                # print(line)
                result_list.append(line.split(' => ')[0].strip('\''))
        i += 1
    return result_list

def generate_web_key_list(filename, result_list):
    with open(filename) as f:
        lines = f.readlines()
        result_list = parse_block(lines)
    pp.pprint(result_list)
    f.close()

generate_web_key_list(LOCAL_WEB_FILE, local_web_key_list)

def ordering_compare():
    print('ordering')

# app_compare()
