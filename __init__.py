from .core import Quantity
from .util import enable_interactive_features

def setup(locals):
  from .util import make_and_import_modules, inject_extended_functions
  make_and_import_modules()
  inject_extended_functions(locals)

setup(globals())
del setup
