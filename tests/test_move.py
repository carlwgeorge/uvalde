import pathlib

import click.testing
import repomd

import uvalde


def test_move(tmp_path, tmp_config):
    runner = click.testing.CliRunner()

    args = ['add', '--keep', '--repo', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))
    runner.invoke(uvalde.main, args)

    result = runner.invoke(uvalde.main, ['move', '--from', 'repo1', '--to', 'repo2', 'cello-1.0-1'])

    assert result.exit_code == 0

    # src
    repo = repomd.load(f'file://{tmp_path}/repo1/src')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/src/packages/c/cello-1.0-1.src.rpm').exists()
    assert not (tmp_path / 'repo1/src/packages/c').exists()

    repo = repomd.load(f'file://{tmp_path}/repo2/src')
    assert [p.nevra for p in repo] == ['cello-1.0-1.src']
    assert (tmp_path / 'repo2/src/packages/c/cello-1.0-1.src.rpm').exists()

    # i686
    repo = repomd.load(f'file://{tmp_path}/repo1/i686')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/i686/packages/c/cello-1.0-1.i686.rpm').exists()
    assert not (tmp_path / 'repo1/i686/packages/c/cello-extra-1.0-1.noarch.rpm').exists()
    assert not (tmp_path / 'repo1/i686/packages/c').exists()

    repo = repomd.load(f'file://{tmp_path}/repo2/i686')
    assert [p.nevra for p in repo] == ['cello-1.0-1.i686', 'cello-extra-1.0-1.noarch']
    assert (tmp_path / 'repo2/i686/packages/c/cello-1.0-1.i686.rpm').exists()
    assert (tmp_path / 'repo2/i686/packages/c/cello-extra-1.0-1.noarch.rpm').exists()

    # i686 debug
    repo = repomd.load(f'file://{tmp_path}/repo1/i686/debug')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/i686/debug/packages/c/cello-debuginfo-1.0-1.i686.rpm').exists()
    assert not (tmp_path / 'repo1/i686/debug/packages/c/cello-debugsource-1.0-1.i686.rpm').exists()
    assert not (tmp_path / 'repo1/i686/debug/packages/c').exists()

    repo = repomd.load(f'file://{tmp_path}/repo2/i686/debug')
    assert [p.nevra for p in repo] == ['cello-debuginfo-1.0-1.i686', 'cello-debugsource-1.0-1.i686']
    assert (tmp_path / 'repo2/i686/debug/packages/c/cello-debuginfo-1.0-1.i686.rpm').exists()
    assert (tmp_path / 'repo2/i686/debug/packages/c/cello-debugsource-1.0-1.i686.rpm').exists()

    # x86_64
    repo = repomd.load(f'file://{tmp_path}/repo1/x86_64')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/x86_64/packages/c/cello-1.0-1.x86_64.rpm').exists()
    assert not (tmp_path / 'repo1/x86_64/packages/c/cello-extra-1.0-1.noarch.rpm').exists()
    assert not (tmp_path / 'repo1/x86_64/packages/c').exists()

    repo = repomd.load(f'file://{tmp_path}/repo2/x86_64')
    assert [p.nevra for p in repo] == ['cello-1.0-1.x86_64', 'cello-extra-1.0-1.noarch']
    assert (tmp_path / 'repo2/x86_64/packages/c/cello-1.0-1.x86_64.rpm').exists()
    assert (tmp_path / 'repo2/x86_64/packages/c/cello-extra-1.0-1.noarch.rpm').exists()

    # x86_64 debug
    repo = repomd.load(f'file://{tmp_path}/repo1/x86_64/debug')
    assert len(repo) == 0
    assert not (tmp_path / 'repo1/x86_64/debug/packages/c/cello-debuginfo-1.0-1.x86_64.rpm').exists()
    assert not (tmp_path / 'repo1/x86_64/debug/packages/c/cello-debugsource-1.0-1.x86_64.rpm').exists()
    assert not (tmp_path / 'repo1/x86_64/debug/packages/c').exists()

    repo = repomd.load(f'file://{tmp_path}/repo2/x86_64/debug')
    assert [p.nevra for p in repo] == ['cello-debuginfo-1.0-1.x86_64', 'cello-debugsource-1.0-1.x86_64']
    assert (tmp_path / 'repo2/x86_64/debug/packages/c/cello-debuginfo-1.0-1.x86_64.rpm').exists()
    assert (tmp_path / 'repo2/x86_64/debug/packages/c/cello-debugsource-1.0-1.x86_64.rpm').exists()


def test_move_mixed_architectures(tmp_config_mixed_architectures):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['move', '--from', 'repo1', '--to', 'repo2', 'cello-1.0-1'])

    assert 'configured architectures for repo1 and repo2 do not match' in result.output
    assert result.exit_code == 1
