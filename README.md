# Trie-based pattern matching

This package uses a Trie to find words from a dictionary file matching a pattern. The pattern can contain any uppercase letter A&ndash;Z plus the wildcard character &ldquo;.&rdquo; matching a single character.

Timing tests are performed in `notebooks/test.ipynb`.

## uv-based installation

See [the official instructions for installing `uv`](https://docs.astral.sh/uv/getting-started/installation/).  Then, run:

```bash
uv sync -p pypy@3.11
```
Finally, set up Visual Studio Code to use the newly created virtual environment.

Note that in the command above, we use [Pypy](https://pypy.org/index.html) over the default CPython version of Python for improved speed.

## Running from the command line

Try:
```bash
uv run wordtrie S...ING words.txt.gz
```

Alternatively:
```bash
source .venv/bin/activate
python -m wordtrie S...ING  words.txt.gz
deactivate
```

### The input file

**Gzip support**: We support the reading of .gz files for the word list.  To zip/unzip:
```bash
gzip -kv9 words.txt
gunzip -ckv words.txt.gz > words_out.txt

# check
diff words.txt words_out.txt
```

The `main` function in `__main__.py` will automatically decompress the input file if the filename ends in `.gz`.

**Line endings:** Parsing the word list may fail if the line endings do not match those expected by Python's `open()`. Various tools can be used to fix this, e.g. `dos2unix`.

## Running from a Python script

See `__main__.py` for an example of using the `wordtrie` module in a Python script.  This is the same script that is invoked by `uv run wordtrie`.

## Using this module in another project

On the command line:
```bash
uv add git+https://github.com/yinchi/wordtrie
```

In Python, import the class as normal:
```py
from wordtrie import Trie
```

To update the `wordtrie` module:
```bash
uv sync -P wordtrie  # This pulls the latest version from Git
```

## Code style

We use `isort`, `autopep8`, and `pylint` to format and lint our code.  A script `.style.sh` has been provided to run all three commands in sequence.


## Forking this project under the MIT license

Append your own copyright line in `LICENSE` below the existing line and leave the rest of the file unchanged.
