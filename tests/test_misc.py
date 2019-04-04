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
