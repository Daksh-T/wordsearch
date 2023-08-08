# Word Search Puzzle Generator

This program generates a word search puzzle using random words fetched from API Ninjas' Random Word API. The words are placed horizontally, vertically, and diagonally in a grid, with the possibility of being placed backward as well. 

The grid size is calculated based on the longest word in the list, with some additional space for better placement. The program also lists the words placed in the puzzle at the end.

## Requirements

- Python 3.x
- `requests` library

## Usage

1. Install the `requests` library if you haven't already:

```
pip install requests
```

2. Replace `YOUR_API_KEY` in the `get_random_word` function with your API key from the [API Ninjas](https://api-ninjas.com) website.

3. Run the script:

```
python wordsearch.py
```
for the TUI version

or

```
python gui.py
```
for the GUI version

4. The script will generate a word search puzzle grid and print it to the console, followed by a list of the words placed in the puzzle in a box.
The GUI version prints a grid on the right side and a list of words that are to be searched for, on the left. You can enter words into the input box as you find them. If the word you entered is found in the list, the word found will turn green in the list. Else if the word is not present in the list, the input box will turn red.

## Customization

- You can customize the number of words fetched by changing the argument passed to the `get_valid_words` function in line 97 of the script (line 214 for GUI)
```python
words = get_valid_words(8)        # Default is 8 words
```
- You can also customize the extra space added to the grid by changing the number added to the value returned from the `get_longest_word` function in line 18 of the script (line 38 for GUI)
```python
    return max(len(word) for word in words) + 3        # Default is 3
```

There is no GUI settings page to adjust these yet.
