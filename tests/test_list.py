import pathlib
import textwrap

import click.testing

import uvalde


def test_list_nvrs(tmp_path):
    runner = click.testing.CliRunner()

    # import rpms so output is meaningful
    args = ['import', '--keep-original', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))
    runner.invoke(uvalde.main, args)

    result = runner.invoke(uvalde.main, ['list', 'nvrs', 'repo1'])

    assert result.exit_code == 0
    assert result.output == textwrap.dedent('''\
        cello-1.0-1
    ''')


def test_list_repos():
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['list', 'repos'])

    assert result.exit_code == 0
    assert result.output == textwrap.dedent('''\
        repo1
        repo2
    ''')
