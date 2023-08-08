# Name: Joel Strong
# OSU Email: stronjoe@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/15/2023
# Description:  TODO

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """Add a key/value pair to the hast map, doubling the capacity if the load factor is >= 0.5"""
        load_factor = self.table_load()
        if load_factor >= 0.5:
            self.resize_table(self._capacity * 2)
        self.add_key(HashEntry(key, value))

    def add_key(self, hash_entry: HashEntry) -> None:
        """Add a hash_entry object into the hash map using open addressing with quadratic probing for collision
            resolution. If hash_entry.key is found, update the value."""
        flag = False
        counter = 0
        hash = self._hash_function(hash_entry.key)
        while not flag:
            index = (hash + (counter ** 2)) % self._capacity
            if index > self._capacity - 1:
                index = index // self._capacity
            bucket = self._buckets[index]
            if not bucket:
                self._buckets[index] = hash_entry
                self._size += 1
                flag = True
            elif bucket.key == hash_entry.key:
                bucket.value = hash_entry.value
                if bucket.is_tombstone:
                    self._buckets[index].is_tombstone = False
                    self._size += 1
                flag = True
            elif bucket and bucket.is_tombstone:
                self._buckets[index] = hash_entry
                self._size += 1
                flag = True
            counter += 1

    def table_load(self) -> float:
        """Return the float value of size / capacity for the hash table"""
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """Return the number of empty buckets in the hash table DynamicArray.  O(N) time complexity"""
        count = 0
        for index in range(self._capacity):
            bucket = self._buckets[index]
            if not bucket or bucket.is_tombstone:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """If parameter new_capacity is less than current size - do nothing.  Check if new_capacity is a prime number -
            if not increment to the next prime number. O(N) time complexity. TODO"""
        # check and get correct next capacity
        if new_capacity < self._size:
            return
        if new_capacity < self._capacity:
            new_capacity = int((self._size / 0.66) * 2)
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # save and clear current array and build new one
        old = self._buckets
        old_size = self._size
        old_capacity = self._capacity
        self._capacity = new_capacity
        self.clear()

        # rehash all values from the old array into the new array
        for index in range(old_capacity):
            old_bucket = old[index]
            if old_bucket:
                if not old_bucket.is_tombstone:
                    self.add_key(old_bucket)

        if old_size != self._size:
            raise DynamicArrayException("Old Array values not transferred correctly")

    def get(self, key: str) -> object:
        """Return the value of parameter key if found, else None."""
        bucket = self.find_key(key)
        if bucket:
            return bucket.value

    def contains_key(self, key: str) -> bool:
        """Return True if the hash map contains the parameter key, else False"""
        bucket = self.find_key(key)
        return True if bucket else False

    def remove(self, key: str) -> None:
        """Remove the first key/value pair found with the parameter key in the hash table, else
            return None"""
        bucket = self.find_key(key)
        if bucket:
            bucket.is_tombstone = True
            self._size -= 1

    def find_key(self, key) -> object:
        """Return a hash_entry object if the parameter key is found in the hash map, else return None.
            Helper method used by get, contains_key, and remove methods."""
        counter = 0
        hash = self._hash_function(key)
        while counter != self._capacity - 2:
            index = (hash + (counter ** 2)) % self._capacity
            if index > self._capacity - 1:
                index = index // self._capacity
            bucket = self._buckets[index]
            if bucket:
                if bucket.key == key and not bucket.is_tombstone:
                    return bucket
            counter += 1
        return

    def clear(self) -> None:
        """Clear all data from the hash table"""
        self._buckets = DynamicArray()
        for times in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """Return a DynmaicArray of all keys and values in the hash table"""
        da = DynamicArray()
        if self._size == 0:
            return da
        for index in range(self._capacity):
            bucket = self._buckets[index]
            if bucket:
                if not bucket.is_tombstone:
                    da.append((bucket.key, bucket.value))
        return da

    def __iter__(self):
        """Return an iterable object of self"""
        self._index = 0
        return self

    def __next__(self):
        """Return the next variable of the iterable object of self"""
        try:
            test = False
            if self._buckets[self._index]:
                if not self._buckets[self._index].is_tombstone:
                    test = True
            while not test:
                self._index += 1
                test = False
                if self._buckets[self._index]:
                    if not self._buckets[self._index].is_tombstone:
                        test = True
        except DynamicArrayException:
            raise StopIteration
        self.key = self._buckets[self._index].key
        self.value = self._buckets[self._index].value
        saved = self
        self._index += 1
        return saved


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
