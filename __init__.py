from .core import Quantity

def setup(scope):
  from .util import Importer
  Importer.make_and_import_modules()
  Importer.inject_extended_functions(scope)

setup(globals())
del setup
