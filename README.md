### Introduction

This Python package allows the user to perform algebraic operations on physical quantities, each of which consists of three parts: a value, an error, and units. Errors are propagated automatically in quadrature. The package also comes with a vast set of pre-defined physical constants, which makes it extremely convenient for carrying out computations on physical problems.

The package requires Python 3.3 or later.

### Getting started

For typical use, simply import `physical.<system>` in an interactive session or in a script, where `<system>` is one of `si`, `cgs`, `esu`, `emu`, and `gauss`:

```python
>>> from math import pi
>>> from physical.si import *
```

The quantity (9.81 ± 0.01) m s⁻² can be declared explicitly as

```python
>>> Quantity(9.81, 0.01, {'Meter': 1, 'Second': -2}, system)
(9.810 ± 0.010) m s^(-2)
```

If a quantity has no error, it is much easier to write it in the better-known form

```python
>>> 9.81*m/s**2
9.81 m s^(-2)
```

The components of a quantity can be assessed through its members `value`, `error`, `units`, and `system`. The global variable `system` represents the unit system in use and is automatically defined when `physical.<system>` is imported.

Below is an exhaustive list of units and constants defined in the SI system:

```python
>>> sorted(a for a, b in globals().items() if isinstance(b, Quantity))
['AU', 'Ba', 'Bq', 'G', 'Gal', 'Gy', 'Hz', 'Jy', 'K', 'LSun', 'MEarth', 'MJupiter', 'MSun', 'NA', 'P', 'R', 'Ry', 'St', 'Sv', 'Torr', 'a', 'a0', 'aSB', 'alpha', 'amu', 'angstrom', 'arcmin', 'arcsec', 'at', 'atm', 'bar', 'c', 'cm', 'd', 'deg', 'dyn', 'eV', 'erg', 'g', 'g0', 'ge', 'gmu', 'gn', 'gp', 'h', 'hbar', 'kB', 'kat', 'lambdae', 'ly', 'mH', 'mHe', 'me', 'mmu', 'mn', 'mol', 'mp', 'pc', 'rEarth', 'rJupiter', 'rSun', 'rad', 're', 's', 'sigmaH', 'sigmaSB', 'sigmaT', 'sr']
```

They are likewise printed when the package is run as a script: `python3 -m physical <system>`.

Mathematical functions have been extended to take quantities with no units as input:

```python
>>> exp(eV / (hbar*1e15*Hz))
4.568877028379119
>>> sqrt(Quantity(2, 1, {}, system))
1.41 ± 0.35
```

The package also guards against the misuse of units:

```python
>>> m + kg
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'Quantity' and 'Quantity'
```

### Sample calculations

We can determine the gravitational radius of the Sun:

```python
>>> (G*MSun/c**2).expand()
(1.476625 ± 0.000047)e+03 m
```

We can express the Schwarzschild radius of a typical super-massive black hole in astronomical units:

```python
>>> (2*G*1e8*MSun/c**2 / AU).expand()
1.974126 ± 0.000063
```

We can compute the ionization energy of hydrogen atoms in electron volts:

```python
>>> (Ry / eV).expand()
(1.36056931229 ± 0.00000000059)e+01
```

We can convert room temperature, expressed as the kinetic energy of air molecules, to electron volts:

```python
>>> (kB*300*K / eV).expand()
0.025851999786435535
```

We can find the approximate mean free path of an oxygen molecule in air, assuming they have a double bond of length 120.74 pm and a cross section the square of that length:

```python
>>> (101325*Pa/(kB*300*K) * (120.74e-12*m)**2).expand()**-1
2.8040488928816928e-06 m
```

We can ask if the Sun floats on water:

```python
>>> (MSun / (4*pi/3*rSun**3)).expand()
(1.409780 ± 0.000032)e+03 kg m^(-3)
```

Finally, we can check the claim from every astronomer that there are about π × 10⁷ seconds to a year:

```python
>>> log10(a / s)
7.499103967085228
```

### Caveats

The variable for the unit gauss (`G`) is overridden by the gravitational constant (`G`), but the synonym abtesla (`abT`) can be used instead for the former.
