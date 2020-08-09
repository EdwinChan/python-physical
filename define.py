# sources:
#   2018 CODATA recommended values
#   IUPAC, CIAAW, "Atomic weights of the elements 2013"
#   IAU 2012 resolution B2
#   IAU 2015 resolution B3

import fractions
import math
import weakref

from .core import UnitSystem, Quantity

half = fractions.Fraction(1, 2)

shared_system = UnitSystem()

shared_system.add_unit('Second', 's')
shared_system.add_unit('Kelvin', 'K')
shared_system.add_unit('Mole', 'mol')
shared_system.add_unit('Radian', 'rad')
shared_system.add_unit('Steradian', 'sr')

shared_system.add_unit('Becquerel', 'Bq',
  Quantity(1, 0, {'Second': -1}, shared_system))
shared_system.add_unit('Hertz', 'Hz',
  Quantity(1, 0, {'Second': -1}, shared_system))
shared_system.add_unit('Katal', 'kat',
  Quantity(1, 0, {'Mole': 1, 'Second': -1}, shared_system))
shared_system.add_unit('Day', 'd',
  Quantity(86400, 0, {'Second': 1}, shared_system))
shared_system.add_unit('JulianYear', 'a',
  Quantity(365.25, 0, {'Day': 1}, shared_system))
shared_system.add_unit('Degree', '\xb0',
  Quantity(math.pi / 180, 0, {'Radian': 1}, shared_system))
shared_system.add_unit('ArcMinute', "'",
  Quantity(fractions.Fraction(1, 60), 0, {'Degree': 1}, shared_system))
shared_system.add_unit('ArcSecond', '"',
  Quantity(fractions.Fraction(1, 60), 0, {'ArcMinute': 1}, shared_system))

shared_system.add_constant('AvogadroConstant', 'nA',
  Quantity(6.02214076e23, 0, {'Mole': -1}, shared_system))
shared_system.add_constant('ElectronGFactor', 'ge',
  Quantity(-2.00231930436256, 3.5e-13, {}, shared_system))
shared_system.add_constant('ProtonGFactor', 'gp',
  Quantity(5.5856946893, 1.6e-9, {}, shared_system))
shared_system.add_constant('NeutronGFactor', 'gn',
  Quantity(-3.82608545, 9e-7, {}, shared_system))
shared_system.add_constant('MuonGFactor', 'g\u03bc',
  Quantity(-2.0023318418, 1.3e-9, {}, shared_system))

si_system = shared_system.copy()

si_system.add_unit('Meter', 'm')
si_system.add_unit('Kilogram', 'kg')
si_system.add_unit('Newton', 'N',
  Quantity(1, 0, {'Kilogram': 1, 'Meter': 1, 'Second': -2}, si_system))
si_system.add_unit('Pascal', 'Pa',
  Quantity(1, 0, {'Newton': 1, 'Meter': -2}, si_system))
si_system.add_unit('Joule', 'J',
  Quantity(1, 0, {'Newton': 1, 'Meter': 1}, si_system))
si_system.add_unit('Watt', 'W',
  Quantity(1, 0, {'Joule': 1, 'Second': -1}, si_system))

si_system.add_unit('Ampere', 'A')
si_system.add_unit('Coulomb', 'C',
  Quantity(1, 0, {'Ampere': 1, 'Second': 1}, si_system))
si_system.add_unit('Volt', 'V',
  Quantity(1, 0, {'Joule': 1, 'Coulomb': -1}, si_system))
si_system.add_unit('Farad', 'F',
  Quantity(1, 0, {'Coulomb': 1, 'Volt': -1}, si_system))
si_system.add_unit('Ohm', '\u2126',
  Quantity(1, 0, {'Volt': 1, 'Ampere': -1}, si_system))
si_system.add_unit('Siemens', 'S',
  Quantity(1, 0, {'Ampere': 1, 'Volt': -1}, si_system))
si_system.add_unit('Weber', 'Wb',
  Quantity(1, 0, {'Volt': 1, 'Second': 1}, si_system))
si_system.add_unit('Tesla', 'T',
  Quantity(1, 0, {'Weber': 1, 'Meter': -2}, si_system))
si_system.add_unit('Henry', 'H',
  Quantity(1, 0, {'Weber': 1, 'Ampere': -1}, si_system))

si_specific_units = si_system.units.keys() - shared_system.units.keys()

si_system.add_constant('LightSpeed', 'c',
  Quantity(299792458, 0, {'Meter': 1, 'Second': -1}, si_system))
