import os
from functools import partial

import click
from hfmirror.storage import LocalStorage, HuggingfaceStorage
from hfmirror.sync import SyncTask
from huggingface_hub import create_repo

from sync.sync import GenshinDBResource
from .utils import GLOBAL_CONTEXT_SETTINGS
from .utils import print_version as _origin_print_version

print_version = partial(_origin_print_version, 'sync')


@click.group(context_settings={**GLOBAL_CONTEXT_SETTINGS}, help='Utils for sync genshin-db')
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True)
def cli():
    pass  # pragma: no cover


@cli.command('local', help='Sync genshin db data to local directory.',
             context_settings={**GLOBAL_CONTEXT_SETTINGS})
@click.option('--output_dir', '-O', 'output_dir', type=str, default='data',
              help='Output directory of genshin db data.', show_default=True)
def local(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    source = GenshinDBResource()
    storage = LocalStorage(output_dir)

    task = SyncTask(source, storage)
    task.sync()


@cli.command('huggingface', help='Sync genshin db data to huggingface directory.',
             context_settings={**GLOBAL_CONTEXT_SETTINGS})
@click.option('--repository', '-r', 'repository', type=str, default='hansbug/genshin-db-sync',
              help='Repository of genshin db data.', show_default=True)
def huggingface(repository):
    source = GenshinDBResource()
    access_token = os.environ.get('HF_TOKEN')
    create_repo(repository, token=access_token, repo_type='dataset', exist_ok=True)
    storage = HuggingfaceStorage(repository, access_token=access_token)

    task = SyncTask(source, storage)
    task.sync()


if __name__ == '__main__':
    cli()
