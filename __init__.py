from .core import Quantity

def setup():
  import sys
  from .util import Importer
  Importer.make_and_import_modules()
  Importer.inject_extended_functions(sys.modules[__package__].__dict__)

setup()
del setup
