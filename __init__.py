from .core import Quantity
from .util import Importer

Importer.enable()
Importer.inject_extended_functions(globals())
del Importer
