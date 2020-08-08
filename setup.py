project_name = 'sourceinspect'
version = '0.0.1'
description = 'A unified inspector for retriving source from Python objects'
long_description = '''
SourceInspect
=============
'''
classifiers = [
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
]
python_requires = '>=3.6'
install_requires = [
    'dill',
]

import setuptools

setuptools.setup(
    name=project_name,
    version=version,
    author='彭于斌',
    author_email='1931127624@qq.com',
    description=description,
    long_description=long_description,
    classifiers=classifiers,
    python_requires=python_requires,
    install_requires=install_requires,
    packages=setuptools.find_packages(),
)
