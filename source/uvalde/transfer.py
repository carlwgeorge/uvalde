import click


def safe_check(start, end):
    """Validate existence of files and directories for a move/copy."""

    click.echo(
        click.style(f'{start}', fg='cyan') +
        click.style(' -> ', fg='yellow') +
        click.style(f'{end.parent}/', fg='green')
    )

    if not start.exists():
        raise SystemExit(f'{start} does not exist')
    if end.exists():
        raise SystemExit(f'{end} already exists')
    if not end.parent.is_dir():
        end.parent.mkdir(parents=True)


def remove_empty_parent(target):
    """Remove the parent directory if empty."""

    try:
        next(target.parent.glob('*'))
    except StopIteration:
        target.parent.rmdir()
