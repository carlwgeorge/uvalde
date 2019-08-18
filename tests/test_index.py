import pathlib
import shutil

import appdirs
import click.testing

import uvalde
from uvalde.database import load_db, NVR


def test_index(tmp_config):
    runner = click.testing.CliRunner()

    args = ['add', '--keep', '--repo', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))
    runner.invoke(uvalde.main, args)

    db_dir = pathlib.Path(appdirs.user_data_dir('uvalde'))
    db_file = db_dir / 'index.1.db'
    db_file.unlink()

    result = runner.invoke(uvalde.main, ['index', 'repo1'])
    assert 'indexing repo repo1' in result.output
    assert result.exit_code == 0

    # db records
    db = load_db()
    nvr = NVR.get(label='cello-1.0-1')
    actual = set(
        (
            artifact.filename,
            artifact.architecture,
            artifact.debug,
        )
        for artifact in nvr.artifacts
    )
    expected = set([
        ('cello-1.0-1.src.rpm', 'src', False),
        ('cello-1.0-1.i686.rpm', 'i686', False),
        ('cello-debuginfo-1.0-1.i686.rpm', 'i686', True),
        ('cello-debugsource-1.0-1.i686.rpm', 'i686', True),
        ('cello-1.0-1.x86_64.rpm', 'x86_64', False),
        ('cello-debuginfo-1.0-1.x86_64.rpm', 'x86_64', True),
        ('cello-debugsource-1.0-1.x86_64.rpm', 'x86_64', True),
        ('cello-extra-1.0-1.noarch.rpm', 'noarch', False),
    ])
    assert actual == expected
    db.close()


def test_index_unexpected_path_noarch(tmp_path, tmp_config):
    runner = click.testing.CliRunner()

    args = ['add', '--keep', '--repo', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))
    result = runner.invoke(uvalde.main, args)
    assert result.exit_code == 0

    shutil.move(
        tmp_path / 'repo1/x86_64/packages/c/cello-extra-1.0-1.noarch.rpm',
        tmp_path / 'repo1/x86_64/cello-extra-1.0-1.noarch.rpm',
    )

    result = runner.invoke(uvalde.main, ['index', 'repo1'])
    assert 'cello-extra-1.0-1.noarch.rpm: not in expected location' in result.output
    assert result.exit_code == 1


def test_index_unexpected_path(tmp_path, tmp_config):
    runner = click.testing.CliRunner()

    args = ['add', '--keep', '--repo', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))
    result = runner.invoke(uvalde.main, args)
    assert result.exit_code == 0

    shutil.move(
        tmp_path / 'repo1/x86_64/packages/c/cello-1.0-1.x86_64.rpm',
        tmp_path / 'repo1/x86_64/cello-1.0-1.x86_64.rpm',
    )

    result = runner.invoke(uvalde.main, ['index', 'repo1'])
    assert 'cello-1.0-1.x86_64.rpm: not in expected location' in result.output
    assert result.exit_code == 1


def test_index_architecture_not_configured(tmp_path, tmp_config_architecture_not_configured):
    runner = click.testing.CliRunner()

    # We need a good config to setup the structure, then a bad config to test
    # an exception.  Since we can't swap the config during the test, fake the
    # initial structure.
    test_data = pathlib.Path('tests/data')
    for destination in [
        tmp_path / 'repo1/src/packages/c/cello-1.0-1.src.rpm',
        tmp_path / 'repo1/i686/packages/c/cello-1.0-1.i686.rpm',
        tmp_path / 'repo1/i686/packages/c/cello-extra-1.0-1.noarch.rpm',
        tmp_path / 'repo1/i686/debug/packages/c/cello-debuginfo-1.0-1.i686.rpm',
        tmp_path / 'repo1/i686/debug/packages/c/cello-debugsource-1.0-1.i686.rpm',
        tmp_path / 'repo1/x86_64/packages/c/cello-1.0-1.x86_64.rpm',
        tmp_path / 'repo1/x86_64/packages/c/cello-extra-1.0-1.noarch.rpm',
        tmp_path / 'repo1/x86_64/debug/packages/c/cello-debuginfo-1.0-1.x86_64.rpm',
        tmp_path / 'repo1/x86_64/debug/packages/c/cello-debugsource-1.0-1.x86_64.rpm',
    ]:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(test_data / destination.name, destination)

    result = runner.invoke(uvalde.main, ['index', 'repo1'])
    assert 'architecture not configured for repo repo1' in result.output
    assert result.exit_code == 1
