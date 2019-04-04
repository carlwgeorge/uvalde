import pathlib

import click.testing

import uvalde


def test_import(tmp_path):
    runner = click.testing.CliRunner()

    args = ['import', '--keep-original', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))

    result = runner.invoke(uvalde.main, args)

    assert result.exit_code == 0
    for path in [
        tmp_path / 'repo1/src/packages/c/cello-1.0-1.src.rpm',
        tmp_path / 'repo1/src/repodata/repomd.xml',
        tmp_path / 'repo1/src/repodata/other.xml.gz',
        tmp_path / 'repo1/src/repodata/filelists.xml.gz',
        tmp_path / 'repo1/src/repodata/primary.xml.gz',

        tmp_path / 'repo1/i686/packages/c/cello-1.0-1.i686.rpm',
        tmp_path / 'repo1/i686/packages/c/cello-extra-1.0-1.noarch.rpm',
        tmp_path / 'repo1/i686/repodata/repomd.xml',
        tmp_path / 'repo1/i686/repodata/other.xml.gz',
        tmp_path / 'repo1/i686/repodata/filelists.xml.gz',
        tmp_path / 'repo1/i686/repodata/primary.xml.gz',

        tmp_path / 'repo1/i686/debug/packages/c/cello-debuginfo-1.0-1.i686.rpm',
        tmp_path / 'repo1/i686/debug/packages/c/cello-debugsource-1.0-1.i686.rpm',
        tmp_path / 'repo1/i686/debug/repodata/repomd.xml',
        tmp_path / 'repo1/i686/debug/repodata/other.xml.gz',
        tmp_path / 'repo1/i686/debug/repodata/filelists.xml.gz',
        tmp_path / 'repo1/i686/debug/repodata/primary.xml.gz',

        tmp_path / 'repo1/x86_64/packages/c/cello-1.0-1.x86_64.rpm',
        tmp_path / 'repo1/x86_64/packages/c/cello-extra-1.0-1.noarch.rpm',
        tmp_path / 'repo1/x86_64/repodata/repomd.xml',
        tmp_path / 'repo1/x86_64/repodata/other.xml.gz',
        tmp_path / 'repo1/x86_64/repodata/filelists.xml.gz',
        tmp_path / 'repo1/x86_64/repodata/primary.xml.gz',

        tmp_path / 'repo1/x86_64/debug/packages/c/cello-debuginfo-1.0-1.x86_64.rpm',
        tmp_path / 'repo1/x86_64/debug/packages/c/cello-debugsource-1.0-1.x86_64.rpm',
        tmp_path / 'repo1/x86_64/debug/repodata/repomd.xml',
        tmp_path / 'repo1/x86_64/debug/repodata/other.xml.gz',
        tmp_path / 'repo1/x86_64/debug/repodata/filelists.xml.gz',
        tmp_path / 'repo1/x86_64/debug/repodata/primary.xml.gz',
    ]:
        assert path.exists()
