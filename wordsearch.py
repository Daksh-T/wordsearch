import requests
import random
import string
import json

# Fetch a random word from the API
def get_random_word():
    api_url = 'https://api.api-ninjas.com/v1/randomword'
    response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
    if response.status_code == requests.codes.ok:
        json_response = json.loads(response.text)
        return json_response["word"]
    else:
        return None

# Determine the grid size based on the longest word
def get_longest_word(words):
    return max(len(word) for word in words) + 3

# Fetch the specified number of valid words from the API
def get_valid_words(count):
    words = []
    while len(words) < count:
        word = get_random_word()
        if word:
            words.append(word)
    return words

# Check if the word can be placed at the specified position without overlapping or going out of bounds
def is_valid_placement(grid, word, row, col, orientation, size, backward):
    direction = -1 if backward else 1
    if orientation == 'horizontal':
        if col + len(word) * direction > size or col + len(word) * direction < 0:
            return False
        for i in range(len(word)):
            if grid[row][col + i * direction] != ' ' and grid[row][col + i * direction] != word[i].upper():
                return False
    elif orientation == 'vertical':
        if row + len(word) * direction > size or row + len(word) * direction < 0:
            return False
        for i in range(len(word)):
            if grid[row + i * direction][col] != ' ' and grid[row + i * direction][col] != word[i].upper():
                return False
    else:  # diagonal
        if row + len(word) * direction >= size or row + len(word) * direction < 0 or col + len(word) * direction >= size or col + len(word) * direction < 0:
            return False
        for i in range(len(word)):
            if grid[row + i * direction][col + i * direction] != ' ' and grid[row + i * direction][col + i * direction] != word[i].upper():
                return False
    return True

# Generate the word search grid with the given words and grid size
def generate_grid(words, size):
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    
    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            orientation = random.choice(['horizontal', 'vertical', 'diagonal'])
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            backward = random.choice([True, False])

            if is_valid_placement(grid, word, row, col, orientation, size, backward):
                if orientation == 'horizontal':
                    for i, letter in enumerate(word):
                        grid[row][col + i * (1 if not backward else -1)] = letter.upper()
                elif orientation == 'vertical':
                    for i, letter in enumerate(word):
                        grid[row + i * (1 if not backward else -1)][col] = letter.upper()
                else:  # diagonal
                    for i, letter in enumerate(word):
                        grid[row + i * (1 if not backward else -1)][col + i * (1 if not backward else -1)] = letter.upper()
                placed = True
            attempts += 1

    for i in range(size):
        for j in range(size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice(string.ascii_uppercase)

    return grid

# Print the generated grid and word-list for the words
def print_grid(grid, words):
    for row in grid:
        print(" ".join(row))
    
    print("\nWords::\n")
    print("+{:-^30}+".format(''))
    for word in words:
        print("| {: <28} |".format(word.upper()))
    print("+{:-^30}+".format(''))

# Main program
words = get_valid_words(8) # Fetch 8 words for the puzzle
grid_size = get_longest_word(words) # Determine the grid size
grid = generate_grid(words, grid_size) # Generate the puzzle grid
print_grid(grid, words) # Print the grid and word-list