"""WordTrie: A Trie Data Structure for Word Games

This module provides a Trie class for efficiently storing and querying a set of
capitalized words (matching the regex [A-Z]+). It supports the insertion of words,
checking for word existence, and traversing the trie to find all words matching
a given pattern, using '.' as a wildcard character.

Example usage:
```
trie = Trie.from_file("words.txt")   # Load words from a file into the trie
is_found = "WORD" in trie            # Check if "WORD" is in the trie
words = list(trie.traverse("W..D"))  # Find all words matching the pattern "W..D"
```
"""

from .trie import Trie

__all__ = ["Trie"]
