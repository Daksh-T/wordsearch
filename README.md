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

4. The script will generate a word search puzzle grid and print it to the console, followed by a list of the words placed in the puzzle in a box.

## Customization

- You can customize the number of words fetched by changing the argument passed to the `get_valid_words` function in line 97 of the script. The default value is 8.
```python
words = get_valid_words(8) # Fetch 8 words for the puzzle
```
- You can also customize the extra space added to the grid by changing the number added to the value returned from the `get_longest_word` function in line 18 of the script. The default setting is 3.
```python
    return max(len(word) for word in words) + 3
```
