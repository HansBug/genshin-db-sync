import glob
import json
import os.path
from typing import List

DB_DIR = 'genshin_db'

if not os.path.exists(DB_DIR):
    raise FileNotFoundError(f'{DB_DIR!r} not found, please execute \'make dataset\' to download this.')

DB_DATA_DIR = os.path.join(DB_DIR, 'src', 'data')

LANGS = [
    os.path.dirname(os.path.relpath(dir_, DB_DATA_DIR)) for dir_ in
    glob.glob(os.path.join(DB_DATA_DIR, '*', 'tcgactioncards'))
]


def get_langs() -> List[str]:
    return LANGS


DATA_CATEGORIES = ['tcgactioncards', 'tcgcardbacks', 'tcgcardboxes', 'tcgcharactercards', 'tcgdetailedrules',
                   'tcgenemycards', 'tcgkeywords', 'tcglevelrewards', 'tcgstatuseffects', 'tcgsummons']


def get_data_with_category(category, lang):
    items_dir = os.path.join(DB_DATA_DIR, lang, category)
    meta_path = os.path.join(DB_DATA_DIR, 'index', lang, f'{category}.json')

    items = {}
    for ifile in os.listdir(items_dir):
        with open(os.path.join(items_dir, ifile), 'r') as f:
            data = json.load(f)

        name = os.path.splitext(ifile)[0]
        items[name] = data

    with open(meta_path, 'r') as f:
        meta = json.load(f)

    return {
        'items': items,
        'meta': meta
    }
