class TrieNode:
    """
    A TrieNode represents a single node in the Trie.
    
    Attributes:
        children (dict): A dictionary mapping characters to child TrieNode instances.
        value (Any): The value associated with the node. None if no value is set.
        pass_count (int): The number of words that pass through this node.
    """
    def __init__(self):
        self.children = {}
        self.value = None
        self.pass_count = 0


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
            # Increase the pass_count for each node visited
            current.pass_count += 1

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

    # Інші методи (delete, is_empty, тощо) можемо додати, якщо потрібно, 
    # але для завдання з пошуком спільного префікса вони не обов'язкові.


class LongestCommonWord(Trie):
    """
    A class that extends Trie to find the longest common prefix (LCP)
    among a list of input strings.
    """

    def find_longest_common_word(self, strings) -> str:
        """
        Finds the longest common prefix among all strings in the input list.

        If the list is empty, or if there's no common prefix, returns an empty string.
        Raises TypeError if 'strings' is not a list of strings.

        The time complexity is O(S), where S is the total length of all strings,
        because we insert each string into the Trie, then traverse the Trie once
        to find the longest common prefix.

        Args:
            strings (list): A list of strings for which to find the common prefix.

        Returns:
            str: The longest common prefix of all strings in the list.
                 Returns "" if no common prefix exists or input is invalid.
        """
        # Validate input
        if not isinstance(strings, list):
            return ""  # or raise TypeError("strings must be a list")
        if not strings:
            return ""  # empty list => no common prefix

        # Check that all elements are strings
        for s in strings:
            if not isinstance(s, str):
                return ""  # or raise TypeError(f"Invalid element in strings: {s}")

        # Insert all strings into the Trie
        # We'll also track how many words we have (needed for pass_count check)
        total_strings = len(strings)
        for s in strings:
            # Each time we put a string, we start from the root; 
            # increment the pass_count for each node as we go along
            self._insert_with_passcount(s)

        # Now traverse from the root, collecting characters while:
        # 1) There's exactly 1 child in the current node
        # 2) That child's pass_count == total_strings
        longest_common_prefix = ""
        current_node = self.root

        # We continue as long as there's exactly one child
        # and that child is common to all strings.
        while True:
            if len(current_node.children) != 1:
                break  # more than 1 child or 0 children => stop
            (char, next_node), = current_node.children.items()

            # If pass_count is not equal to total_strings,
            # it means not all strings share this path
            if next_node.pass_count != total_strings:
                break

            # Add this char to our prefix and move deeper
            longest_common_prefix += char
            current_node = next_node

        return longest_common_prefix

    def _insert_with_passcount(self, key):
        """
        A helper method that inserts a key into the existing Trie.
        Increments pass_count for each node on the path.

        Args:
            key (str): The string to insert into the Trie.
        """
        current = self.root
        # Root node pass_count isn't strictly needed if we only
        # track deeper nodes, but let's increment it consistently
        current.pass_count += 1  

        for char in key:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
            current.pass_count += 1


if __name__ == "__main__":
    # Tests
    trie = LongestCommonWord()
    strings = ["flower", "flow", "flight"]
    assert trie.find_longest_common_word(strings) == "fl"

    trie = LongestCommonWord()
    strings = ["interspecies", "interstellar", "interstate"]
    assert trie.find_longest_common_word(strings) == "inters"

    trie = LongestCommonWord()
    strings = ["dog", "racecar", "car"]
    assert trie.find_longest_common_word(strings) == ""

    print("All tests passed successfully!")
