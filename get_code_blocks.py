from defines import REPODIR_PATH
from defines import CORPUSDIR_PATH
from pathlib import Path
from os import listdir
from numpy import std, average
from xml.etree import ElementTree as ET

import numpy.random as rd
import re

def get_comment_lengths():
    '''
    Gets a list containing number of lines of comments from the corpus, which can be naively used as a probability distribution.

    Return: comment_lengths, a list containing the number of newline characters in each comment in the corpora.
    '''
    comment_lengths = []

    for path in listdir(CORPUSDIR_PATH):
        path = CORPUSDIR_PATH / path
        with open(path, encoding='utf-8') as corpus:
            tree = ET.parse(corpus)
            root = tree.getroot()
            for note in root.iter('note'):
                raw = note.find('raw').text
                comment_lengths.append(raw.count('\n'))

    return comment_lengths
    
def get_python_sections(comment_lengths):
    all_python_lines = []
    docstring_delims = ("'''", '"""')

    paths = REPODIR_PATH.rglob("*.py")
    for path in paths:
        with open(path, encoding='utf-8') as source_file:
            docstring_active = 0
            source_file_lines = source_file.readlines()
            non_comment_lines = [line for line in source_file_lines if not line.strip().startswith('#') and line.strip()]
            
            for line in non_comment_lines:
                if docstring_active:
                    if any([delim in line for delim in docstring_delims]):
                        docstring_active = 0
                    continue
                            
                else:
                    if line.strip().startswith(docstring_delims):
                        docstring_active = 1
                        continue

                    elif any([delim in line for delim in docstring_delims]):
                        docstring_active = 0
                        line = line.split()[0]

                    else:
                        docstring_active = 0
                        if('#' in line): 
                            line = line.split('#')[0]
                
                all_python_lines.append(line)

    random_sample = []

    while len(random_sample) < 25:
        random_index = rd.randint(len(all_python_lines))
        random_length = rd.choice(comment_lengths)
        random_section = all_python_lines[random_index : random_index + random_length]

        if re.search('[a-zA-Z]', '|'.join(random_section)):
            random_sample.append(random_section)
        else:
            continue
    
    return random_sample

def get_clike_sections(comment_lengths, c_or_cpp):
    all_cpp_lines = []

    suffix = "*.cpp" if c_or_cpp else "*.c"

    paths = REPODIR_PATH.rglob(suffix)
    for path in paths:
        with open(path, encoding='utf-8') as source_file:
            docstring_active = 0
            source_file_lines = source_file.readlines()
            non_comment_lines = [line for line in source_file_lines if not line.strip().startswith('//') and line.strip()]
            
            for line in non_comment_lines:
                if docstring_active:
                    if "*\\" in line:
                        docstring_active = 0
                    continue
                            
                else:
                    if line.strip().startswith("/*"):
                        docstring_active = 1
                        continue

                    elif "/*" in line:
                        docstring_active = 0
                        line = line.split()[0]

                    else:
                        docstring_active = 0
                        if('//' in line): 
                            line = line.split('//')[0]
                
                all_cpp_lines.append(line)

    random_sample = []

    while len(random_sample) < 25:
        random_index = rd.randint(len(all_cpp_lines))
        random_length = rd.choice(comment_lengths)
        random_section = all_cpp_lines[random_index : random_index + random_length]

        if re.search('[a-zA-Z]', '|'.join(random_section)):
            random_sample.append(random_section)
        else:
            continue
    
    return random_sample

comment_lengths = get_comment_lengths()

python_sections = get_python_sections(comment_lengths)
c_sections = get_clike_sections(comment_lengths, 0)
cpp_sections = get_clike_sections(comment_lengths, 1)

print("##################")
print("PYTHON STARTS HERE")
print("##################")

for section in python_sections:
    for line in section:
        print(line, end='')
    print("\n\n =============================== \n\n")

print("###############")
print("C++ STARTS HERE")
print("###############")

for section in cpp_sections:
    for line in section:
        print(line, end='')
    print("\n\n =============================== \n\n")

print("#############")
print("C STARTS HERE")
print("#############")

for section in c_sections:
    for line in section:
        print(line, end='')
    print("\n\n =============================== \n\n")
