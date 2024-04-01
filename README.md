# Description
Efficient set consolidation

Given a list of sets, consolidate sets that share at least one member.
See set consolidation - see https://rosettacode.org/wiki/Set_consolidation
This is also known as connected components in graphs.

This is (in most circumstances) a more efficient implementation of set consolidation than those on Rosetta Code and others found on Stack Overflow.

Use cases:
1. You have duplicated entities (i.e. an entity can have more than one id spread across one or more databases) and you have a non-exhaustive list of certain links between these ids. The Consolidator class can resolve/consolidate them all into single entities based on those sets of linked ids.

2. You want to determine all the nodes that connect (directly or indirectly) to every other node based on a list of known direct edges. This is equivalent to determining the components in undirected graph. Additionally it can be used as a metric of 'connectedness'.

# Usage
```
>>> from entity_merge.consolidation import Consolidator
>>> id_sets = [{0, 5, 1, 3}, {2, 4}, {9, 8, 7}, {6}, {6, 7}, {10}]
>>> consolidator = Consolidator()
>>> for id_set in id_sets:
        consolidator.add_id_set(id_set)
>>> consolidator.consolidate()
>>> print(consolidator.as_sets())
[{0, 1, 3, 5}, {2, 4}, {8, 9, 6, 7}, {10}]

>>> consolidator.add_id_set({3, 6})
>>> consolidator.consolidate()
>>> print(consolidator.as_sets())
[{0, 1, 3, 5, 6, 7, 8, 9}, {2, 4}, {10}]
```