si_system.add_constant('ElementaryCharge', 'e',
  Quantity(1.602176634e-19, 0, {'Coulomb': 1}, si_system))
si_system.add_constant('PlanckConstant', 'h',
  Quantity(6.62607015e-34, 0, {'Joule': 1, 'Second': 1}, si_system))
si_system.add_constant('BoltzmannConstant', 'kB',
  Quantity(1.380649e-23, 0, {'Joule': 1, 'Kelvin': -1}, si_system))

si_system.add_constant('GravitationalConstant', 'G',
  Quantity(6.6743e-11, 1.5e-15, {
    'Newton': 1, 'Kilogram': -2, 'Meter': 2}, si_system))
si_system.add_constant('VacuumPermeability', '\u03bc0',
  Quantity(1.25663706212e-6, 1.9e-16, {'Newton': 1, 'Ampere': -2}, si_system))
si_system.add_constant('ElectronMass', 'me',
  Quantity(9.1093837015e-31, 2.8e-40, {'Kilogram': 1}, si_system))
si_system.add_constant('ProtonMass', 'mp',
  Quantity(1.67262192369e-27, 5.1e-37, {'Kilogram': 1}, si_system))
si_system.add_constant('NeutronMass', 'mn',
  Quantity(1.67492749804e-27, 9.5e-37, {'Kilogram': 1}, si_system))
si_system.add_constant('MuonMass', 'm\u03bc',
  Quantity(1.883531627e-28, 4.2e-36, {'Kilogram': 1}, si_system))

si_system.add_constant('VacuumPermittivity', '\u03b50',
  si_system.get_constant({'LightSpeed': -2, 'VacuumPermeability': -1}))
si_system.add_constant('ReducedPlanckConstant', '\u0127',
  1/(2*math.pi) * si_system.get_constant('PlanckConstant'))
si_system.add_constant('FineStructureConstant', '\u03b1',
  1/2 * si_system.get_constant({
    'VacuumPermittivity': -1, 'ElementaryCharge': 2,
    'PlanckConstant': -1, 'LightSpeed': -1}))
si_system.add_constant('ElectronClassicalRadius', 're',
  1/(4*math.pi) * si_system.get_constant({
    'VacuumPermittivity': -1, 'ElementaryCharge': 2,
    'ElectronMass': -1, 'LightSpeed': -2}))
si_system.add_constant('ElectronComptonWavelength', '\u03bbe',
  si_system.get_constant({
    'PlanckConstant': 1, 'ElectronMass': -1, 'LightSpeed': -1}))
si_system.add_constant('BohrRadius', 'a0',
  si_system.get_constant({
    'FineStructureConstant': -1, 'ReducedPlanckConstant': 1,
    'ElectronMass': -1, 'LightSpeed': -1}))
si_system.add_constant('BohrMagneton', '\u03bcB',
  1/(4*math.pi) * si_system.get_constant({
    'ElementaryCharge': 1, 'PlanckConstant': 1, 'ElectronMass': -1}))
si_system.add_constant('ThomsonCrossSection', '\u03c3T',
  8/3 * math.pi * si_system.get_constant({
    'FineStructureConstant': 2, 'ReducedPlanckConstant': 2,
    'ElectronMass': -2, 'LightSpeed': -2}))
si_system.add_constant('HydrogenIonizationThresholdCrossSection', '\u03c3H',
  512/3 * math.pi**2 / math.exp(4) * si_system.get_constant({
    'FineStructureConstant': 1, 'BohrRadius': 2}))
si_system.add_constant('StefanBoltzmannConstant', '\u03c3SB',
  2/15 * math.pi**5 * si_system.get_constant({
    'BoltzmannConstant': 4, 'PlanckConstant': -3, 'LightSpeed': -2}))
si_system.add_constant('RadiationConstant', 'aSB',
  4 * si_system.get_constant({'StefanBoltzmannConstant': 1, 'LightSpeed': -1}))
si_system.add_constant('MolarGasConstant', 'R',
  si_system.get_constant({'AvogadroConstant': 1, 'BoltzmannConstant': 1}))

si_system.add_unit('AtomicMassUnit', 'amu',
  Quantity(1.6605390666e-27, 5e-37, {'Kilogram': 1}, si_system))
si_system.add_constant('HydrogenMass', 'mH',
  Quantity(1.007975, 1.35e-4, {'AtomicMassUnit': 1}, si_system))
si_system.add_constant('HeliumMass', 'mHe',
  Quantity(4.002602, 2e-6, {'AtomicMassUnit': 1}, si_system))

