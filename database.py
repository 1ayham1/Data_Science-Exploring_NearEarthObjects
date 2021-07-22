"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

"""

from collections import defaultdict

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s. --> list
        :param approaches: A collection of `CloseApproach`es. --> list
        """

        self._neos = neos
        self._approaches = approaches

        #approaches is a subset from neos. i.e. some neos approach earth and some don't
        #The mapping between the lists is many_to_one with unique id....
        #  The same neo may approach earth multiple times

        neos_ids = [neo.designation for neo in self._neos]
        approach_ids = [app.get_designation for app in self._approaches]

        #store original indeces for fast access
        neos_org_idxs = dict((k,i) for i,k in enumerate(neos_ids))
        approach_org_idxs = dict((k,i) for i,k in enumerate(approach_ids))

        #common ids between neos and approaches
        neos_approach_shared_ids = set(neos_org_idxs).intersection(approach_ids)
        
        #locations of neo in neos_list that has a corrosponding id in approaches list and vice versa
        idx_neos_subset = [neos_org_idxs[x] for x in neos_approach_shared_ids]
        idx_approach_subset = [approach_org_idxs[x] for x in neos_approach_shared_ids]

        
        #iterat over the matched indeces
        for neo_idx,approach_idx in zip(idx_neos_subset,idx_approach_subset):
            self._approaches[approach_idx].neo = self._neos[neo_idx]
            self._neos[neo_idx].approaches.append(self._approaches[approach_idx])

        print("\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(self._neos[10])
        print("-------------------------------------")
        print(self._approaches[10])
        print("\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        #these neos has designation that is also in approaches
        #neos_of_interest = map(self._neos.__getitem__, idx_neos_subset)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        #build temp dictionary
        neos_ids = {neo.designation: neo for neo in self._neos}

        return neos_ids.get(designation.upper(),None)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        
        #Fetch an NEO by its name. Build temp dict
        neos_names = {neo.name: neo for neo in self._neos}

        return neos_names.get(name.capitalize(), None)

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # TODO: Generate `CloseApproach` objects that match all of the filters.
        for approach in self._approaches:
            yield approach
