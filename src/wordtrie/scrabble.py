
"""Manage a Scrabble hand of tiles and compute word scores.

Run this file using `uv run scrabble <pattern> <trie_file>[.gz]`.
"""

from collections import Counter
from itertools import islice
from pprint import pprint
from collections import Counter
from random import sample
import re
from sys import argv

from wordtrie import Trie

values = {}

for letter in "LSUNRTOAIE":
    values[letter] = 1
for letter in "GD":
    values[letter] = 2
for letter in "BCMP":
    values[letter] = 3
for letter in "FHVWY":
    values[letter] = 4
for letter in "K":
    values[letter] = 5
for letter in "JX":
    values[letter] = 8
for letter in "QZ":
    values[letter] = 10

default_tiles = Counter()
for letter in "E":
    default_tiles[letter] = 12
for letter in "AI":
    default_tiles[letter] = 9
for letter in "O":
    default_tiles[letter] = 8
for letter in "NRT":
    default_tiles[letter] = 6
for letter in "LSDU":
    default_tiles[letter] = 4
for letter in "G":
    default_tiles[letter] = 3
for letter in "BCMPFHVWY":
    default_tiles[letter] = 2
for letter in "KJXQZ":
    default_tiles[letter] = 1

def score(word: str) -> int:
    """Compute the Scrabble score for a word."""
    return sum(values[letter] for letter in word)

def can_play(word: Counter, hand: Counter = default_tiles) -> bool:
    """Can I play the word with my tiles?
    
    Params:
        word: The word to play, as a Counter of letters
        hand: The current hand of tiles, as a Counter
    Returns:
        True if the word can be played, False if not enough tiles
    """
    return not (word - hand)

def play(word: str, hand: Counter = default_tiles) -> bool:
    """Play the word if possible, returning whether it was played.
    
    Params:
        word: The word to play, in uppercase A-Zs
        hand: The current hand of tiles, as a Counter
    Returns:
        True if the word was played, False if not enough tiles
    """
    cword = Counter(word)
    if can_play(cword, hand):
        hand.subtract(cword)
        return True
    return False

def unplay(word: str, hand: Counter = default_tiles) -> None:
    """Return the tiles from a played word back to the hand.

    Params:
        word: The word to unplay, in uppercase A-Zs
        hand: The current hand of tiles, as a Counter
    """
    hand.update(Counter(word))

def main() -> None:
    """Main function to run the scrabble script."""
    pprint(list(Counter(default_tiles).items()), width=100, compact=True)
    print(f"Total tiles (excluding 2 blanks): {sum(default_tiles.values())}")
    print()

    # Play the word "hello"
    hand = default_tiles.copy()
    assert play("HELLO", hand)
    print(f"Played HELLO for {score('HELLO')} points, now we have {hand['L']} Ls left")
    assert not play("LOLLY", hand)  # 4 Ls but we already used 2
    print(f"Cannot play LOLLY, would have scored {score('LOLLY')} points")
    unplay("HELLO", hand)
    print(f"Unplayed HELLO, now we have {hand['L']} Ls left")
    assert hand == default_tiles  # back to original state?

    # Test our word list
    if len(argv) != 3:
        print("Usage: scrabble <pattern> <trie_file>[.gz]")
        print("Example: scrabble W..D words.txt.gz")
        exit(1)
    pattern = argv[1]
    trie_file = argv[2]
    assert re.fullmatch(r"[A-Z.]+", pattern), "Pattern must be capitalized A-Z and . only."

    N_SHOW = 20

    trie = Trie.from_file(trie_file, gzip=trie_file.endswith(".gz"))
    # TODO: incorporate the filtering into the traversal to avoid traversing unplayable branches
    filtered_words = [word for word in trie.traverse(pattern) if can_play(Counter(word))]
    filtered_words.sort(key=score, reverse=True)
    scored_words = [(word, score(word)) for word in islice(filtered_words, N_SHOW)]

    print()
    print(f"Top {min(N_SHOW, len(scored_words))} words I can play with my tiles "
          f"matching '{pattern}':")
    print("-"*100)
    pprint(scored_words, width=100, compact=True)

    n_random = min(10, len(filtered_words))
    print()
    print(f"{n_random} random words I can play with my tiles matching '{pattern}':")
    print("-"*100)
    random_words = sample(filtered_words, n_random)
    scored_words = [(word, score(word)) for word in random_words]
    pprint(scored_words, width=100, compact=True)


if __name__ == "__main__":
    main()
