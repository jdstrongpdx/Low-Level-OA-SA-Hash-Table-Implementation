# Name: Joel Strong
# OSU Email: stronjoe@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/15/2023
# Description:  Creation of a hash map using singly chained collision resolution.  Includes common methods for
#               add (put), get, contains_key, remove, clear, export (get_keys_and_values) as well as methods for
#               internal functioning (table_load, resize_table, empty_buckets).  Includes a out of class function
#               for find_mode.


from a6_include import (DynamicArray, LinkedList, SLNode, LinkedListIterator, DynamicArrayException,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        """Add parameter key/value pair to the hash map using chaining for collision resolution.  If key exists in the
            hash table, update the value for the key.  Double the hash map capacity if the load factor is >= 1."""
        # resize the DynamicArray if the table load is >= 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # find hash and index for the key in the array
        hash = self._hash_function(key) % self._capacity
        bucket = self._buckets[hash]

        # if index is empty, add node to LinkedList - O(1) time complexity
        if not bucket.length():
            bucket.insert(key, value)
            self._size += 1
            return

        # if not empty, search the LinkedList for the parameter key and replace the value if found
        # worst case O(LinkedList.length())
        for node in bucket:
            if node.key == key:
                node.value = value
                return

        # if the key was not found, insert the key/value pair - O(1) time complexity
        bucket.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """Return the number of empty buckets in the hash table DynamicArray.  O(N) time complexity"""
        count = 0
        for index in range(self._capacity):
            if not self._buckets[index].length():
                count += 1
        return count

    def table_load(self) -> float:
        """Return the float value of size / capacity for the hash table.  O(1) time complexity"""
        return self._size / self._capacity

    def clear(self) -> None:
        """Clear all key/value pairs from the hash table.  O(N) time complexity"""
        self._buckets = DynamicArray()
        for index in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """If parameter new_capacity is less than 1 - do nothing.  Check if new_capacity is a prime number - if not
            increment to the next prime number. O(N) time complexity. TODO"""
        # if new_capacity is not less than 1, do nothing
        if new_capacity < 1:
            return

        # check/make new_capacity a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # save current array and build a new one
        old = self.get_keys_and_values()
        self._capacity = new_capacity
        old_size = self._size
        self.clear()

        # rehash all values from the old array into the new array
        for index in range(old_size):
            old_bucket = old[index]
            self.put(old_bucket[0], old_bucket[1])

        # check all values transferred properly
        if old_size != self._size:
            raise DynamicArrayException("Error transferring data during resize_table")

    def get(self, key: str) -> object:
        """Return the value of parameter key if found, else None."""
        bucket = self.get_bucket(key)
        if bucket:
            result = bucket.contains(key)
            return result.value if result else None
        return None

    def contains_key(self, key: str) -> bool:
        """Return True if the hash map contains the parameter key, else False"""
        bucket = self.get_bucket(key)
        if bucket:
            result = bucket.contains(key)
            return True if result else False
        return False

    def remove(self, key: str) -> None:
        """Remove a key/value pair from the hash map if the parameter key is found, else do nothing."""
        bucket = self.get_bucket(key)
        if bucket:
            result = bucket.remove(key)
            if result:
                self._size -= 1

    def get_bucket(self, key) -> object:
        """Return the LinkedList object for the parameter key if found, else return None"""
        hash = self._hash_function(key) % self._capacity
        # if the hash is smaller or greater than the array size
        if hash < 0 or hash > self._capacity - 1:
            return
        # if the hash bucket is empty
        if not self._buckets[hash].length():
            return
        return self._buckets[hash]

    def get_keys_and_values(self) -> DynamicArray:
        """Return a DynamicArray of all key/value pairs in the hash map"""
        da = DynamicArray()

        if self._size == 0:
            return da
        for index in range(self._capacity):
            bucket = self._buckets[index]
            if bucket.length():
                for node in bucket:
                    da.append((node.key, node.value))
        return da


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """Return a new DynamicArray and count of the highest occurring items in the parameter DynamicArray.
        O(N) time complexity"""
    map = HashMap()
    da_return = DynamicArray()
    max_val = 0
    for index in range(da.length()):
        # For each 'key' in parameter DynamicArray, increment value if it exists else add 'key' with value of 1 if not
        item = da[index]
        value = map.get(item)
        if not value:
            value = 1
        else:
            value += 1
        # if the value is greater than the max_val, clear the return array and add keys with same max_val
        if value > max_val:
            da_return = DynamicArray()
            da_return.append(item)
            max_val = value
        elif value == max_val:
            da_return.append(item)
        map.put(item, value)
    return da_return, max_val


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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

    print("\nPDF - get out of bounds")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 123456)
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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())
    
    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
