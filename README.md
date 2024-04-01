# Description
Given a list of sets, consolidate sets that share at least one member.
See set consolidation - see https://rosettacode.org/wiki/Set_consolidation
This is also known as connected components in graphs.

This is (in most circumstances) a more efficient implementation of set consolidation than those on Rosetta Code and others found on Stack Overflow.

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