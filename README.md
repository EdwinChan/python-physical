### Introduction

This Python package allows the user to perform algebraic operations on physical quantities, each of which consists of three parts: a value, an error, and units. Errors are propagated automatically in quadrature. The package also comes with a vast set of pre-defined physical constants, which makes it extremely convenient for carrying out computations on physical problems.

The package requires Python 3.3 or later.

### Getting started

For typical use, simply import `physical.<system>` in an interactive session or in a script, where `<system>` is one of `si`, `cgs`, `esu`, `emu`, and `gauss`:

    >>> from math import pi
    >>> from physical.si import *

The quantity (9.81 ± 0.01) m s⁻² can be declared explicitly as

    >>> Quantity(9.81, 0.01, {'Meter': 1, 'Second': -2}, system)
    (9.810 ± 0.010) m s^(-2)

If a quantity has no error, it is much easier to write it in the better-known form

    >>> 9.81*m/s**2
    9.81 m s^(-2)

The components of a quantity can be assessed through its members `value`, `error`, `units`, and `system`. The global variable `system` represents the unit system in use and is automatically defined when `physical.<system>` is imported.

Below is an exhaustive list of units and constants defined in the SI system:

    >>> sorted(a for a, b in globals().items() if isinstance(b, Quantity))
    ['A', 'AU', 'Bq', 'C', 'F', 'G', 'Gy', 'H', 'Hz', 'J', 'Jy', 'K', 'N', 'Ohm', 'Pa', 'R', 'Ry', 'S', 'Sv', 'T', 'Torr', 'V', 'W', 'Wb', 'a', 'a0', 'aSB', 'alpha', 'amu', 'angstrom', 'at', 'atm', 'bar', 'c', 'd', 'deg', 'e', 'eV', 'epsilon0', 'g0', 'ge', 'gmu', 'gn', 'gp', 'h', 'hbar', 'kB', 'kat', 'kg', 'lSun', 'ly', 'm', 'mEarth', 'mH', 'mHe', 'mJupiter', 'mSun', 'me', 'min', 'mn', 'mol', 'mp', 'mu0', 'muB', 'nA', 'pc', 'rEarth', 'rJupiter', 'rSun', 'rad', 's', 'sec', 'sigmaH', 'sigmaSB', 'sigmaT', 'sr']

They are likewise printed when the package is run as a script: `python3 -m physical <system>`.

Mathematical functions have been extended to take quantities with no units as input:

    >>> exp(eV / hbar * 1e-15*s)
    4.56887734 ± 0.00000034
    >>> sqrt(Quantity(2, 1, {}, system))
    1.41 ± 0.35

The package also guards against the misuse of units:

    >>> m + kg
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unsupported operand type(s) for +: 'Quantity' and 'Quantity'

### Sample calculations

We can determine the gravitational radius of the Sun:

    >>> (G * mSun / c**2).expand()
    (1.47704 ± 0.00018)e3 m

We can express the Schwarzschild radius of a typical super-massive black hole in astronomical units:

    >>> (2 * G * 1e8*mSun / c**2 / AU).expand()
    1.97467 ± 0.00024

We can compute the ionization energy of hydrogen atoms in electron volts:

    >>> (Ry / eV).expand()
    (1.36056914 ± 0.00000017)e1

We can convert room temperature, expressed as the kinetic energy of air molecules, to electron volts:

    >>> (kB * 300*K / eV).expand()
    (2.5851997 ± 0.0000024)e-2

We can find the approximate mean free path of an oxygen molecule in air, assuming they have a double bond of length 120.74 pm and a cross section the square of that length:

    >>> (101325*Pa / kB / (300*K) * (120.74e-12*m)**2).expand()**-1
    (2.8040485 ± 0.0000026)e-6 m

We can ask if the Sun floats on water:

    >>> (mSun / (4*pi/3 * rSun**3)).expand()
    1406.3720817644312 kg m^(-3)

Finally, we can check the claim from every astronomer that there are about π × 10⁷ seconds to a year:

    >>> math.log10(a / s)
    7.499103967085228

### Caveats

The variable for the unit gauss (`G`) is overridden by the gravitational constant (`G`), but the synonym abtesla (`abT`) can be used instead for the former.
