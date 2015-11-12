from .core import Quantity
from .util import Importer

Importer.enable()
Importer.insert_extended_functions(globals())
del Importer
