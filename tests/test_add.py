import pathlib
import shutil

import click.testing
import pytest
import repomd

import uvalde


@pytest.mark.parametrize('keep_flag', [False, True], ids=['remove original', 'keep original'])
def test_add(tmp_path, tmp_config, keep_flag):
    runner = click.testing.CliRunner()

    args = ['add', '--repo', 'repo1']
    if keep_flag:
        args.append('--keep')
    test_data = pathlib.Path('tests/data')
    for rpm in test_data.glob('*.rpm'):
        destination = tmp_path / rpm.name
        shutil.copy2(rpm, destination)
        args.append(str(destination))

    result = runner.invoke(uvalde.main, args)

    assert result.exit_code == 0

    # check original files
    for rpm in [
        'cello-1.0-1.i686.rpm',
        'cello-1.0-1.src.rpm',
        'cello-1.0-1.x86_64.rpm',
        'cello-debuginfo-1.0-1.i686.rpm',
        'cello-debuginfo-1.0-1.x86_64.rpm',
        'cello-debugsource-1.0-1.i686.rpm',
        'cello-debugsource-1.0-1.x86_64.rpm',
        'cello-extra-1.0-1.noarch.rpm',
    ]:
        if keep_flag:
            assert (test_data / rpm).exists()
        else:
            assert not (tmp_path / rpm).exists()

    # src
    repo = repomd.load(f'file://{tmp_path}/repo1/src')
    assert [p.nevra for p in repo] == ['cello-1.0-1.src']
    assert (tmp_path / 'repo1/src/packages/c/cello-1.0-1.src.rpm').exists()

    # i686
    repo = repomd.load(f'file://{tmp_path}/repo1/i686')
    assert [p.nevra for p in repo] == ['cello-1.0-1.i686', 'cello-extra-1.0-1.noarch']
    assert (tmp_path / 'repo1/i686/packages/c/cello-1.0-1.i686.rpm').exists()
    assert (tmp_path / 'repo1/i686/packages/c/cello-extra-1.0-1.noarch.rpm').exists()

    # i686 debug
    repo = repomd.load(f'file://{tmp_path}/repo1/i686/debug')
    assert [p.nevra for p in repo] == ['cello-debuginfo-1.0-1.i686', 'cello-debugsource-1.0-1.i686']
    assert (tmp_path / 'repo1/i686/debug/packages/c/cello-debuginfo-1.0-1.i686.rpm').exists()
    assert (tmp_path / 'repo1/i686/debug/packages/c/cello-debugsource-1.0-1.i686.rpm').exists()

    # x86_64
    repo = repomd.load(f'file://{tmp_path}/repo1/x86_64')
    assert [p.nevra for p in repo] == ['cello-1.0-1.x86_64', 'cello-extra-1.0-1.noarch']
    assert (tmp_path / 'repo1/x86_64/packages/c/cello-1.0-1.x86_64.rpm').exists()
    assert (tmp_path / 'repo1/x86_64/packages/c/cello-extra-1.0-1.noarch.rpm').exists()

    # x86_64 debug
    repo = repomd.load(f'file://{tmp_path}/repo1/x86_64/debug')
    assert [p.nevra for p in repo] == ['cello-debuginfo-1.0-1.x86_64', 'cello-debugsource-1.0-1.x86_64']
    assert (tmp_path / 'repo1/x86_64/debug/packages/c/cello-debuginfo-1.0-1.x86_64.rpm').exists()
    assert (tmp_path / 'repo1/x86_64/debug/packages/c/cello-debugsource-1.0-1.x86_64.rpm').exists()


def test_add_architecture_not_configured(tmp_config_architecture_not_configured):
    runner = click.testing.CliRunner()

    args = ['add', '--keep', '--repo', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))

    result = runner.invoke(uvalde.main, args)
    assert 'architecture not configured for repo1' in result.output
    assert result.exit_code == 1