si_system.add_constant('SunMass', 'mSun',
  Quantity(1.3271244e20, 0, {'Meter': 3, 'Second': -2}, si_system) /
  si_system.get_constant('GravitationalConstant'))
si_system.add_constant('SunRadius', 'rSun',
  Quantity(6.957e8, 0, {'Meter': 1}, si_system))
si_system.add_constant('SunLuminosity', 'lSun',
  Quantity(3.828e26, 0, {'Watt': 1}, si_system))
si_system.add_constant('EarthMass', 'mEarth',
  Quantity(3.986004e14, 0, {'Meter': 3, 'Second': -2}, si_system) /
  si_system.get_constant('GravitationalConstant'))
si_system.add_constant('EarthEquatorialRadius', 'rEarth',
  Quantity(6.3781e6, 0, {'Meter': 1}, si_system))
si_system.add_constant('JupiterMass', 'mJupiter',
  Quantity(1.2668653e17, 0, {'Meter': 3, 'Second': -2}, si_system) /
  si_system.get_constant('GravitationalConstant'))
si_system.add_constant('JupiterEquatorialRadius', 'rJupiter',
  Quantity(7.1492e7, 0, {'Meter': 1}, si_system))

si_system.add_unit('\xc5ngstr\xf6m', '\u212b',
  Quantity(fractions.Fraction(1, 10**10), 0, {
    'Meter': 1}, si_system))
si_system.add_constant('StandardGravity', 'g0',
  Quantity(fractions.Fraction(980665, 10**5), 0, {
    'Newton': 1, 'Kilogram': -1}, si_system))

si_system.add_unit('StandardAtmosphere', 'atm',
  Quantity(101325, 0, {'Pascal': 1}, si_system))
si_system.add_unit('TechnicalAtmosphere', 'at',
  Quantity(fractions.Fraction(980665, 10), 0, {'Pascal': 1}, si_system))
si_system.add_unit('Bar', 'bar',
  Quantity(100000, 0, {'Pascal': 1}, si_system))
si_system.add_unit('Torr', 'Torr',
  Quantity(fractions.Fraction(1, 760), 0, {
    'StandardAtmosphere': 1}, si_system))

si_system.add_unit('ElectronVolt', 'eV', (
  si_system.get_constant('ElementaryCharge') *
  Quantity(1, 0, {'Volt': 1}, si_system)))
si_system.add_unit('RydbergEnergy', 'Ry',
  1/8 * si_system.get_constant({
    'VacuumPermittivity': -2, 'PlanckConstant': -2,
    'ElementaryCharge': 4, 'ElectronMass': 1}))

si_system.add_unit('Gray', 'Gy',
  Quantity(1, 0, {'Joule': 1, 'Kilogram': -1}, si_system))
si_system.add_unit('Sievert', 'Sv',
  Quantity(1, 0, {'Joule': 1, 'Kilogram': -1}, si_system))

si_system.add_unit('AstronomicalUnit', 'AU',
  Quantity(149597870700, 0, {'Meter': 1}, si_system))
si_system.add_unit('Parsec', 'pc',
  Quantity(180 * 3600 / math.pi, 0, {'AstronomicalUnit': 1}, si_system))
si_system.add_unit('LightYear', 'ly', (
  si_system.get_constant('LightSpeed') *
  Quantity(1, 0, {'JulianYear': 1}, si_system)))
si_system.add_unit('Jansky', 'Jy',
  Quantity(fractions.Fraction(1, 10**26), 0, {
    'Watt': 1, 'Hertz': -1, 'Meter': -2}, si_system))

cgs_system = shared_system.copy()

cgs_system.add_unit('Centimeter', 'cm')
cgs_system.add_unit('Gram', 'g')
cgs_system.add_unit('Galileo', 'Gal',
  Quantity(1, 0, {'Centimeter': 1, 'Second': -2}, cgs_system))
cgs_system.add_unit('Dyne', 'dyn',
  Quantity(1, 0, {'Gram': 1, 'Galileo': 1}, cgs_system))
cgs_system.add_unit('Erg', 'erg',
  Quantity(1, 0, {'Dyne': 1, 'Centimeter': 1}, cgs_system))
cgs_system.add_unit('Barye', 'Ba',
  Quantity(1, 0, {'Dyne': 1, 'Centimeter': -2}, cgs_system))
cgs_system.add_unit('Poise', 'P',
  Quantity(1, 0, {'Gram': 1, 'Centimeter': -1, 'Second': -1}, cgs_system))
cgs_system.add_unit('Stokes', 'St',
  Quantity(1, 0, {'Centimeter': 2, 'Second': -1}, cgs_system))

