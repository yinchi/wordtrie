"""A trie (prefix tree) for storing a set of strings."""

from gzip import open as gzip_open
from os import PathLike
from typing import Iterator, Sequence


class Trie:
    """A trie (prefix tree) for storing a set of strings.

    The strings all match the regex [A-Z]+, i.e. capitalized words.
    """

    def __init__(self) -> None:
        self.is_word: bool = False
        """Is the prefix a word by itself?"""

        self.children: None | Sequence[None | Trie] = None
        """For a leaf node, None, else, a list of child tries for each letter A-Z.

        A leaf node represents a word that is not a prefix of any other word in the trie.
        """

        self.n_descendants: int = 0
        """The number of descendants (children) in the trie.

        That is, the number of words containing `self.prefix` as a prefix, excluding `self.prefix`
        itself.
        """

    def __str__(self) -> str:
        """Get a string representation of the trie.

        Used by `str(trie)` or `print(trie)`.
        """
        return f"Trie(is_word={self.is_word}, n_descendants={self.n_descendants})"

    def __getitem__(self, prefix: str) -> "Trie | None":
        """Get the child trie for the given prefix, if it exists.

        Usage: `trie["WO"]` returns the child trie for the prefix "WO", or None if it
        doesn't exist.
        """
        if prefix:
            # Get the child trie for the first character.
            if self.children:
                if child := self.children[ord(prefix[0]) - ord('A')]:
                    # Recurse into the child trie for the remainder of the prefix.
                    return child.__getitem__(prefix[1:])
            return None  # No child trie exists for this prefix.
        return self  # Prefix is empty, return the current trie.

    def __contains__(self, word: str) -> bool:
        """Check if the trie contains the given word.

        Usage: `"WORD" in trie` returns True if "WORD" is in the trie, else False.
        """
        node = self[word]
        return node is not None and node.is_word

    def insert(self, word: str) -> None:
        """Insert a word into the trie.

        Recurse into the child tries for each character in `word`.
        """

        # If `word` is empty, mark this node as a word.
        if not word:
            self.is_word = True
            return

        # Pop the first character of `word`
        char, remaining = word[0], word[1:]
        assert 'A' <= char <= 'Z', "Words must be capitalized A-Z only."

        # Create the children list if it doesn't exist
        if self.children is None:
            self.children = [None for _ in range(26)]

        # Create the child trie if it doesn't exist
        index = ord(char) - ord('A')
        if self.children[index] is None:
            self.children[index] = Trie()

        # Recurse into the child trie to insert the remainder of the word.
        self.n_descendants += 1
        self.children[index].insert(remaining)

    def traverse(self, pattern: str, prefix: str = "") -> Iterator[str]:
        """Yield all words in the trie that match the given pattern.

        The pattern may contain '.' characters, which match any letter.
        """
        # Base case: if the pattern is empty, yield the current prefix if it's a word,
        # then return.
        if not pattern:
            if self.is_word:
                yield prefix
            return

        # If there are no children, we can't match anything.
        if not self.children:
            return

        char, remaining_pattern = pattern[0], pattern[1:]

        # If the current character is a wildcard '.', we need to explore all children.
        if char == '.':
            for idx, child in enumerate(self.children):
                if child is not None:
                    new_prefix = prefix + chr(idx + ord('A'))
                    yield from child.traverse(remaining_pattern, new_prefix)

        # Otherwise, recurse down the trie for the specific child.
        else:
            if self.children:
                if child := self.children[ord(char) - ord('A')]:
                    new_prefix = prefix + char
                    yield from child.traverse(remaining_pattern, new_prefix)

    @staticmethod
    def from_words(words: Sequence[str]) -> "Trie":
        """Create a trie from a list of words."""
        root = Trie()
        for word in words:
            root.insert(word.upper())
        return root

    @staticmethod
    def from_file(file_path: PathLike, gzip: bool = False) -> "Trie":
        """Create a trie from a file containing one word per line."""
        root = Trie()
        open_func = gzip_open if gzip else open
        with open_func(file_path, "rt", encoding="utf-8") as f:
            for line in f:
                root.insert(line.strip().upper())
        return root
