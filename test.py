import math
import re
import unittest
import urllib.error
import urllib.request

from .core import Quantity
from .define import defined_systems

si = defined_systems['si']
esu = defined_systems['esu']
emu = defined_systems['emu']
gauss = defined_systems['gauss']

class PhysicalQuantitiesTest(unittest.TestCase):
  def assert_quantity_equal(self, first, second):
    self.assertAlmostEqual(first.value, second.value)
    self.assertAlmostEqual(first.error, second.error)
    self.assertEqual(first.units, second.units)
    self.assertEqual(first.system, second.system)

  def test_sign(self):
    a = Quantity(1, 0.2, {'Kilogram': 1}, si)
    b = Quantity(-1, 0.2, {'Kilogram': 1}, si)
    self.assert_quantity_equal(+a, a)
    self.assert_quantity_equal(+b, b)
    self.assert_quantity_equal(-a, b)
    self.assert_quantity_equal(-b, a)
    self.assert_quantity_equal(abs(a), a)
    self.assert_quantity_equal(abs(b), a)

  def test_add(self):
    a = Quantity(1, 0.2, {'Newton': 1}, si)
    b = Quantity(3, 0.4, {'Kilogram': 1, 'Meter': 1, 'Second': -2}, si)
    c = Quantity(4, 1 / math.sqrt(5), {'Newton': 1}, si)
    d = Quantity(1, 0.2, {'Kilogram': 1}, si)
    self.assert_quantity_equal(a + b, c.expand())
    with self.assertRaises(TypeError): a + d
    with self.assertRaises(TypeError): a + 1

  def test_subtract(self):
    a = Quantity(1, 0.2, {'Newton': 1}, si)
    b = Quantity(3, 0.4, {'Kilogram': 1, 'Meter': 1, 'Second': -2}, si)
    c = Quantity(-2, 1 / math.sqrt(5), {'Newton': 1}, si)
    d = Quantity(1, 0.2, {'Kilogram': 1}, si)
    self.assert_quantity_equal(a - b, c.expand())
    with self.assertRaises(TypeError): a - d
    with self.assertRaises(TypeError): a - 1

  def test_multiply(self):
    a = Quantity(1, 0.2, {'Kilogram': 1}, si)
    b = Quantity(3, 0.4, {'Meter': -2}, si)
    c = Quantity(3, math.sqrt(13) / 5, {'Kilogram': 1, 'Meter': -2}, si)
    self.assert_quantity_equal(a * b, c)
    a = Quantity(1, 0.2, {'Kilogram': 1}, si) * 5
    b = Quantity(5, 1, {'Kilogram': 1}, si)
    self.assert_quantity_equal(a, b)
    a = Quantity(1, 0.2, {'Kilogram': 1}, si) * -5
    b = Quantity(-5, 1, {'Kilogram': 1}, si)
    self.assert_quantity_equal(a, b)
    a = 5 * Quantity(3, 0.4, {'Kilogram': 1}, si)
    b = Quantity(15, 2, {'Kilogram': 1}, si)
    self.assert_quantity_equal(a, b)
    a = -5 * Quantity(3, 0.4, {'Kilogram': 1}, si)
    b = Quantity(-15, 2, {'Kilogram': 1}, si)
    self.assert_quantity_equal(a, b)

  def test_divide(self):
    a = Quantity(2, 0.1, {'Kilogram': 1}, si)
    b = Quantity(4, 0.3, {'Meter': -2}, si)
    c = Quantity(0.5, math.sqrt(13) / 80,
      {'Kilogram': 1, 'Meter': 2}, si)
    self.assert_quantity_equal(a / b, c)
    a = Quantity(1, 0.2, {'Kilogram': 1}, si) / 5
    b = Quantity(0.2, 0.04, {'Kilogram': 1}, si)
    self.assert_quantity_equal(a, b)
    a = Quantity(1, 0.2, {'Kilogram': 1}, si) / -5
    b = Quantity(-0.2, 0.04, {'Kilogram': 1}, si)
    self.assert_quantity_equal(a, b)
    a = 5 / Quantity(3, 0.4, {'Kilogram': 1}, si)
    b = Quantity(5/3, 2/9, {'Kilogram': -1}, si)
    self.assert_quantity_equal(a, b)
    a = -5 / Quantity(3, 0.4, {'Kilogram': 1}, si)
    b = Quantity(-5/3, 2/9, {'Kilogram': -1}, si)
    self.assert_quantity_equal(a, b)

  def test_power(self):
    a = Quantity(3, 0.4, {'Kilogram': 1, 'Meter': 1}, si) ** 5
    b = Quantity(243, 162, {'Kilogram': 5, 'Meter': 5}, si)
    self.assert_quantity_equal(a, b)

  def test_almost_equals(self):
    a = Quantity(1, 0.5, {'Kilogram': 1}, si)
    b = Quantity(2, 0.7, {'Kilogram': 1}, si)
    c = Quantity(3, 0.9, {'Kilogram': 1}, si)
    d = Quantity(1, 0.5, {'Meter': 1}, si)
    e = Quantity(1, 0.5, {}, si)
    f = Quantity(2, 0.7, {}, si)
    self.assertTrue(a.almost_equals(b))
    self.assertFalse(a.almost_equals(c))
    self.assertRaises(TypeError, a.almost_equals, d)
    for x in [a, b, c, d]:
      self.assertRaises(TypeError, x.almost_equals, 1)
    self.assertTrue(e.almost_equals(1))
    self.assertTrue(f.almost_equals(2))
    self.assertFalse(e.almost_equals(2))
    self.assertFalse(f.almost_equals(1))
    self.assertTrue(e.almost_equals(f))

  def test_float(self):
    a = Quantity(1, 0, {'Second': 1, 'Hertz': 1}, si)
    b = Quantity(365.25 * 86400, 0, {'Second': 1, 'JulianYear': -1}, si)
    self.assertEqual(math.cos(a), math.cos(1))
    self.assertEqual(math.cos(b), math.cos(1))

  def test_expand(self):
    # Lorentz force
    a = Quantity(1, 0,
      {'Coulomb': 1, 'Meter': 1, 'Second': -1, 'Tesla': 1}, si)
    b = Quantity(1, 0, {'Newton': 1}, si)
    self.assert_quantity_equal(a.expand(), b.expand())
    # Faraday's law
    a = Quantity(1, 0, {'Weber': 1, 'Second': -1}, si)
    b = Quantity(1, 0, {'Volt': 1}, si)
    self.assert_quantity_equal(a.expand(), b.expand())
    # torque of a motor
    a = Quantity(1, 0, {'Ampere': 1, 'Tesla': 1, 'Meter': 2}, si)
    b = Quantity(1, 0, {'Newton': 1, 'Meter': 1}, si)
    self.assert_quantity_equal(a.expand(), b.expand())
    # resonance frequency of an RLC circuit
    a = Quantity(1, 0, {'Henry': -1/2, 'Farad': -1/2}, si)
    b = Quantity(1, 0, {'Hertz': 1}, si)
    self.assert_quantity_equal(a.expand(), b.expand())

  def test_simple_constants(self):
    for system in defined_systems.values():
      a = Quantity(13.6, 0,
        {'ElectronVolt': 1, 'RydbergEnergy': -1}, system).expand()
      self.assertAlmostEqual(a.value, 1, places=3)
      self.assertEqual(a.units, {})
      a = system.get_constant('FineStructureConstant').expand() * 137
      self.assertAlmostEqual(a.value, 1, places=3)
      self.assertEqual(a.units, {})

  def test_electromagnetic_constants(self):
    from . import si, esu, emu, gauss
    a = (si.e**2 / si.a0 / (4*math.pi*si.epsilon0) / (1e-7*si.J)).expand()
    b = (esu.e**2 / esu.a0 / esu.erg).expand()
    c = (emu.e**2 / emu.a0 * emu.c**2 / emu.erg).expand()
    d = (gauss.e**2 / gauss.a0 / gauss.erg).expand()
    self.assertAlmostEqual(a.value * 1e11, b.value * 1e11)
    self.assertAlmostEqual(a.value * 1e11, c.value * 1e11)
    self.assertAlmostEqual(a.value * 1e11, d.value * 1e11)
    a = (si.muB**2 / si.a0**3 * si.mu0 / (1e-7*si.J)).expand()
    b = (esu.muB**2 / esu.a0**3 / esu.c**2 / esu.erg).expand()
    c = (emu.muB**2 / emu.a0**3 / emu.erg).expand()
    d = (gauss.muB**2 / gauss.a0**3 / gauss.erg).expand()
    self.assertAlmostEqual(a.value * 1e3, b.value * 1e3)
    self.assertAlmostEqual(a.value * 1e3, c.value * 1e3)
    self.assertAlmostEqual(a.value * 1e3, d.value * 1e3)

  def test_codata(self):
    url = 'http://physics.nist.gov/cuu/Constants/Table/allascii.txt'

    units = {
      'AtomicMassUnit':        'unified atomic mass unit'}
    constants = {
      'AvogadroConstant':      'Avogadro constant',
      'ElectronGFactor':       'electron g factor',
      'ProtonGFactor':         'proton g factor',
      'NeutronGFactor':        'neutron g factor',
      'MuonGFactor':           'muon g factor',
      'LightSpeed':            'speed of light in vacuum',
      'ElementaryCharge':      'atomic unit of charge',
      'PlanckConstant':        'Planck constant',
      'BoltzmannConstant':     'Boltzmann constant',
      'GravitationalConstant': 'Newtonian constant of gravitation',
      'VacuumPermeability':    'vacuum mag. permeability',
      'ElectronMass':          'electron mass',
      'ProtonMass':            'proton mass',
      'NeutronMass':           'neutron mass',
      'MuonMass':              'muon mass'}

    try:
      response = urllib.request.urlopen(url)
    except urllib.error.URLError:
      raise ValueError('Cannot download data.')

    data = iter(response.read().decode('ascii').rstrip('\n').split('\n'))
    while not next(data).startswith('--'):
      pass
    data = (re.split(' {2,}', x) for x in data)
    def parse_value(x):
      return float(x.replace(' ', '').replace('...', ''))
    def parse_error(x):
      return 0 if x == '(exact)' else float(x.replace(' ', ''))
    data = {x: (parse_value(y), parse_error(z)) for x, y, z, *_ in data}

    for local_name, codata_name in units.items():
      quantity = Quantity(1, 0, {local_name: 1}, si).expand()
      x, y = data[codata_name]
      assert math.isclose(quantity.value, x)
      assert math.isclose(quantity.error, y)
    for local_name, codata_name in constants.items():
      quantity = si.get_constant(local_name).expand()
      x, y = data[codata_name]
      assert math.isclose(quantity.value, x)
      assert math.isclose(quantity.error, y)

if __name__ == '__main__':
  unittest.main()
