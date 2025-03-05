import builtins
import numbers
import sys
import types

from . import __main__
from .core import Quantity
from .define import defined_systems
from .func import extended_functions

def expand(quantity=None):
  if quantity is not None:
    return quantity.expand()
  quantity = getattr(builtins, '_', None)
  if isinstance(quantity, Quantity):
    return quantity.expand()
  elif isinstance(quantity, numbers.Real):
    return quantity

class Importer:
  @classmethod
  def make_and_import_modules(cls):
    for name, system in defined_systems.items():
      qualname = __package__ + '.' + name
      module = types.ModuleType(qualname)
      cls.inject_variables(system, vars(module))
      if not hasattr(__main__, '__file__') or sys.flags.interactive:
        cls.inject_interactive_features(module.__dict__)
      setattr(sys.modules[__package__], name, module)
      sys.modules[qualname] = module

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
      '\xb0':   'deg',      "'":      'arcmin',   '"':      'arcsec',
      '\u0127': 'hbar',     '\u2126': 'Ohm',      '\u212b': 'angstrom'}
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

  @staticmethod
  def inject_extended_functions(scope):
    for function in extended_functions:
      scope[function.__name__] = function

  @classmethod
  def inject_interactive_features(cls, scope):
    scope['Quantity'] = Quantity
    scope['Quantity'].__repr__ = scope['Quantity'].__str__
    scope['expand'] = expand
    cls.inject_extended_functions(scope)
