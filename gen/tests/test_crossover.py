from gen.crossover import Crossover
import pytest
from dna.RotTable import RotTable
from random import randint

crossover = Crossover()
table_example = RotTable() #Default rot table
n = randint(0,len(list(table_example)))

def test_size():
    assert len(crossover.make_full_population(table_example,n)) == n + len(table_example)

def test_empty_list():
    assert crossover.make_full_population([],0) == []