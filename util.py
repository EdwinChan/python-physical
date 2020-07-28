import __main__
import builtins
import importlib
import numbers
import sys
import types

from .core import Quantity, extended_functions
from .define import defined_systems

def expand(quantity=None):
  if quantity is not None:
    return quantity.expand()
  else:
    if '_' in builtins.__dict__:
      quantity = builtins._
      if isinstance(quantity, Quantity):
        return quantity.expand()
      elif isinstance(quantity, numbers.Real):
        return quantity

class Importer:
  fullname_to_system = {'{}.{}'.format(__package__, key): value
    for key, value in defined_systems.items()}

  def find_module(self, fullname, path=None):
    return self if fullname in self.fullname_to_system else None

  def load_module(self, fullname):
    if fullname in sys.modules:
      return sys.modules[fullname]
    elif fullname in self.fullname_to_system:
      module = types.ModuleType(fullname)
      system = self.fullname_to_system[fullname]
      self.inject_variables(system, module.__dict__)
      if not hasattr(__main__, '__file__') or sys.flags.interactive:
        self.inject_interactive_features(module.__dict__)
      sys.modules[fullname] = module
      return module
    else:
      raise ImportError()

  @staticmethod
  def module_repr(module):
    return "<module '{}' (virtual)>".format(module.__name__)

  @classmethod
  def enable(cls):
    sys.meta_path.append(cls())
    # import all virtual modules once, so that they are added to sys.modules
    # and that they are available even if only the package is imported
    for fullname in cls.fullname_to_system:
      importlib.import_module(fullname)

  @staticmethod
  def inject_variables(system, scope):
    scope['system'] = system
    symbol_to_english = {
      '\u03b1': 'alpha',    '\u03b2': 'beta',     '\u03b3': 'gamma',
      '\u03b4': 'delta',    '\u03b5': 'epsilon',  '\u03b6': 'zeta',
      '\u03b7': 'eta',      '\u03b8': 'theta',    '\u03b9': 'iota',
      '\u03ba': 'kappa',    '\u03bb': 'lambda',   '\u03bc': 'mu',
      '\u03bd': 'nu',       '\u03be': 'xi',       '\u03bf': 'omicron',
      '\u03c0': 'pi',       '\u03c1': 'rho',      '\u03c3': 'sigma',
      '\u03c4': 'tau',      '\u03c5': 'upsilon',  '\u03c6': 'phi',
      '\u03c7': 'chi',      '\u03c8': 'psi',      '\u03c9': 'omega',
      '\xb0':   'deg',      "'":      'min',      '"':      'sec',
      '\u0127': 'hbar',     '\u2126': 'Ohm',      '\u212b': 'angstrom'
    }
    for unit, data in system.units.items():
      name = data['symbol']
      for symbol, english in symbol_to_english.items():
        name = name.replace(symbol, english)
      scope[name] = Quantity(1, 0, {unit: 1}, system)
    for data in system.constants.values():
      name = data['symbol']
      for symbol, english in symbol_to_english.items():
        name = name.replace(symbol, english)
      scope[name] = data['definition']

  @classmethod
  def inject_interactive_features(cls, scope):
    scope['Quantity'] = Quantity
    scope['Quantity'].__repr__ = scope['Quantity'].__str__
    scope['expand'] = expand
    cls.inject_extended_functions(scope)

  @staticmethod
  def inject_extended_functions(scope):
    for function in extended_functions:
      scope[function.__name__] = function
