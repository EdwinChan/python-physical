from .core import Quantity

def setup(locals):
  from .util import make_and_import_modules, inject_extended_functions
  make_and_import_modules()
  inject_extended_functions(locals)

setup(globals())
del setup
