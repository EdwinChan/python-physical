import builtins
import numbers
import sys
import types

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

def make_and_import_modules():
  for name, system in defined_systems.items():
    full_name = __package__ + '.' + name
    module = types.ModuleType(full_name)
    setattr(module, '__file__', '<generated>')
    setattr(module, '__package__', __package__)
    inject_variables(system, vars(module))
    setattr(sys.modules[__package__], name, module)
    sys.modules[full_name] = module

def inject_variables(system, locals):
  locals['system'] = system
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
    locals[name] = Quantity(1, 0, {unit: 1}, system)
  for data in system.constants.values():
    name = data['symbol']
    for symbol, english in symbol_to_english.items():
      name = name.replace(symbol, english)
    locals[name] = data['definition']

def inject_extended_functions(locals):
  for function in extended_functions:
    locals[function.__name__] = function

def enable_interactive_features(locals=None):
  import __main__
  locals = vars(__main__) if locals is None else locals
  Quantity.__repr__ = Quantity.__str__
  locals['Quantity'] = Quantity
  locals['expand'] = expand
  inject_extended_functions(locals)
