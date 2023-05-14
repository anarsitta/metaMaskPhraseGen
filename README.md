# metaMaskPhraseGen

An algorithm that allows you to generate 23 words and then replace them with the words specified in the file pattern.txt , preserving the positions of words.
Then, based on the replaced combination, the 24th word is selected according to the meaning and added to the end of both combinations.

## The output generates 2 files:
`file_with_replace.txt` : a file containing combinations with replacement\
`file_without_replace.txt` : a file containing combinations without replacement\

Used to create a secret phrase in the MetaMask application.

## Files used:
`bip39.txt` - word library used to select the 24th word\
`generate.txt` - a list of words used to create a 23-word phrase\
`pattern.txt` - the number and word used to replace\
`file_with_replace.txt` : a file containing combinations with replacement\
`file_without_replace.txt` : a file containing combinations without replacement
