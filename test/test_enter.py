"""Test enter"""
import os
import pytest


@pytest.mark.parametrize(
    'shell, expected_code', [
        ('delete', 0),
        ('', 1),
        ('/usr/bin/env', 0),
        ('noexec', 1),
    ], ids=[
        'missing',
        'empty',
        'env',
        'not executable',
    ])
@pytest.mark.usefixtures('ds1_copy')
def test_enter(runner, yadm_y, paths, shell, expected_code):
    """Enter tests"""
    env = os.environ.copy()
    if shell == 'delete':
        if 'SHELL' in env:
            del env['SHELL']
    elif shell == 'noexec':
        noexec = paths.root.join('noexec')
        noexec.write('')
        noexec.chmod(0o664)
        env['SHELL'] = str(noexec)
    else:
        env['SHELL'] = shell
    run = runner(command=yadm_y('enter'), env=env)
    run.report()
    assert run.code == expected_code
    if expected_code == 0:
        assert run.out.startswith('Entering yadm repo')
        assert run.out.rstrip().endswith('Leaving yadm repo')
    if expected_code == 1:
        assert 'does not refer to an executable' in run.out
    if 'env' in shell:
        assert f'GIT_DIR={paths.repo}' in run.out
        assert 'PROMPT=yadm shell' in run.out
        assert 'PS1=yadm shell' in run.out