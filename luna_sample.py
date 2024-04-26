#!/usr/bin/env python

import argparse
import json
from pathlib import Path
import random
import sys

from defines import Label
from defines import Language
from defines import NoteType
from reader import CccReader


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')

sample_parser = subparsers.add_parser(
    'sample',
)

label_parser = subparsers.add_parser(
    'label',
)

SAMPLE_SIZE = 50

BASE_PATH = Path('luna_sample')
PATH = {
    f'{language}': BASE_PATH / Path(f'{language}.json')
    for language in Language
}


def _filter_comments_by_language(xml_root, language):
    return [
        note for note in xml_root
        if note.find('language').text == language
    ]


def _filter_sample(sample):
    text_set = set()
    for example in list(sample):
        text = example.find('raw').text
        if text in text_set or text.startswith('--------'):
            sample.remove(example)
            print(text)
        else:
            text_set.add(text)


def _sample_to_json(sample, filepath):
    dictlist = [
        {
            'text': note.find('raw').text,
            'label': Label.NONE,
        }
        for note in sample
    ]

    with open(filepath, 'w') as f:
        json.dump(dictlist, f)


def sample():
    ccc = CccReader()

    comments = ccc.xml(categories=[NoteType.COMMENT])

    BASE_PATH.mkdir(exist_ok=True)
    for language in Language:
        lang_comments = _filter_comments_by_language(comments, language)

        lang_sample = []
        while len(lang_sample) < SAMPLE_SIZE:
            lang_sample.extend(random.sample(lang_comments, SAMPLE_SIZE - len(lang_sample)))
            _filter_sample(lang_sample)
            print(f"{language} {len(lang_sample)}")

        _sample_to_json(lang_sample, PATH[language])


def label():
    try:
        for language, path in PATH.items():
            with open(path, 'r') as f:
                sample = json.load(f)

            for example in sample:
                if example['label'] == Label.NONE:
                    print("```")
                    print(example['text'])
                    print("```")
                    print(f"({language})")
                    choice = None
                    while choice not in ('y', 'n'):
                        choice = input(
                            "Is this code? (y/n)> ",
                        ).lower()
                    if choice == 'y':
                        example['label'] = Label.CODE
                    elif choice == 'n':
                        example['label'] = Label.NONCODE
                    print()

                    with open(path, 'w') as f:
                        json.dump(sample, f)

    except FileNotFoundError:
        raise FileNotFoundError(f"{path} does not exist, please run `sample` subcommand.")


def main(argv):
    args = parser.parse_args(argv)
    if args.subcommand == 'sample':
        sample()
    elif args.subcommand == 'label':
        label()


if __name__ == '__main__': main(sys.argv[1:])
