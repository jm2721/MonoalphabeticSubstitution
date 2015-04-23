import fileinput
import sys

# Basic Cryptanalysis

def see_if_fits(word, match, existing_key):
  key = {}
  for k in existing_key:
    key[k] = existing_key[k]
 
  for (i, char) in enumerate(word):
    if char not in key:
      key[char] = match[i]
  
  if apply_key(word, key):
    return key
  return None

def apply_key(word, key):
  decoded = ""
  for i in word:
    try:
      decoded+=key[i]
    except KeyError:
      decoded+=i
  # Search dictionary
  dictionary = open("dictionary.lst", "r")
  for line in dictionary: 
    real_word = line.rstrip()
    if (decoded == real_word):
      return True 
  return False

if __name__ == "__main__":
  for line in fileinput.input():
    encoded_words = line.split(" ")

  non_sorted = []
  for w in encoded_words:
    non_sorted.append(w)

  # sort them in order of size (from largest to smallest)
  # keep a copy of the unsorted version for later
  encoded_words.sort(key=lambda s: -len(s))
  dictionary = open("dictionary.lst", "r")
  # Start building up the key from nothing
  full_key = {}

  seen_characters = ""
  run = False
  for count, word in enumerate(encoded_words):
    for i in word:
      if i not in seen_characters:
        run = True
    if run:
      potential_matches = []
      for dict_word in dictionary:
        dict_word = dict_word.rstrip()
        if (len(dict_word) == len(word)):
          potential_matches.append(dict_word)
      
      dictionary.seek(0)
      
      for match in potential_matches:
        if see_if_fits(word, match, full_key) != None:
          for k in see_if_fits(word, match, full_key):
            full_key[k] = see_if_fits(word, match, full_key)[k]
    for i in word:
      seen_characters+=i
    run = False
  
  dictionary.close()
  for j, word in enumerate(non_sorted):
    decoded = ""
    for i in word:
      try:
        decoded+=full_key[i]
      except KeyError:
        decoded+=i
    if j==0:
      sys.stdout.write(decoded)
    else:
      sys.stdout.write(" " + decoded)
