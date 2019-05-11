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
    setup_args = ['import', '--keep', '--repo', 'repo1']
    test_data = pathlib.Path('tests/data')
    setup_args.extend(map(str, test_data.glob('*.rpm')))
    runner.invoke(uvalde.main, setup_args)

    result = runner.invoke(uvalde.main, args)

    assert result.output == expected
    assert result.exit_code == 0
