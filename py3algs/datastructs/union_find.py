"""
A simple Union-Find data structure implementation.

author: 
Christos Nitsas
(chrisn654 or nitsas)

language:
Python 3(.4)

date:
July, 2014
"""


class UnionFindSimpleImpl:
    """
    A simple Union-Find data structure implementation.
    
    If n is the number of items in the structure, a series of m union 
    operations will take O(m * log(n)) time. Find operations are (amortized)
    constant time (O(1)) though.
    """
    def __init__(self, items):
        """Initialize the Union-Find structure from an iterable."""
        self._items = set(items)
        self._leader = dict()
        self._followers = dict()
        self._cluster_size = dict()
        for item in self._items:
            self._leader[item] = item
            self._followers[item] = [item]
            self._cluster_size[item] = 1
    
    def __getitem__(self, item):
        """
        Return the cluster (i.e. the cluster's leader) that the given item 
        belongs to.
        
        Equivalent to UnionFindStructure.find().
        """
        return self._leader[item]
    
    
    def find(self, item):
        """
        Return the cluster (i.e. the cluster's leader) that the given item 
        belongs to.
        
        Equivalent to UnionFindStructure.__getitem__().
        """
        return self[item]
    
    def union(self, item_a, item_b):
        """
        Join together the two clusters that items item_a and item_b 
        belong to.
        """
        leader_a = self._leader[item_a]
        leader_b = self._leader[item_b]
        if leader_a == leader_b:
            return
        if self._cluster_size[leader_b] > self._cluster_size[leader_a]:
            leader_a, leader_b = leader_b, leader_a
        for follower in self._followers[leader_b]:
            self._leader[follower] = leader_a
        self._followers[leader_a].extend(self._followers[leader_b])
        del(self._followers[leader_b])
        self._cluster_size[leader_a] += self._cluster_size[leader_b]
        del(self._cluster_size[leader_b])
    
    def joined(self, item_a, item_b):
        """
        Return True it the items belong to the same cluster; False otherwise.
        """
        if self.find(item_a) == self.find(item_b):
            return True
        else:
            return False
    
    def num_clusters(self):
        """Return the current number of clusters as an int."""
        return len(self._cluster_size)
    
    def clusters(self):
        """
        Return all clusters as a (real-time) dictview of lists.
        
        Caution: 
        The result is a real-time view of the clusters, i.e. if one first
        calls this method to get a clusters_view object and then merges two
        clusters, the original clusters_view object will reflect the change.
        
        One can use list(myunionfindobject.clusters()) if they want a list of 
        lists. BUT this is even more dangerous if there are more unions to 
        come, because some of the inner lists of the result will change or
        stop being valid after a union operation.
        """
        return self._followers.values()
    
    def items(self):
        """Return a set containing all the items in the structure."""
        return self._items


class UnionFindUnionByRankAndPathCompression:
    """
    A faster Union-Find implementation with lazy unions (using union by 
    rank) and path compression.
    
    A series of m union & find operations on a structure with n items 
    will need time O(m * a(n)), where a(n) is the reverse Ackerman 
    function.
    """
    def __init__(self, items):
        """Initialize the Union-Find structure from an iterable."""
        raise(NotImplementedError)
    
    def __getitem__(self, item):
        """
        Return the cluster (i.e. the cluster's leader) that the given item 
        belongs to.
        
        Equivalent to UnionFindStructure.find().
        """
        raise(NotImplementedError)
    
    
    def find(self, item):
        """
        Return the cluster (i.e. the cluster's leader) that the given item 
        belongs to.
        
        Equivalent to UnionFindStructure.__getitem__().
        """
        raise(NotImplementedError)
    
    def union(self, item_a, item_b):
        """
        Join together the two clusters that items item_a and item_b 
        belong to.
        """
        raise(NotImplementedError)
    
    def joined(self, item_a, item_b):
        """
        Return True it the items belong to the same cluster; False otherwise.
        """
        raise(NotImplementedError)
    
    def num_clusters(self):
        """Return the current number of clusters as an int."""
        raise(NotImplementedError)
    
    def clusters(self):
        """
        Return all clusters as a (real-time) dictview of lists.
        
        Caution: 
        The result is a real-time view of the clusters, i.e. if one first
        calls this method to get a clusters_view object and then merges two
        clusters, the original clusters_view object will reflect the change.
        
        One can use list(myunionfindobject.clusters()) if they want a list of 
        lists. BUT this is even more dangerous if there are more unions to 
        come, because some of the inner lists of the result will change or
        stop being valid after a union operation.
        """
        raise(NotImplementedError)
    
    def items(self):
        """Return a set containing all the items in the structure."""
        raise(NotImplementedError)


_default_impl = UnionFindSimpleImpl


class UnionFindStructure:
    """
    A Union-Find data structure interface.
    
    It relies on a concrete Union-Find implementation such as 
    UnionFindSimpleImpl or UnionFindLazyUnionsAndPathCompressionImpl.
    """
    def __init__(self, items, *, impl=_default_impl):
        self._impl = impl(items)
    
    def __getitem__(self, item):
        return self._impl.__getitem__(item)
    
    def __getattr__(self, name):
        return getattr(self._impl, name)