esu_system = cgs_system.copy()
emu_system = cgs_system.copy()
gauss_system = cgs_system.copy()

esu_system.add_unit('Statcoulomb', 'statC',
  Quantity(1, 0, {'Dyne': half, 'Centimeter': 1}, esu_system))
esu_system.add_unit('Statampere', 'statA',
  Quantity(1, 0, {'Statcoulomb': 1, 'Second': -1}, esu_system))
esu_system.add_unit('Statvolt', 'statV',
  Quantity(1, 0, {'Erg': 1, 'Statcoulomb': -1}, esu_system))
esu_system.add_unit('Statfarad', 'statF',
  Quantity(1, 0, {'Statcoulomb': 1, 'Statvolt': -1}, esu_system))
esu_system.add_unit('Statohm', 'stat\u2126',
  Quantity(1, 0, {'Statvolt': 1, 'Statampere': -1}, esu_system))
esu_system.add_unit('Statsiemens', 'statS',
  Quantity(1, 0, {'Statampere': 1, 'Statvolt': -1}, esu_system))
esu_system.add_unit('Statweber', 'statWb',
  Quantity(1, 0, {'Statvolt': 1, 'Second': 1}, esu_system))
esu_system.add_unit('Stattesla', 'statT',
  Quantity(1, 0, {'Statweber': 1, 'Centimeter': -2}, esu_system))
esu_system.add_unit('Stathenry', 'statH',
  Quantity(1, 0, {'Statweber': 1, 'Statampere': -1}, esu_system))
esu_system.add_unit('Franklin', 'Fr',
  Quantity(1, 0, {'Statcoulomb': 1}, esu_system))
esu_system.add_unit('Debye', 'D',
  Quantity(fractions.Fraction(1, 10**18), 0, {
    'Statcoulomb': 1, 'Centimeter': 1}, esu_system))

emu_system.add_unit('Abampere', 'abA',
  Quantity(1, 0, {'Dyne': half}, emu_system))
emu_system.add_unit('Abcoulomb', 'abC',
  Quantity(1, 0, {'Abampere': 1, 'Second': 1}, emu_system))
emu_system.add_unit('Abvolt', 'abV',
  Quantity(1, 0, {'Erg': 1, 'Abcoulomb': -1}, emu_system))
emu_system.add_unit('Abfarad', 'abF',
  Quantity(1, 0, {'Abcoulomb': 1, 'Abvolt': -1}, emu_system))
emu_system.add_unit('Abohm', 'ab\u2126',
  Quantity(1, 0, {'Abvolt': 1, 'Abampere': -1}, emu_system))
emu_system.add_unit('Absiemens', 'abS',
  Quantity(1, 0, {'Abampere': 1, 'Abvolt': -1}, emu_system))
emu_system.add_unit('Abweber', 'abWb',
  Quantity(1, 0, {'Abvolt': 1, 'Second': 1}, emu_system))
emu_system.add_unit('Abtesla', 'abT',
  Quantity(1, 0, {'Abweber': 1, 'Centimeter': -2}, emu_system))
emu_system.add_unit('Abhenry', 'abH',
  Quantity(1, 0, {'Abweber': 1, 'Abampere': -1}, emu_system))
emu_system.add_unit('Biot', 'Bi',
  Quantity(1, 0, {'Abampere': 1}, emu_system))
emu_system.add_unit('Gauss', 'G',
  Quantity(1, 0, {'Abtesla': 1}, emu_system))
emu_system.add_unit('Oersted', 'Oe',
  Quantity(1, 0, {'Abtesla': 1}, emu_system))
emu_system.add_unit('Gilbert', 'Gb',
  Quantity(1, 0, {'Abtesla': 1, 'Centimeter': 1}, emu_system))
emu_system.add_unit('Maxwell', 'Mx',
  Quantity(1, 0, {'Abweber': 1}, emu_system))

gauss_system.add_unit('Statcoulomb', 'statC',
  Quantity(1, 0, {'Dyne': half, 'Centimeter': 1}, gauss_system))
gauss_system.add_unit('Statampere', 'statA',
  Quantity(1, 0, {'Statcoulomb': 1, 'Second': -1}, gauss_system))
gauss_system.add_unit('Statvolt', 'statV',
  Quantity(1, 0, {'Erg': 1, 'Statcoulomb': -1}, gauss_system))
gauss_system.add_unit('Statfarad', 'statF',
  Quantity(1, 0, {'Statcoulomb': 1, 'Statvolt': -1}, gauss_system))
