class ChainingHashTable:

    # Constructor with optional capacity parameter
    # Assigns an empty list to each bucket
    # Time complexity: O(n)
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])


    # Establishes the correct bucket for a given key
    # Time complexity: O(1)
    def _get_hash(self, key):
        bucket = hash(key) % len(self.table)
        return self.table[bucket]


    # Inserts a new item into the hash table
    # Time complexity: O(n)
    def insert(self, key, item):
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

    # Return the value for a given key or 'None' if the key is not found
    # Time complexity: O(n)
    def search(self, key):
        # get the bucket list for where this item would be
        bucket_list = self._get_hash(key)

        # search for the key within the bucket list. If found, return the value
        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        return None

    # Remove an item based on the parameter 'key' from the hash table.
    # Time complexity: O(n)
    def remove(self, key):
        # get the bucket list where the item resides
        bucket_list = self._get_hash(key)

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
