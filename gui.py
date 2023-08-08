import tkinter as tk
from tkinter import Canvas, Frame, Button, Listbox, Entry, StringVar
import requests
import random
import string
import json
import queue
import threading

# Define the global words list
words = []

# grid
grid = []

# Define found words list
found_words = {}  # Format: {"WORD": [(x1, y1), (x2, y2), ...]}
word_coordinates = {}

# Create the main window
window = None

# Create queue
update_queue = queue.Queue()

# Original functions

def get_random_word():
    api_url = 'https://api.api-ninjas.com/v1/randomword'
    response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
    if response.status_code == requests.codes.ok:
        json_response = json.loads(response.text)
        return json_response["word"]
    else:
        return None

def get_longest_word(words):
    return max(len(word) for word in words) + 3

def print_words_periodically():
    """Print the words list and schedule itself to run again. For debugging purposes, not to be called in prod"""
    global window
    print(words)
    window.after(3000, print_words_periodically)

def get_valid_words(count):
    words = []
    while len(words) < count:
        word = get_random_word()
        if word:
            words.append(word.upper())  # Convert word to uppercase before appending
    return words

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

def generate_grid(words, size):
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    local_word_coordinates = {}  # This will store the coordinates of each word

    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            orientation = random.choice(['horizontal', 'vertical', 'diagonal'])
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            backward = random.choice([True, False])

            if is_valid_placement(grid, word, row, col, orientation, size, backward):
                coords = []  # This will store the coordinates for this word
                if orientation == 'horizontal':
                    for i, letter in enumerate(word):
                        x = col + i * (1 if not backward else -1)
                        y = row
                        grid[y][x] = letter.upper()
                        coords.append((y, x))
                elif orientation == 'vertical':
                    for i, letter in enumerate(word):
                        x = col
                        y = row + i * (1 if not backward else -1)
                        grid[y][x] = letter.upper()
                        coords.append((y, x))
                else:  # diagonal
                    for i, letter in enumerate(word):
                        x = col + i * (1 if not backward else -1)
                        y = row + i * (1 if not backward else -1)
                        grid[y][x] = letter.upper()
                        coords.append((y, x))
                local_word_coordinates[word] = coords  # Store the coordinates for this word
                placed = True
            attempts += 1

    for i in range(size):
        for j in range(size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice(string.ascii_uppercase)

    return grid, local_word_coordinates

# GUI functions

def create_grid_canvas(grid, canvas, word_coordinates=None):
    """Draws the word search grid on the canvas."""
    rows, cols = len(grid), len(grid[0])
    cell_size = min(500 / rows, 30)  # Adjusting cell size based on grid size
    canvas.delete("all")  # Clearing the canvas

    # Draw the grid
    for i in range(rows + 1):
        canvas.create_line(i * cell_size, 0, i * cell_size, rows * cell_size)
    for j in range(cols + 1):
        canvas.create_line(0, j * cell_size, cols * cell_size, j * cell_size)

    # Populate the grid with letters
    for i in range(rows):
        for j in range(cols):
            is_highlighted = any(word for word, coords in found_words.items() if (i, j) in coords)
            if is_highlighted:
                # Draw a yellow rectangle (or any color of your choice) behind the letter
                canvas.create_rectangle(j * cell_size, i * cell_size, (j+1) * cell_size, (i+1) * cell_size, fill="yellow")
            canvas.create_text((j + 0.5) * cell_size, (i + 0.5) * cell_size, text=grid[i][j])

def get_word_coordinates(grid, word):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == word[0]:  # If the first letter matches
                # Check all three orientations
                if is_word_at_position(grid, word, i, j, "horizontal"):
                    return [(i, j + k) for k in range(len(word))]
                elif is_word_at_position(grid, word, i, j, "vertical"):
                    return [(i + k, j) for k in range(len(word))]
                elif is_word_at_position(grid, word, i, j, "diagonal"):
                    return [(i + k, j + k) for k in range(len(word))]
    return []

def is_word_at_position(grid, word, row, col, orientation):
    if orientation == "horizontal" and col + len(word) <= len(grid[0]):
        return grid[row][col:col + len(word)] == list(word)
    elif orientation == "vertical" and row + len(word) <= len(grid):
        return [grid[row + i][col] for i in range(len(word))] == list(word)
    elif orientation == "diagonal" and row + len(word) <= len(grid) and col + len(word) <= len(grid[0]):
        return [grid[row + i][col + i] for i in range(len(word))] == list(word)
    return False

def submit_word():
    """Handle word submission."""
    global words, word_coordinates, found_words, grid
    word = word_entry_var.get().upper()
    if word in words:
        index = words.index(word)
        word_listbox.itemconfig(index, {"bg": "green"})  # Change the color to green
        word_entry.config(bg="white")  # Reset the Entry background color to white        
        if word in word_coordinates:  # Check if word exists in word_coordinates
            found_words[word] = word_coordinates[word]
        create_grid_canvas(grid, grid_canvas, word_coordinates)
    else:
        word_entry.config(bg="red")  # Change the Entry background color to red
    if all_words_found():
        display_completion_prompt()

def all_words_found():
    for i in range(word_listbox.size()):
        if word_listbox.itemcget(i, "bg") != "green":  # If any word is not marked as found
            return False
    return True

def display_completion_prompt():
    prompt = tk.Toplevel(window)
    prompt.title("Congratulations!")
    label = tk.Label(prompt, text="Congratulations, would you like to try again?")
    label.pack(pady=20)
    regenerate_button = Button(prompt, text="Regenerate", command=lambda: [generate_puzzle(), prompt.destroy()])
    regenerate_button.pack(side=tk.LEFT, padx=10)
    quit_button = Button(prompt, text="Quit", command=window.quit)
    quit_button.pack(side=tk.RIGHT, padx=10)

def display_word_list(words, listbox):
    """Displays the list of words to find in a listbox."""
    listbox.delete(0, tk.END)  # Clear existing words
    for word in words:
        listbox.insert(tk.END, word)

def generate_puzzle():
    """Start a new thread for puzzle generation."""
    threading.Thread(target=generate_puzzle_threaded).start()

def generate_puzzle_threaded():
    global grid
    global words, word_coordinates, found_words  # Add found_words to the global declarations
    
    # Clear found_words
    found_words.clear()
    
    words = get_valid_words(8)
    grid_size = get_longest_word(words)
    grid, word_coordinates = generate_grid(words, grid_size)
    
    # Update the GUI in the main thread
    update_queue.put((grid, word_coordinates))

def update_gui(grid, word_coordinates=None):
    """Update the GUI elements."""
    create_grid_canvas(grid, grid_canvas, word_coordinates)
    display_word_list(words, word_listbox)

def check_queue():
    global window, update_queue
    try:
        grid, word_coordinates = update_queue.get_nowait()
        update_gui(grid, word_coordinates)
    except queue.Empty:
        pass
    window.after(100, check_queue)

def initialize_gui():
    """Sets up the main GUI window and widgets."""
    global window
    window = tk.Tk()
    window.title("Word Search Puzzle")

    # Frame for holding Listbox, Entry, and Submit button
    left_frame = Frame(window)
    left_frame.pack(side=tk.LEFT, padx=20, pady=20)

    # Listbox for the word list inside the left frame
    global word_listbox
    word_listbox = Listbox(left_frame)
    word_listbox.pack(pady=20)

    # Entry for word input inside the left frame
    global word_entry_var
    word_entry_var = StringVar()
    global word_entry
    word_entry = Entry(left_frame, textvariable=word_entry_var)
    word_entry.pack(pady=10)

    # Button for word submission inside the left frame
    submit_button = Button(left_frame, text="Submit Word", command=submit_word)
    submit_button.pack(pady=10)

    # Button for generating the puzzle
    generate_button = Button(window, text="Generate Puzzle", command=generate_puzzle)
    generate_button.pack(pady=20)

    # Canvas for the word search grid
    global grid_canvas
    grid_canvas = Canvas(window, bg="white", width=500, height=500)  # Adjust size as needed
    grid_canvas.pack(side=tk.RIGHT, pady=20)
    
    check_queue()
    
    window.mainloop()

# Start the GUI
initialize_gui()