
import io
import pytest

import logging
from logging import debug
import re

import re
import collections

def parse(fp):
    seq = []
    p = re.compile(r'^(.+) \(contains (.+)\)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        ingredients = set(m.groups()[0].split(' '))
        allergens = set(m.groups()[1].split(', '))
        seq.append( (ingredients,allergens))

    return seq

def main( fp):
    pairs = parse(fp)
    print(pairs)

    # allergen => ingredient
    a2i = {}
    
    # ingredient => Option[allergen]
    i2a = {}


    original_pairs = pairs[:]

    for _ in range(10):

        singletons = {}

        for pair in pairs:
            ingredients, allergens = pair

            if len(allergens) == 1:
                allergen = list(allergens)[0]
                if allergen not in singletons:
                    singletons[allergen] = ingredients
                else:
                    singletons[allergen] = singletons[allergen].intersection(ingredients)


        for i in range(len(pairs)):
            for j in range(i):
                ingredients0, allergens0 = pairs[j]
                ingredients1, allergens1 = pairs[i]

                common_ingredients = ingredients0.intersection(ingredients1)
                common_allergens = allergens0.intersection(allergens1)

                if len(common_allergens) == 1:
                    allergen = list(common_allergens)[0]
                    if allergen not in singletons:
                        singletons[allergen] = common_ingredients
                    else:
                        singletons[allergen] = singletons[allergen].intersection(common_ingredients)
                    

        for (k,v) in singletons.items():
            if len(v) == 1:
                a2i[k] = list(v)[0]


        found_ingredients = set()
        found_allergens = set()
        for (k,v) in a2i.items():
            found_allergens.add(k)
            found_ingredients.add(v)

        print('SMB:', found_ingredients, found_allergens)

        new_pairs = []
        changed = False
        for pair in pairs:
            ingredients, allergens = pair
            if len(ingredients.intersection(found_ingredients)) > 0 or \
               len(allergens.intersection(found_ingredients)) > 0:
                changed = True

            new_pairs.append( (ingredients.difference(found_ingredients),
                               allergens.difference(found_allergens)))

        if not changed:
            break

        pairs = new_pairs
    
            
    allergen_free_ingredients = set()
    for pair in pairs:
        ingredients, allergens = pair

        if len(allergens) == 0:
            allergen_free_ingredients = allergen_free_ingredients.union(ingredients)

    #print('original_pairs:', original_pairs)
    #print('new_pairs:', pairs)

    
    all_allergens = set()
    sum = 0
    for pair in original_pairs:
        ingredients, allergens = pair        
        sum += len(ingredients.intersection(allergen_free_ingredients))
        all_allergens = all_allergens.union(allergens)

    print('allergen_free_ingredients',allergen_free_ingredients)
    print( 'mapping', a2i)
    print('number of allergens', len(all_allergens), len(a2i))

    canonical = ''
    first = True
    for (k,v) in sorted(a2i.items()):
        if not first:
            canonical += ','
        first = False
        canonical += v


    return sum, canonical

def test_A():
    with open( "data0", "rt") as fp:
        assert (5, 'mxmxvkd,sqjhc,fvjkl') == main(fp)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
