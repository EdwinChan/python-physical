import argparse
import unittest

from . import test
from .define import defined_systems

def print_units(system):
  if system.units:
    data = [
      [data['symbol'], data['expansion']]
      for data in system.units.values()]
    width = max(len(symbol) for symbol, _ in data)
    for item in sorted(data):
      print(('  {:{width}}  {}').format(*item, width=width))

def print_constants(system):
  if system.constants:
    data = [
      [data['symbol'], data['definition']]
      for data in system.constants.values()]
    width = max(len(symbol) for symbol, _ in data)
    for item in sorted(data):
      print(('  {:{width}}  {}').format(*item, width=width))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='Perform algebraic operations on physical quantities.')
  subparsers = parser.add_subparsers(dest='mode', required=True)

  list_subparser = subparsers.add_parser(
    'list',
    help='list units and constants',
    description='List all defined units and constants.')
  list_subparser.add_argument(
    'system', nargs='?', choices=defined_systems,
    default=next(iter(defined_systems)),
    help='unit system')

  test_subparser = subparsers.add_parser(
    'test',
    help='run unit tests',
    description='Run unit tests.')

  args = parser.parse_args()

  if args.mode == 'list':
    system = defined_systems[args.system]
    print('Available units:')
    print_units(system)
    print('Available constants:')
    print_constants(system)
  elif args.mode == 'test':
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()
    runner.run(loader.loadTestsFromModule(test))
