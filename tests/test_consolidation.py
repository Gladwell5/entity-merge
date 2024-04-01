from uuid import uuid4
from time import time
from random import seed, sample, randint

from src.consolidation import Consolidator

seed(42)

def cross_check(id_sets):
    pool = set(map(frozenset, id_sets))
    groups = []
    while pool:
        groups.append(set(pool.pop()))
        while True:
            for candidate in pool:
                if groups[-1] & candidate:
                    groups[-1] |= candidate
                    pool.remove(candidate)
                    break
            else:
                break
    return groups

def generate_ids(ids_pool_size):
    id_list = set([])
    while len(id_list) < ids_pool_size:
        id_list |= set([uuid4().__str__()])
    return id_list

def generate_sets(ids_pool_size, n_sets, max_set_size, _seed=42):
    seed(_seed)
    id_list = list(generate_ids(ids_pool_size=ids_pool_size))
    set_list = []
    for _ in range(n_sets):
        set_list.append(set(sample(id_list, randint(2, max_set_size))))
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
    set_list2 = cross_check(id_sets)
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
    print(f"connectedness: {connectednees}")
    print(f"consolidate: {int((t1 - t0) * 1000)}ms cross_check: {int((t2 - t1) * 1000)}ms")
    return len(tuple_list1) # n consolidated sets

def test_case1():
    n_sets = verify_sets(10, 10**2, 2)
    assert n_sets == 1

def test_case2():
    n_sets = verify_sets(10**5, 10**2, 2)
    assert n_sets == 100

def test_case3():
    n_sets = verify_sets(10**3, 10**4, 2)
    assert n_sets == 1

def test_case4():
    n_sets = verify_sets(10**5, 10**4, 2)
    assert n_sets == 8135

def test_case5():
    n_sets = verify_sets(10**3, 10**2, 32)
    assert n_sets == 1

def test_case6():
    n_sets = verify_sets(10**5, 10**2, 32)
    assert n_sets == 86

def test_case7():
    n_sets = verify_sets(10**6, 10**3, 32)
    assert n_sets == 882

test_case1()
test_case2()
test_case3()
test_case4()
test_case5()
test_case6()
test_case7()
