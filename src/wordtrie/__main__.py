"""Entry point for the wordtrie package.

Run this file using `uv run wordtrie <pattern> <trie_file>[.gz]`.
"""

import re
from pprint import pprint
from sys import argv

from wordtrie import Trie


def main() -> None:
    """Main function to run the wordtrie script."""
    if len(argv) != 3:
        print("Usage: wordtrie <pattern> <trie_file>[.gz]")
        print("Example: wordtrie W..D words.txt.gz")
        return
    pattern = argv[1]
    trie_file = argv[2]
    assert re.fullmatch(r"[A-Z.]+", pattern), "Pattern must be capitalized A-Z and . only."

    trie = Trie.from_file(trie_file, gzip=trie_file.endswith(".gz"))
    filtered_words = list(trie.traverse(pattern))
    pprint(filtered_words, width=200, compact=True)


if __name__ == "__main__":
    main()
