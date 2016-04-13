import copy
import fractions
import functools
import math
import numbers
import re
import sys
import weakref

class UnitArithmetic:
  @classmethod
  def multiply(cls, first, second):
    result = first.copy()
    for unit, power in second.items():
      result[unit] = result.get(unit, 0) + power
    return cls.clean(result)

  @classmethod
  def divide(cls, first, second):
    result = first.copy()
    for unit, power in second.items():
      result[unit] = result.get(unit, 0) - power
    return cls.clean(result)

  @classmethod
  def power(cls, units, other):
    if other == 0:
      return {}
    else:
      return cls.clean({unit: power * other for unit, power in units.items()})

  @staticmethod
  def clean(units):
    result = {}
    for unit, power in units.items():
      if isinstance(power, fractions.Fraction):
        if power.denominator == 1:
          if not power.numerator == 0:
            result[unit] = power.numerator
        else:
          result[unit] = power
      else:
        rounded = round(power)
        # each operation contributes at most one epsilon of relative error;
        # assuming limited number of operations and powers close to unity,
        # this is a reasonable upper bound for the absolute error
        if abs(power - rounded) < 16 * sys.float_info.epsilon:
          if rounded != 0:
            result[unit] = rounded
        else:
          result[unit] = power
    return result

class UnitSystem:
  def __init__(self):
    self.units = {}
    self.constants = {}

  def add_unit(self, unit, symbol, expansion=None):
    if expansion is not None and expansion.system() is not self:
      raise TypeError('unit expansion is not in terms of system units')
    self.units[unit] = {'symbol': symbol, 'expansion': expansion}

  def add_constant(self, constant, symbol, definition):
    if definition.system() is not self:
      raise TypeError('constant definition is not in terms of system units')
    self.constants[constant] = {'symbol': symbol, 'definition': definition}

  def get_constant(self, arg):
    if isinstance(arg, dict):
      # argument is a dictionary of constants and their powers
      return functools.reduce(Quantity.__mul__,
        (self.constants[constant]['definition'] ** power
          for constant, power in arg.items()))
    else:
      # argument is the name of a constant
      return self.constants[arg]['definition']

  def expand_quantity(self, quantity):
    return (Quantity(quantity.value, quantity.error, {}, self) *
      self.expand_units(quantity.units))

  def expand_units(self, units):
    if not units:
      return Quantity(1, 0, {}, self)
    units = list(units.items())
    expansions = []
    while units:
      unit, power = units.pop()
      expansion = self.units.get(unit, {'expansion': None})['expansion']
      if expansion is None:
        expansions.append(Quantity(1, 0, {unit: power}, self))
      else:
        temp = expansion ** power
        units += list(temp.units.items())
        expansions.append(Quantity(temp.value, temp.error, {}, self))
    return functools.reduce(Quantity.__mul__, expansions)

  def format_quantity(self, quantity, format_spec):
    if quantity.units:
      units_string = ' '.join(self.format_unit(unit, power)
        for unit, power in sorted(quantity.units.items(),
        key=lambda arg: (math.copysign(1, -arg[1]), arg[0])))
      if quantity.error == 0:
        return '{} {}'.format(quantity.value, units_string)
      else:
        value_error_string = self.format_value_error(
          quantity.value, quantity.error, format_spec, parens=True)
        return '{} {}'.format(value_error_string, units_string)
    else:
      if quantity.error == 0:
        return str(quantity.value)
      else:
        return self.format_value_error(
          quantity.value, quantity.error, format_spec)

  @staticmethod
  def format_value_error(value, error, format_spec, parens=False):
    # options: number of significant digits displayed for error
    #          separate value and error ('s') or parenthesize error ('p')
    error_sigfig, mode = 2, 's'
    match = re.match(r'^(\d*)([sp])$', format_spec)
    if match:
      temp = match.group(1)
      if temp:
        temp = int(temp)
        if temp > 0:
          error_sigfig = temp
      mode = match.group(2)
    # 'head' and 'tail' refer to the places (in positional notation) of the
    # highest and lowest displayed digits of a number
    value_head = math.floor(math.log10(abs(value)))
    error_head = math.floor(math.log10(error))
    error_tail = error_head - error_sigfig + 1
    if mode == 's':
      dp = max(value_head - error_tail, 0)
      if value_head == 0:
        result = '{:.{dp}f} \xb1 {:.{dp}f}'.format(value, error, dp=dp)
        return '({})'.format(result) if parens else result
      else:
        temp1 = value / 10**value_head
        temp2 = error / 10**value_head
        return '({:.{dp}f} \xb1 {:.{dp}f})e{}'.format(temp1, temp2, value_head,
          dp=dp)
    else:
      if value_head >= error_head:
        formatted_head = value_head
        dp = value_head - error_tail
      else:
        formatted_head = error_head
        dp = error_sigfig - 1
      temp1 = value / 10**formatted_head
      temp2 = round(error / 10**error_tail)
      if formatted_head == 0:
        return '{:.{dp}f}({})'.format(temp1, temp2, dp=dp)
      else:
        return '{:.{dp}f}({})e{}'.format(temp1, temp2, formatted_head, dp=dp)

  def format_unit(self, unit, power):
    symbol = self.units.get(unit, {'symbol': unit})['symbol']
    if power == 1:
      return symbol
    elif power < 0 or isinstance(power, fractions.Fraction):
      return '{}^({})'.format(symbol, power)
    else:
      return '{}^{}'.format(symbol, power)

  def copy(self):
    result = copy.deepcopy(self)
    # copy.deepcopy updates the circular reference automatically, but not
    # circular weak references
    for data in result.units.values():
      if data['expansion'] is not None:
        data['expansion'].system = weakref.ref(result)
    for data in result.constants.values():
      data['definition'].system = weakref.ref(result)
    return result

