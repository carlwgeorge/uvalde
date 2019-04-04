import pathlib
import textwrap

import click.testing
import repomd

import uvalde


def test_import(tmp_path):
    runner = click.testing.CliRunner()

    args = ['import', '--keep-original', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))

    result = runner.invoke(uvalde.main, args)

    assert result.output == textwrap.dedent('''\
        tests/data/cello-1.0-1.i686.rpm -> {0}/repo1/i686/packages/c/
        tests/data/cello-1.0-1.src.rpm -> {0}/repo1/src/packages/c/
        tests/data/cello-1.0-1.x86_64.rpm -> {0}/repo1/x86_64/packages/c/
        tests/data/cello-debuginfo-1.0-1.i686.rpm -> {0}/repo1/i686/debug/packages/c/
        tests/data/cello-debuginfo-1.0-1.x86_64.rpm -> {0}/repo1/x86_64/debug/packages/c/
        tests/data/cello-debugsource-1.0-1.i686.rpm -> {0}/repo1/i686/debug/packages/c/
        tests/data/cello-debugsource-1.0-1.x86_64.rpm -> {0}/repo1/x86_64/debug/packages/c/
        tests/data/cello-extra-1.0-1.noarch.rpm -> {0}/repo1/i686/packages/c/
        tests/data/cello-extra-1.0-1.noarch.rpm -> {0}/repo1/x86_64/packages/c/
    '''.format(tmp_path))
    assert result.exit_code == 0

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
