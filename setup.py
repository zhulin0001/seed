import os
from setuptools import setup, find_packages

VERSION = '0.1'


def get_requirements(env):
    with open('requirements-{}.txt'.format(env)) as fp:
        return [x.strip() for x in fp.read().split('\n') if not x.startswith('#')]


install_requires = get_requirements('base')


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths
    # for (path, directories, filenames) in os.walk(directory):
    #     paths.append(os.path.join(path, '*'))
    # return paths


static_files = package_files(os.path.join('src', 'seed', 'static'))


setup(
    name='seed',
    version=VERSION,
    install_requires=install_requires,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # package_data={
    #     '': static_folders
    # },
    data_files=static_files,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'seed = seed.runner:main',
        ]
    }
)
