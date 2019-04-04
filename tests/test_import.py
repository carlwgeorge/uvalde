import pathlib
import shutil

import click.testing
import repomd

import uvalde


def test_import(tmp_path, tmp_config):
    runner = click.testing.CliRunner()

    args = ['import', 'repo1']
    test_data = pathlib.Path('tests/data')
    for rpm in test_data.glob('*.rpm'):
        destination = tmp_path / rpm.name
        shutil.copy2(rpm, destination)
        args.append(str(destination))

    result = runner.invoke(uvalde.main, args)

    for line in [
        '{0}/cello-1.0-1.i686.rpm -> {0}/repo1/i686/packages/c/',
        '{0}/cello-1.0-1.src.rpm -> {0}/repo1/src/packages/c/',
        '{0}/cello-1.0-1.x86_64.rpm -> {0}/repo1/x86_64/packages/c/',
        '{0}/cello-debuginfo-1.0-1.i686.rpm -> {0}/repo1/i686/debug/packages/c/',
        '{0}/cello-debuginfo-1.0-1.x86_64.rpm -> {0}/repo1/x86_64/debug/packages/c/',
        '{0}/cello-debugsource-1.0-1.i686.rpm -> {0}/repo1/i686/debug/packages/c/',
        '{0}/cello-debugsource-1.0-1.x86_64.rpm -> {0}/repo1/x86_64/debug/packages/c/',
        '{0}/cello-extra-1.0-1.noarch.rpm -> {0}/repo1/i686/packages/c/',
        '{0}/cello-extra-1.0-1.noarch.rpm -> {0}/repo1/x86_64/packages/c/',
    ]:
        assert line.format(tmp_path) in result.output

    assert result.exit_code == 0

    # ensure original files are gone
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
