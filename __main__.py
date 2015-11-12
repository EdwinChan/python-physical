import argparse
import sys

from .define import defined_systems

def print_units(system):
  if system.units:
    data = [[data['symbol'], data['expansion']]
      for data in system.units.values()]
    width = max(len(item[0]) for item in data)
    for item in sorted(data):
      print(('  {:{width}}  {}').format(*item, width=width))

def print_constants(system):
  if system.constants:
    data = [[data['symbol'], data['definition']]
      for data in system.constants.values()]
    width = max(len(item[0]) for item in data)
    for item in sorted(data):
      print(('  {:{width}}  {}').format(*item, width=width))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='Show all defined units and constants.')
  parser.add_argument('system', choices=defined_systems, nargs='?',
    default='si', help='unit system')
  parser.add_argument('--test', action='store_true',
    help='run unit tests')

  args = parser.parse_args()

  if not args.test:
    system = defined_systems[args.system]
    print('Available units:')
    print_units(system)
    print('Available constants:')
    print_constants(system)
  else:
    import unittest
    from .test import PhysicalQuantitiesTest
    unittest.TextTestRunner().run(unittest.makeSuite(PhysicalQuantitiesTest))
