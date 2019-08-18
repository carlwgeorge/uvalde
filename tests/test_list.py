import pathlib
import textwrap

import click.testing
import pytest

import uvalde


@pytest.mark.parametrize(
    'args,expected',
    [
        (
            ['list'],
            textwrap.dedent('''\
                repo1
                  cello-1.0-1
                repo2
            ''')
        ),
        (
            ['list', '--name', 'cello'],
            textwrap.dedent('''\
                repo1
                  cello-1.0-1
                repo2
            ''')
        ),
        (
            ['list', '--name', 'bello'],
            textwrap.dedent('''\
                repo1
                repo2
            ''')
        ),
        (
            ['list', '--repo', 'repo1'],
            textwrap.dedent('''\
                repo1
                  cello-1.0-1
            ''')
        ),
        (
            ['list', '--repo', 'repo2'],
            textwrap.dedent('''\
                repo2
            ''')
        ),
    ],
    ids=[
        'no filters',
        'filter name cello',
        'filter name bello',
        'filter repo repo1',
        'filter repo repo2',
    ],
)
def test_list(tmp_config, args, expected):
    runner = click.testing.CliRunner()

    # import rpms so output is meaningful
    setup_args = ['add', '--keep', '--repo', 'repo1']
    test_data = pathlib.Path('tests/data')
    setup_args.extend(map(str, test_data.glob('*.rpm')))
    runner.invoke(uvalde.main, setup_args)

    result = runner.invoke(uvalde.main, args)

    assert result.output == expected
    assert result.exit_code == 0


@pytest.mark.parametrize(
    'args,expected',
    [
        (
            ['list'],
            textwrap.dedent('''\
                repo1
            ''')
        ),
        (
            ['list', '--all'],
            textwrap.dedent('''\
                repo1
                repo2
            ''')
        ),
        (
            ['list', '--repo', 'repo1'],
            textwrap.dedent('''\
                repo1
            ''')
        ),
        (
            ['list', '--repo', 'repo2'],
            textwrap.dedent('''\
                repo2
            ''')
        ),
        (
            ['list', '--repo', 'repo1', '--repo', 'repo2'],
            textwrap.dedent('''\
                repo1
                repo2
            ''')
        ),
        (
            ['list', '--all', '--repo', 'repo1'],
            textwrap.dedent('''\
                repo1
            ''')
        ),
        (
            ['list', '--all', '--repo', 'repo2'],
            textwrap.dedent('''\
                repo2
            ''')
        ),
        (
            ['list', '--all', '--repo', 'repo1', '--repo', 'repo2'],
            textwrap.dedent('''\
                repo1
                repo2
            ''')
        ),
    ],
    ids=[
        'normal',
        'all',
        'filter repo',
        'filter hidden repo',
        'filter repo and hidden repo',
        'all and filter repo',
        'all and filter hidden repo',
        'all and filter repo and hidden repo',
    ],
)
def test_list_hidden(tmp_config_hidden, args, expected):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, args)

    assert result.output == expected
    assert result.exit_code == 0
