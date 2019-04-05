import pathlib

import setuptools


with pathlib.Path('README.md').open() as f:
    long_description = f.read()


setuptools.setup(
    name='uvalde',
    version='0.3.0',
    author='Carl George',
    author_email='carl@george.computer',
    description='Yum repository management tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/carlwgeorge/uvalde',
    license='MIT',
    package_dir={'': 'source'},
    packages=['uvalde'],
    # f-strings
    python_requires='>=3.6',
    # markdown content type
    setup_requires=['setuptools>=38.6.0'],
    install_requires=[
        'appdirs',
        'click',
        'createrepo_c',
        'peewee',
    ],
    extras_require={
        'tests': [
            'pytest',
            'pytest-cov',
            'pytest-flake8',
            'repomd',
        ],
    },
    entry_points={'console_scripts': ['uvalde=uvalde:main']},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Software Distribution',
    ],
)
