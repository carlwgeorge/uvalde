import shutil

import click


def echo_move(start, end):
    """Print a colorized message describing a move/copy."""

    click.echo(
        click.style(f'{start}', fg='cyan') +
        click.style(' -> ', fg='yellow') +
        click.style(f'{end.parent}/', fg='green')
    )


def safe_check(start, end):
    """Validate existence of files and directories for a move/copy."""

    if not start.exists():
        raise SystemExit(f'{start} does not exist')
    if end.exists():
        raise SystemExit(f'{end} already exists')
    if not end.parent.is_dir():
        end.parent.mkdir(parents=True)


def safe_move(start, end, cleanup=False):
    """Safely move file."""

    safe_check(start, end)
    echo_move(start, end)
    shutil.move(start, end)
    if cleanup:
        # if the parent directory is empty, remove it
        try:
            next(start.parent.glob('*'))
        except StopIteration:
            start.parent.rmdir()


def safe_copy(start, end):
    """Safely copy file."""

    safe_check(start, end)
    echo_move(start, end)
    shutil.copy2(start, end)
