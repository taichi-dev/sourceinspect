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