class Quantity:
  def __init__(self, value, error, units, system):
    self.value = value
    self.error = error
    self.units = units
    if isinstance(system, weakref.ref):
      self.system = system
    else:
      self.system = weakref.ref(system)

  def __pos__(self):
    return Quantity(self.value, self.error, self.units, self.system)

  def __neg__(self):
    return Quantity(-self.value, self.error, self.units, self.system)

  def __abs__(self):
    return Quantity(abs(self.value), self.error, self.units, self.system)

  def __add__(self, other):
    if isinstance(other, Quantity) and self.system is other.system:
      first, second = self.expand(), other.expand()
      if first.units == second.units:
        value = first.value + second.value
        error = math.hypot(first.error, second.error)
        return Quantity(value, error, first.units, first.system)
    elif isinstance(other, numbers.Real):
      first = self.expand()
      if not first.units:
        return Quantity(first.value + other, first.error, {}, first.system)
    return NotImplemented

  def __sub__(self, other):
    if isinstance(other, Quantity) and self.system is other.system:
      first, second = self.expand(), other.expand()
      if first.units == second.units:
        value = first.value - second.value
        error = math.hypot(first.error, second.error)
        return Quantity(value, error, first.units, first.system)
    elif isinstance(other, numbers.Real):
      first = self.expand()
      if not first.units:
        return Quantity(first.value - other, first.error, {}, first.system)
    return NotImplemented

  def __mul__(self, other):
    if isinstance(other, Quantity) and self.system is other.system:
      value = self.value * other.value
      error = math.hypot(self.error * other.value, other.error * self.value)
      units = UnitArithmetic.multiply(self.units, other.units)
      return Quantity(value, error, units, self.system)
    elif isinstance(other, numbers.Real):
      value = self.value * other
      error = abs(self.error * other)
      return Quantity(value, error, self.units, self.system)
    else:
      return NotImplemented

  def __truediv__(self, other):
    if isinstance(other, Quantity) and self.system is other.system:
      value = self.value / other.value
      error = math.hypot(self.error / other.value,
        other.error * self.value / other.value**2)
      units = UnitArithmetic.divide(self.units, other.units)
      return Quantity(value, error, units, self.system)
    elif isinstance(other, numbers.Real):
      value = self.value / other
      error = abs(self.error / other)
      return Quantity(value, error, self.units, self.system)
    else:
      return NotImplemented

  def __pow__(self, other):
    if isinstance(other, Quantity) and self.system is other.system:
      first, second = self.expand(), other.expand()
      if first.units and second.error == 0 and not second.units:
        value = first.value ** second.value
        error = value * second.value / first.value * first.error
        units = UnitArithmetic.power(first.units, second.value)
        return Quantity(value, error, units, first.system)
      elif not first.units and not second.units:
        value = first.value ** second.value
        error = value * math.hypot(
          second.value / first.value * first.error,
          math.log(first.value) * second.error)
        return Quantity(value, error, {}, first.system)
    elif isinstance(other, numbers.Real):
      value = 1 if self.value == 1 else self.value ** other
      error = abs(other * value / self.value * self.error)
      units = UnitArithmetic.power(self.units, other)
      return Quantity(value, error, units, self.system)
    return NotImplemented

  def __radd__(self, other):
    if isinstance(other, numbers.Real):
      return self + other
    else:
      return NotImplemented

  def __rsub__(self, other):
    if isinstance(other, numbers.Real):
      return -self + other
    else:
      return NotImplemented

  def __rmul__(self, other):
    if isinstance(other, numbers.Real):
      return self * other
    else:
      return NotImplemented

  def __rtruediv__(self, other):
    if isinstance(other, numbers.Real):
      return self**-1 * other
    else:
      return NotImplemented

  def __rpow__(self, other):
    if isinstance(other, numbers.Real):
      second = self.expand()
      if not second.units:
        return Quantity(other, 0, {}, second.system) ** second
    return NotImplemented

  def __eq__(self, other):
    return (isinstance(other, Quantity) and
      self.value == other.value and self.error == other.error and
      self.units == other.units and self.system is other.system)

  def __ne__(self, other):
    return not self == other

  def __hash__(self):
    return hash((self.value, self.error,
      tuple(sorted(self.units.items())), self.system))

  def almost_equals(self, other):
    if isinstance(other, Quantity) and self.system is other.system:
      first, second = self.expand(), other.expand()
      if first.units == second.units:
        return abs(first.value - second.value) <= first.error + second.error
    elif isinstance(other, numbers.Real):
      first = self.expand()
      if not first.units:
        return abs(first.value - other) < first.error
    raise TypeError('quantities are incomparable: {} and {}'
      .format(self, other))

  def __float__(self):
    first = self.expand()
    if first.error == 0 and not first.units:
      return float(first.value)
    else:
      raise TypeError('quantity has either error or units')

  def expand(self):
    if self.system is not None:
      return self.system().expand_quantity(self)
    else:
      return self

  def copy(self):
    return Quantity(self.value, self.error, self.units.copy(), self.system)

  def __repr__(self):
    kwargs = ', '.join('{}={}'.format(key, repr(self.__dict__[key]))
      for key in ['value', 'error', 'units', 'system'])
    return '{}({})'.format(self.__class__.__name__, kwargs)

  def __str__(self):
    return format(self, '2s')

  def __format__(self, format_spec):
    return self.system().format_quantity(self, format_spec)

  @staticmethod
  def make_same_system(args):
    if all(isinstance(arg, numbers.Real) for arg in args):
      return args
    if not all(isinstance(arg, (Quantity, numbers.Real)) for arg in args):
      raise TypeError('arguments are not all quantities or numbers')
    systems = [arg.system for arg in args if isinstance(arg, Quantity)]
    if not all(system is systems[0] for system in systems):
      raise TypeError('arguments do not have the same system')
    return [Quantity(arg, 0, {}, systems[0]) if isinstance(arg, numbers.Real)
      else arg for arg in args]

