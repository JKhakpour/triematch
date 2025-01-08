# TrieMatch
A multiple pattern matching library. Trying to implement some algorithms for matching many string patterns in the pattern.

This project is a WIP and I would like to receive your idea on improving it.

## Trie (Prefix Tree)
This class implements a prefix tree for matching the patterns.

It uses a normal Trir data structure, and Aho-Corasick is used for pattern search (`Trie.search`). Just make sure to use `Trie.link_nodes()`.

```python
import this
from triematch import Trie

zen_of_klingon = this.s
print(zen_of_klingon)

zen_of_klingon = zen_of_klingon.lower()

words = {
    "gur": "the",
    "mra": "zen",
    "gur mra": "the zen",
    "guna": "than",
    "chevgl": "purity",
    "Pbzcyrk": "complex",
}


wordset = Trie(words) ## or Trie(**words) like a dict initalization

## Similar behavior with dict object
"error" in wordset # Output: True
wordset.get('error') # Output: False
wordset.setdefault("error", "reebef") # Outpit: reebef

wordset
# Output: {'error': 'reebef', 'complex': 'Pbzcyrk', 'purity': 'chevgl', 'mra': 'zen', 'gur': 'the', 'gur mra': 'the zen'}

## Get list of all patterns which zen_of_klingon.strtswith(pattern)
list(wordset.match(zen_of_klingon))
# Output: [(3, 'the'), (7, 'the zen')]
## where wordset[zen_of_klingon[:3]] == 'the'

wordset.link_nodes() ## do this to speed up the search process
list(wordset.search(zen_of_klingon))
# Output: [(0, 3, 'the'), (0, 7, 'the zen'), (4, 7, 'zen'), (54, 58, 'than'), ...]
## where wordset[zen_of_klingon[4:7]] == 'zen'

## Compressed regex of Trie
wordset.to_regex()
'Pbzcyrk|chevgl|gu(?:na|r)|mra'
```

## Tuples as Trie keys
`TupleTrie` treats keys as tuples (instead of strings), so you can pass keys like tuple of numbers as keys.

```python
from triematch import TupleTrie

trie = TupleTrie()
trie[127,0,0,1] = "home"
trie[(8,8,8,8)] = "Google Public DNS"
trie["hello", "python"] = object()

list(trie.match((127,0,0,1,2,3)))
## Output; [(4, 'home')]
```

## Radix
A compressed prefix tree. This is a memory efficient data structure compared to `Trie` with same features (but current version is slower that Trie).
