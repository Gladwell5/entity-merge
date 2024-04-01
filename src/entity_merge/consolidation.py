class Consolidator:
    def __init__(self):
        self.id_sets = []
        self.id_dict = {}
        self.n_ids = 0
        self.n_groups = 0
        self.n_iterations = 0
    
    def add_id_set(self, id_set):
        self.id_sets.append(id_set)
        return None
    
    def _get_min_grp(self, id_set):
        existing_groups = []
        for _id in id_set:
            try:
                existing_groups.extend(self.id_dict[_id])
            except KeyError:
                pass
        min_grp = min(existing_groups) if existing_groups else -1
        return min_grp
    
    def _assign_grp(self, id_set, grp_num):
        for _id in id_set:
            try:
                self.id_dict[_id] |= set([grp_num])
            except KeyError:
                self.id_dict[_id] = set([grp_num])
        return None

    def _setup_id_dict(self):
        self.n_iterations = 0
        self.id_dict = {}
        grp_counter = 0
        for id_set in self.id_sets:
            min_grp = self._get_min_grp(id_set)
            if min_grp >= 0:
                this_group_num = min_grp
            else:
                this_group_num = grp_counter
                grp_counter += 1
            self._assign_grp(id_set, this_group_num)
        return None
    
    def _make_multi_lookup(self):
        multi_lookup = {}
        for grps in self.id_dict.values():
            for grp in grps:
                min_grp = min(grps)
                try:
                    min_grp = min(multi_lookup[grp], min_grp)
                except KeyError:
                    pass
                multi_lookup[grp] = min_grp
        is_resolved = set(multi_lookup.keys()) == set(multi_lookup.values())
        return is_resolved, multi_lookup

    def _reduce_id_dict(self):
        while True:
            is_resolved, multi_lookup = self._make_multi_lookup()
            if is_resolved:
                break
            else:
                for _id, grps in self.id_dict.items():
                    self.id_dict[_id] = set([multi_lookup[grp] for grp in grps])
            self.n_iterations += 1
        return None
    
    def consolidate(self):
        self._setup_id_dict()
        self._reduce_id_dict()
        for _id, grps in self.id_dict.items():
            self.id_dict[_id] = list(grps)[0]
        self.n_ids = len(self.id_dict.keys())
        self.n_groups = len(set(self.id_dict.values()))
        return None

    def as_sets(self):
        set_dict = {}
        for _id, grp in self.id_dict.items():
            if grp not in set_dict.keys():
                set_dict[grp] = set([])
            set_dict[grp] |= set([_id])
        return list(set_dict.values())
