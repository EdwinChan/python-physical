from .core import Quantity

def setup(scope):
  from .util import make_and_import_modules, inject_extended_functions
  make_and_import_modules()
  inject_extended_functions(scope)

setup(globals())
del setup
