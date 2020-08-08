project_name = 'sourceinspect'
version = '0.0.1'
description = 'A unified inspector for retriving source from Python objects'
long_description = '''
SourceInspect
=============

The functionality is mainly same as ``inspect``, but fixing the ``OSError``
when used in some non-standard shells.

API reference
-------------

- ``sourceinspect.getsource(object)``
- ``sourceinspect.getsourcelines(object)``
- ``sourceinspect.getsourcefile(object)``


Supported shells
----------------

- Python script (wrap ``dill.source``)
- Python interactive shell (wrap ``dill.source``)
- IPython advanced shell (wrap ``IPython.core.oinspect``)
- Jupyter notebook (wrap ``IPython.core.oinspect``)
- Blender scripting module (add hooks to ``inspect``)
- Blender interactive mode (add hooks to ``code.py``)
- Python IDLE file mode (wraps ``dill.source``)
- Python IDLE interactive mode (need manually add hooks to ``code.py``)
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
