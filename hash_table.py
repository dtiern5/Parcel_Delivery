# This class is slightly modified from zyBooks C950: Data Structures and Algorithms II Section 7.8

class ChainingHashTable:

    # Constructor with optional capacity parameter
    # Assigns an empty list to each bucket
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def _get_hash(self, key):
        """
        Establishes the correct bucket for a given key
        :param key: The key to hash
        :return: The bucket for the key
        Time complexity: O(1)
        """
        bucket = hash(key) % len(self.table)
        return self.table[bucket]

    def insert(self, key, item):
        """
        Inserts a new item into the hash table
        :param key: The key of the item to insert (in our case, package ID)
        :param item: The item to insert (in our case, the package itself)
        :return: True
        Time complexity: O(n)
        """
        # get the bucket list where the item belongs
        bucket_list = self._get_hash(key)

        # if key is already in bucket list, value will be updated to the given parameter 'item'
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # insert key_value to the end of the list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        """
        Searches for an item from the hash table
        :param key: The key of the item to search for
        :return: the value for the given key
        Time complexity: O(n)
        """
        # get the bucket list for where this item would be
        bucket_list = self._get_hash(key)

        # search for the key within the bucket list. If found, return the value
        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        return None

    def remove(self, key):
        """
        Removes an item from the hash table
        :param key: The key of the item to remove
        :return: None
        Time complexity: O(n)
        """
        # get the bucket list where the item resides
        bucket_list = self._get_hash(key)

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