gauss_system.add_unit('Statohm', 'stat\u2126',
  Quantity(1, 0, {'Statvolt': 1, 'Statampere': -1}, gauss_system))
gauss_system.add_unit('Statsiemens', 'statS',
  Quantity(1, 0, {'Statampere': 1, 'Statvolt': -1}, gauss_system))
gauss_system.add_unit('Stathenry', 'statH',
  Quantity(1, 0, {'Statvolt': 1, 'Second': 1, 'Statampere': -1}, gauss_system))
gauss_system.add_unit('Abtesla', 'abT',
  Quantity(1, 0, {'Dyne': half, 'Centimeter': -1}, gauss_system))
gauss_system.add_unit('Abweber', 'abWb',
  Quantity(1, 0, {'Abtesla': 1, 'Centimeter': 2}, gauss_system))
gauss_system.add_unit('Franklin', 'Fr',
  Quantity(1, 0, {'Statcoulomb': 1}, gauss_system))
gauss_system.add_unit('Debye', 'D',
  Quantity(fractions.Fraction(1, 10**18), 0, {
    'Statcoulomb': 1, 'Centimeter': 1}, gauss_system))
gauss_system.add_unit('Gauss', 'G',
  Quantity(1, 0, {'Abtesla': 1}, gauss_system))
gauss_system.add_unit('Oersted', 'Oe',
  Quantity(1, 0, {'Abtesla': 1}, gauss_system))
gauss_system.add_unit('Gilbert', 'Gb',
  Quantity(1, 0, {'Abtesla': 1, 'Centimeter': 1}, gauss_system))
gauss_system.add_unit('Maxwell', 'Mx',
  Quantity(1, 0, {'Abweber': 1}, gauss_system))

si_to_cgs = UnitSystem()

si_to_cgs.add_unit('Meter', 'm',
  Quantity(100, 0, {'Centimeter': 1}, si_to_cgs))
si_to_cgs.add_unit('Kilogram', 'kg',
  Quantity(1000, 0, {'Gram': 1}, si_to_cgs))

si_to_esu = si_to_cgs.copy()
si_to_emu = si_to_cgs.copy()

def translate(quantity, through_system, to_system):
  result = through_system.expand_quantity(quantity.expand())
  return Quantity(result.value, result.error, result.units, to_system)

si_to_esu.add_unit('Ampere', 'A', translate(
  Quantity(1, 0, {'Ampere': 1}, si_system) /
    (4*math.pi * si_system.get_constant('VacuumPermittivity'))**half,
    si_to_cgs, si_to_esu))
si_to_emu.add_unit('Ampere', 'A', translate(
  Quantity(1, 0, {'Ampere': 1}, si_system) /
    (4*math.pi / si_system.get_constant('VacuumPermeability'))**half,
    si_to_cgs, si_to_emu))

for unit, data in si_system.units.items():
  if unit not in si_specific_units and data['expansion']:
    expansion = data['expansion'].expand()
    if 'Ampere' not in expansion.units:
      for system in [cgs_system, esu_system, emu_system, gauss_system]:
        system.add_unit(unit, data['symbol'],
          translate(expansion, si_to_cgs, system))

for constant, data in si_system.constants.items():
  definition = data['definition'].expand()
  if (definition.units.keys() <= shared_system.units.keys() and
    constant not in shared_system.constants):
    result = definition.copy()
    result.system = weakref.ref(shared_system)
    shared_system.add_constant(constant, data['symbol'], result)
  if 'Ampere' not in definition.units:
    cgs_system.add_constant(constant, data['symbol'],
      translate(definition, si_to_cgs, cgs_system))
    gauss_system.add_constant(constant, data['symbol'],
      translate(definition, si_to_cgs, gauss_system))
  if constant not in ['VacuumPermittivity', 'VacuumPermeability']:
    esu_system.add_constant(constant, data['symbol'],
      translate(definition, si_to_esu, esu_system))
    emu_system.add_constant(constant, data['symbol'],
      translate(definition, si_to_emu, emu_system))

gauss_system.add_constant('ElementaryCharge',
  si_system.constants['ElementaryCharge']['symbol'],
  translate(si_system.constants['ElementaryCharge']['definition'],
    si_to_esu, gauss_system))
gauss_system.add_constant('BohrMagneton',
  si_system.constants['BohrMagneton']['symbol'],
  translate(si_system.constants['BohrMagneton']['definition'],
    si_to_emu, gauss_system))

defined_systems = {
  'si': si_system, 'cgs': cgs_system, 'esu': esu_system, 'emu': emu_system,
  'gauss': gauss_system}
