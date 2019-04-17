import pathlib
import textwrap

import click.testing

import uvalde


def test_list_all(tmp_config):
    runner = click.testing.CliRunner()

    # import rpms so output is meaningful
    args = ['import', '--keep', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))
    runner.invoke(uvalde.main, args)

    result = runner.invoke(uvalde.main, ['list', 'all'])

    assert result.output == textwrap.dedent('''\
        repo1
          cello-1.0-1
        repo2
    ''')
    assert result.exit_code == 0


def test_list_nvrs(tmp_config):
    runner = click.testing.CliRunner()

    # import rpms so output is meaningful
    args = ['import', '--keep', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))
    runner.invoke(uvalde.main, args)

    result = runner.invoke(uvalde.main, ['list', 'nvrs', 'repo1'])

    assert result.output == textwrap.dedent('''\
        cello-1.0-1
    ''')
    assert result.exit_code == 0


def test_list_repos(tmp_config):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['list', 'repos'])

    assert result.output == textwrap.dedent('''\
        repo1
        repo2
    ''')
    assert result.exit_code == 0
