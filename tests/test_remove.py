import pathlib

import click.testing
import repomd

import uvalde


def test_remove(tmp_path, tmp_config):
    runner = click.testing.CliRunner()

    args = ['add', '--keep', '--repo', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))
    runner.invoke(uvalde.main, args)

    result = runner.invoke(uvalde.main, ['remove', '--repo', 'repo1', 'cello-1.0-1'])

    assert result.exit_code == 0

    # src
    repo = repomd.load(f'file://{tmp_path}/repo1/src')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/src/packages/c/cello-1.0-1.src.rpm').exists()
    assert not (tmp_path / 'repo1/src/packages/c').exists()

    # i686
    repo = repomd.load(f'file://{tmp_path}/repo1/i686')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/i686/packages/c/cello-1.0-1.i686.rpm').exists()
    assert not (tmp_path / 'repo1/i686/packages/c/cello-extra-1.0-1.noarch.rpm').exists()
    assert not (tmp_path / 'repo1/i686/packages/c').exists()

    # i686 debug
    repo = repomd.load(f'file://{tmp_path}/repo1/i686/debug')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/i686/debug/packages/c/cello-debuginfo-1.0-1.i686.rpm').exists()
    assert not (tmp_path / 'repo1/i686/debug/packages/c/cello-debugsource-1.0-1.i686.rpm').exists()
    assert not (tmp_path / 'repo1/i686/debug/packages/c').exists()

    # x86_64
    repo = repomd.load(f'file://{tmp_path}/repo1/x86_64')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/x86_64/packages/c/cello-1.0-1.x86_64.rpm').exists()
    assert not (tmp_path / 'repo1/x86_64/packages/c/cello-extra-1.0-1.noarch.rpm').exists()
    assert not (tmp_path / 'repo1/x86_64/packages/c').exists()

    # x86_64 debug
    repo = repomd.load(f'file://{tmp_path}/repo1/x86_64/debug')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/x86_64/debug/packages/c/cello-debuginfo-1.0-1.x86_64.rpm').exists()
    assert not (tmp_path / 'repo1/x86_64/debug/packages/c/cello-debugsource-1.0-1.x86_64.rpm').exists()
    assert not (tmp_path / 'repo1/x86_64/debug/packages/c').exists()
