from random import randint, sample, seed
from time import time
from uuid import uuid4

from src.entity_merge import Consolidator

seed(42)

# iterative consolidation
# from https://rosettacode.org/wiki/Set_consolidation#Python
def consolidate(sets):
    setlist = [s for s in sets if s]
    for i, s1 in enumerate(setlist):
        if s1:
            for s2 in setlist[i+1:]:
                intersection = s1.intersection(s2)
                if intersection:
                    s2.update(s1)
                    s1.clear()
                    s1 = s2
    return [s for s in setlist if s]

def generate_ids(ids_pool_size):
    id_list = set([])
    while len(id_list) < ids_pool_size:
        id_list |= set([uuid4().__str__()])
    return id_list

def generate_sets(ids_pool_size, n_sets, max_set_size, _seed=42):
    seed(_seed)
    id_list = list(generate_ids(ids_pool_size=ids_pool_size))
    set_list = []
    if len(id_list) > max_set_size:
        for _ in range(n_sets):
            set_list.append(set(sample(id_list, randint(1, max_set_size))))
    else:
        set_list.append(set(id_list))
    return set_list

def verify_sets(ids_pool_size, n_sets, max_set_size):
    consolidator = Consolidator()
    id_sets = generate_sets(ids_pool_size, n_sets, max_set_size)
    for id_set in id_sets:
        consolidator.add_id_set(id_set)
    t0 = time()
    consolidator.consolidate()
    set_list1 = consolidator.as_sets()
    t1 = time()
    set_list2 = consolidate(id_sets)
    t2 = time()
    assert consolidator.n_groups == len(set_list1) == len(set_list2)
    tuple_list1 = list(set([tuple(sorted(list(_set))) for _set in set_list1]))
    tuple_list2 = list(set([tuple(sorted(list(_set))) for _set in set_list2]))
    tuple_list1.sort()
    tuple_list2.sort()
    assert len(tuple_list1) == len(set_list1) # no connections missed
    assert len(tuple_list2) == len(set_list2) # no connections missed
    assert tuple_list1 == tuple_list2 # same result two different ways
    connectednees = (consolidator.n_ids - consolidator.n_groups)/(consolidator.n_ids - 1)
    print(f"connectedness: {connectednees:.3f}")
    print(f"consolidate: {int((t1 - t0) * 1000)}ms cross_check: {int((t2 - t1) * 1000)}ms")
    print(consolidator.n_groups)
    return consolidator.n_groups

for ids_pool_size in [10**3, 10**5]:
    for n_sets in [10**3, 10**5]:
        for max_set_size in [2**1, 2**4, 2**8, 2**12]:
            print(f"{ids_pool_size} {n_sets} {max_set_size}")
            set_count = verify_sets(ids_pool_size, n_sets, max_set_size)
