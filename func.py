import fractions
import functools
import math

from .core import Quantity

def sqrt(x):
  return x ** fractions.Fraction(1, 2)

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

exp = wrap_unitless_function(math.exp,
  math.exp)
expm1 = wrap_unitless_function(math.expm1,
  math.exp)
log = wrap_unitless_function(math.log,
  lambda x, base=math.e: 1 / x / math.log(base),
  lambda x, base=math.e: -math.log(x) / base / math.log(base)**2)
log1p = wrap_unitless_function(math.log1p,
  lambda x, base=math.e: 1 / x)
log2 = wrap_unitless_function(math.log2,
  lambda x: 1 / x / math.log(2))
log10 = wrap_unitless_function(math.log10,
  lambda x: 1 / x / math.log(10))
sin = wrap_unitless_function(math.sin,
  math.cos)
cos = wrap_unitless_function(math.cos,
  lambda x: -math.sin(x))
tan = wrap_unitless_function(math.tan,
  lambda x: math.cos(x)**-2)
asin = wrap_unitless_function(math.asin,
  lambda x: 1 / math.sqrt(1 - x**2))
acos = wrap_unitless_function(math.acos,
  lambda x: -1 / math.sqrt(1 - x**2))
atan = wrap_unitless_function(math.atan,
  lambda x: 1 / (1 + x**2))
atan2 = wrap_unitless_function(math.atan2,
  lambda y, x: x / (x**2 + y**2),
  lambda y, x: -y / (x**2 + y**2))
sinh = wrap_unitless_function(math.sinh,
  math.cosh)
cosh = wrap_unitless_function(math.cosh,
  math.sinh)
tanh = wrap_unitless_function(math.tanh,
  lambda x: math.cosh(x)**-2)
asinh = wrap_unitless_function(math.asinh,
  lambda x: 1 / math.hypot(1, x))
acosh = wrap_unitless_function(math.acosh,
  lambda x: 1 / math.sqrt(x**2 - 1))
atanh = wrap_unitless_function(math.atanh,
  lambda x: 1 / (1 - x**2))

extended_functions = [sqrt, exp, expm1, log, log1p, log2, log10, sin, cos, tan,
  asin, acos, atan, atan2, sinh, cosh, tanh, asinh, acosh, atanh]
