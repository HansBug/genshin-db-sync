import json
import os.path
from contextlib import contextmanager
from typing import ContextManager, List, Iterable, Union, Tuple, Any, Mapping

from hbutils.system import TemporaryDirectory
from hfmirror.resource import SyncItem, SyncResource
from hfmirror.resource.item import register_sync_type
from hfmirror.utils import TargetPathType

from .lib import LANGS, DATA_CATEGORIES, get_data_with_category


class JsonDataSyncItem(SyncItem):
    __type__ = 'json'

    def __init__(self, value, metadata: dict, segments: List[str]):
        SyncItem.__init__(self, value, metadata, segments)
        self.value = value

    @contextmanager
    def load_file(self) -> ContextManager[str]:
        with TemporaryDirectory() as td:
            json_file = os.path.join(td, 'data.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.value, f, indent=4, ensure_ascii=False, sort_keys=True)

            yield json_file


register_sync_type(JsonDataSyncItem)


class GenshinDBResource(SyncResource):
    def grab(self) -> Iterable[Union[
        Tuple[str, Any, TargetPathType, Mapping],
        Tuple[str, Any, TargetPathType],
    ]]:
        for lang in LANGS:
            for category in DATA_CATEGORIES:
                yield 'json', get_data_with_category(category, lang), f'{lang}/{category}.json'
