import textwrap

import click.testing

import uvalde


def test_config_show(tmp_path, tmp_config):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['config', 'show', 'repo1'])

    assert result.output == textwrap.dedent('''\
        [repo1]
        base = {}/repo1
        architectures = i686, x86_64
    '''.format(tmp_path))
    assert result.exit_code == 0
