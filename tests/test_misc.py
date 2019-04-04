import pytest
import repomd

import uvalde


@pytest.mark.parametrize('real_path', [True, False])
def test_createrepo(tmp_path, real_path):
    target = tmp_path / 'repo'

    if real_path:
        target.mkdir()
        uvalde.repodata.createrepo(target)
        repo = repomd.load(f'file://{target}')
        assert len(repo) == 0
    else:
        with pytest.raises(FileExistsError, match='No such directory'):
            uvalde.repodata.createrepo(target)


@pytest.mark.parametrize(
    'start_exists,end_exists',
    [
        (False, False),
        (True, True),
        (True, False),
    ]
)
def test_safe_check(tmp_path, start_exists, end_exists):
    start = tmp_path / 'a'
    end = tmp_path / 'b'

    if start_exists:
        start.touch()
    if end_exists:
        end.touch()

    if not start_exists:
        with pytest.raises(SystemExit, match='a does not exist'):
            uvalde.transfer.safe_check(start, end)

    if end_exists:
        with pytest.raises(SystemExit, match='b already exists'):
            uvalde.transfer.safe_check(start, end)

    if start_exists and not end_exists:
        uvalde.transfer.safe_check(start, end)
        assert end.parent.exists()
        assert end.parent.is_dir()
