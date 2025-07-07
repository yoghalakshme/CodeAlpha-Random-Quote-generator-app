import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import random

# === SETTINGS ===
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BACKGROUND_IMAGES = ["bg1.jpg", "bg2.jpg", "bg3.jpg","bg4.jpg","bg5.jpg","bg6.jpg"]  # Add your own image files here!

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_IMAGES = [os.path.join(SCRIPT_DIR, img) for img in BACKGROUND_IMAGES]

# === QUOTES LIST ===
quotes = [
    {"quote": "The best way to predict the future is to invent it.", "author": "Alan Kay"},
    {"quote": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
    {"quote": "Success is not final, failure is not fatal: It is the courage to continue that counts.", "author": "Winston Churchill"},
    {"quote": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
    {"quote": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson"},
    {"quote": "Strive not to be a success, but rather to be of value.", "author": "Albert Einstein"},
]

favorites = []  # saved quotes

# === TK MAIN WINDOW ===
root = tk.Tk()
root.title("Random Quote Generator with Favorites")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)

# === CANVAS ===
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

# === Helper: Load and resize image ===
def load_image(path):
    img = Image.open(path)
    img = img.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)
    return img

# === Helper: Add semi-transparent box onto image ===
def add_transparent_box(image, box_coords, color=(0, 0, 0), opacity=140):
    image = image.convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    r, g, b = color
    draw.rectangle(box_coords, fill=(r, g, b, opacity))
    combined = Image.alpha_composite(image, overlay)
    return combined.convert("RGB")

# === Set background with text ===
def set_background_image(new_img, quote_text, author_text):
    global bg_photo
    bg_photo = ImageTk.PhotoImage(new_img)
    canvas.delete("all")

    # 1. Background Image (with overlay baked in)
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)

    # 2. Quote text
    canvas.create_text(
        300, 180,
        text=f'"{quote_text}"',
        font=("Georgia", 16, "italic"),
        fill="white",
        width=480,
        justify="center"
    )

    # 3. Author text
    canvas.create_text(
        300, 230,
        text=f'- {author_text}',
        font=("Georgia", 14, "bold"),
        fill="white"
    )

    # 4. Buttons on top
    canvas.create_window(150, 360, window=btn_new)
    canvas.create_window(300, 360, window=btn_save)
    canvas.create_window(450, 360, window=btn_view)

# === SHOW NEW RANDOM QUOTE ===
def get_new_quote():
    global current_quote

    # Pick random quote & image
    current_quote = random.choice(quotes)
    new_image_path = random.choice(BACKGROUND_IMAGES)

    new_bg_image = load_image(new_image_path)

    # Add semi-transparent overlay for text box
    new_bg_image = add_transparent_box(
        new_bg_image,
        box_coords=(50, 140, 550, 260),
        color=(0, 0, 0),
        opacity=140
    )

    set_background_image(new_bg_image, current_quote["quote"], current_quote["author"])

# === SAVE TO FAVORITES ===
def save_to_favorites():
    if current_quote not in favorites:
        favorites.append(current_quote)
        messagebox.showinfo("Saved!", "Quote added to favorites!")
    else:
        messagebox.showinfo("Info", "This quote is already in favorites.")

# === VIEW FAVORITES ===
def view_favorites():
    if not favorites:
        messagebox.showinfo("Favorites", "You don't have any favorites yet!")
        return

    fav_win = tk.Toplevel(root)
    fav_win.title("My Favorite Quotes")
    fav_win.geometry("500x400")
    fav_win.configure(bg="#f9f9f9")

    tk.Label(fav_win, text="Your Favorite Quotes", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=10)

    text_box = tk.Text(fav_win, wrap="word", font=("Helvetica", 12), bg="#ffffff", relief="sunken")
    text_box.pack(padx=10, pady=10, fill="both", expand=True)

    for i, q in enumerate(favorites, 1):
        text_box.insert("end", f'{i}. "{q["quote"]}"\n   - {q["author"]}\n\n')
    text_box.config(state="disabled")

# === BUTTONS ===
btn_new = tk.Button(root, text="New Quote", command=get_new_quote, bg="#4a90e2", fg="white", font=("Helvetica", 12))
btn_save = tk.Button(root, text="Save to Favorites", command=save_to_favorites, bg="#50b35e", fg="white", font=("Helvetica", 12))
btn_view = tk.Button(root, text="View Favorites", command=view_favorites, bg="#f39c12", fg="white", font=("Helvetica", 12))

# === FIRST QUOTE ===
current_quote = None
get_new_quote()

# === RUN ===
root.mainloop()