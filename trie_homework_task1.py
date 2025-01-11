class TrieNode:
    """
    A TrieNode represents a single node in the Trie.
    
    Attributes:
        children (dict): A dictionary mapping characters to child TrieNode instances.
        value (Any): The value associated with the node. None if no value is set.
    """
    def __init__(self):
        self.children = {}
        self.value = None


class Trie:
    """
    A Trie (prefix tree) for storing string keys with optional associated values.
    
    Attributes:
        root (TrieNode): The root node of the Trie.
        size (int): The total number of keys stored in the Trie.
    """
    def __init__(self):
        """
        Initializes a new Trie instance with an empty root node and size zero.
        """
        self.root = TrieNode()
        self.size = 0

    def put(self, key, value=None):
        """
        Inserts a key-value pair into the Trie. If the key already exists,
        updates its value.

        Args:
            key (str): The string key to insert or update in the Trie.
            value (Any, optional): The value to associate with the key.
                                   Defaults to None.

        Raises:
            TypeError: If key is not a non-empty string.
        """
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for put: key = {key} must be a non-empty string")

        current = self.root
        for char in key:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        if current.value is None:
            self.size += 1
        current.value = value

    def get(self, key):
        """
        Retrieves the value associated with a given key in the Trie.

        Args:
            key (str): The string key to lookup.

        Returns:
            Any: The value stored for this key, or None if the key does not exist.

        Raises:
            TypeError: If key is not a non-empty string.
        """
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for get: key = {key} must be a non-empty string")

        current = self.root
        for char in key:
            if char not in current.children:
                return None
            current = current.children[char]
        return current.value

    def delete(self, key):
        """
        Removes a key (and its associated value) from the Trie if it exists.

        Args:
            key (str): The string key to remove.

        Raises:
            TypeError: If key is not a non-empty string.

        Returns:
            bool: True if the key was successfully deleted, False otherwise.
        """
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for delete: key = {key} must be a non-empty string")

        def _delete(node, key, depth):
            if depth == len(key):
                if node.value is not None:
                    node.value = None
                    self.size -= 1
                    return len(node.children) == 0
                return False

            char = key[depth]
            if char in node.children:
                should_delete = _delete(node.children[char], key, depth + 1)
                if should_delete:
                    del node.children[char]
                    return len(node.children) == 0 and node.value is None
            return False

        return _delete(self.root, key, 0)

    def is_empty(self):
        """
        Checks if the Trie is empty (i.e., contains no keys).

        Returns:
            bool: True if the Trie has size 0, False otherwise.
        """
        return self.size == 0

    def longest_prefix_of(self, s):
        """
        Finds the longest prefix of the given string 's' that exists in the Trie.

        Args:
            s (str): The string for which to find the longest prefix.

        Returns:
            str: The longest prefix in the Trie. If no prefix is found, returns "".

        Raises:
            TypeError: If s is not a non-empty string.
        """
        if not isinstance(s, str) or not s:
            raise TypeError(f"Illegal argument for longestPrefixOf: s = {s} must be a non-empty string")

        current = self.root
        longest_prefix = ""
        current_prefix = ""
        for char in s:
            if char in current.children:
                current = current.children[char]
                current_prefix += char
                if current.value is not None:
                    longest_prefix = current_prefix
            else:
                break
        return longest_prefix

    def keys_with_prefix(self, prefix):
        """
        Collects all keys in the Trie that start with the given prefix.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            list of str: A list of keys in the Trie that start with the specified prefix.

        Raises:
            TypeError: If prefix is not a string.
        """
        if not isinstance(prefix, str):
            raise TypeError(f"Illegal argument for keysWithPrefix: prefix = {prefix} must be a string")

        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        result = []
        self._collect(current, list(prefix), result)
        return result

    def _collect(self, node, path, result):
        """
        Helper method to recursively collect all keys below the given node.

        Args:
            node (TrieNode): The current TrieNode to collect from.
            path (list of str): The current sequence of characters forming a key.
            result (list of str): The list to accumulate the full keys.
        """
        if node.value is not None:
            result.append("".join(path))
        for char, next_node in node.children.items():
            path.append(char)
            self._collect(next_node, path, result)
            path.pop()

    def keys(self):
        """
        Returns a list of all keys stored in the Trie.

        Returns:
            list of str: All the keys in the Trie.
        """
        result = []
        self._collect(self.root, [], result)
        return result


class Homework(Trie):
    """
    Homework class that extends the functionality of the base Trie with two methods:
    1) count_words_with_suffix(pattern)
    2) has_prefix(prefix)
    """
    def count_words_with_suffix(self, pattern) -> int:
        """
        Returns the number of words in the Trie that end with 'pattern'.
        Must handle incorrect inputs by raising TypeError if the pattern is not a string.
        Case-sensitive comparisons.

        Args:
            pattern (str): The suffix to check.

        Returns:
            int: The count of words ending with 'pattern'.
        """
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")

        all_keys = self.keys()
        return sum(1 for key in all_keys if key.endswith(pattern))

    def has_prefix(self, prefix) -> bool:
        """
        Returns True if there is at least one word in the Trie that starts with 'prefix'.
        Must handle incorrect inputs by raising TypeError if the prefix is not a string.
        Case-sensitive comparisons.

        Args:
            prefix (str): The prefix to check.

        Returns:
            bool: True if any word starts with 'prefix', False otherwise.
        """
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")

        current = self.root
        for ch in prefix:
            if ch not in current.children:
                return False
            current = current.children[ch]
        return True


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Testing count_words_with_suffix
    assert trie.count_words_with_suffix("e") == 1   # apple
    assert trie.count_words_with_suffix("ion") == 1 # application
    assert trie.count_words_with_suffix("a") == 1   # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Testing has_prefix
    assert trie.has_prefix("app") == True   # "apple", "application"
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True   # "banana"
    assert trie.has_prefix("ca") == True    # "cat"

    print("All tests passed successfully!")