def wrap_unitless_function(func, *derivs):
  @functools.wraps(func)
  def wrapper(*args):
    try:
      args = Quantity.make_same_system(args)
    except TypeError:
      pass
    else:
      if isinstance(args[0], Quantity):
        args = [arg.expand() for arg in args]
        if all(not arg.units for arg in args):
          arg_values = [arg.value for arg in args]
          value = func(*arg_values)
          error = math.sqrt(sum((deriv(*arg_values) * arg.error)**2
            for arg, deriv in zip(args, derivs)))
          return Quantity(value, error, {}, args[0].system)
    return func(*args)
  return wrapper

exp = wrap_unitless_function(math.exp, math.exp)
log = wrap_unitless_function(math.log,
  lambda x, base=math.e: 1 / x / math.log(base),
  lambda x, base=math.e: -math.log(x) / base / math.log(base)**2)
log10 = wrap_unitless_function(math.log10, lambda x: 1 / x / math.log(10))
sin = wrap_unitless_function(math.sin, math.cos)
cos = wrap_unitless_function(math.cos, lambda x: -math.sin(x))
tan = wrap_unitless_function(math.tan, lambda x: math.cos(x)**-2)
asin = wrap_unitless_function(math.asin, lambda x: 1 / math.sqrt(1 - x**2))
acos = wrap_unitless_function(math.acos, lambda x: -1 / math.sqrt(1 - x**2))
atan = wrap_unitless_function(math.atan, lambda x: 1 / (1 + x**2))
atan2 = wrap_unitless_function(math.atan2,
  lambda y, x: x / (x**2 + y**2), lambda y, x: -y / (x**2 + y**2))
sinh = wrap_unitless_function(math.sinh, math.cosh)
cosh = wrap_unitless_function(math.cosh, math.sinh)
tanh = wrap_unitless_function(math.tanh, lambda x: math.cosh(x)**-2)
asinh = wrap_unitless_function(math.asinh, lambda x: 1 / math.hypot(1, x))
acosh = wrap_unitless_function(math.acosh, lambda x: 1 / math.sqrt(x**2 - 1))
atanh = wrap_unitless_function(math.atanh, lambda x: 1 / (1 - x**2))

def sqrt(x):
  return x ** fractions.Fraction(1, 2)

extended_functions = [exp, log, log10, sqrt, sin, cos, tan, asin, acos, atan,
  atan2, sinh, cosh, tanh, asinh, acosh, atanh]
