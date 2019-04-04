import textwrap

import click.testing

import uvalde


def test_list_repos():
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['list', 'repos'])

    assert result.exit_code == 0
    assert result.output == textwrap.dedent('''\
        repo1
        repo2
    ''')
