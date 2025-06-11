# Random Password Generator with GUI (Advanced Version)
# -----------------------------------------------------
# Tech Stack: Python, Tkinter, secrets, string, pyperclip

import tkinter as tk
from tkinter import messagebox
import string
import secrets
import pyperclip

# === PASSWORD GENERATOR LOGIC ===
def generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_chars):
    if not (use_upper or use_lower or use_digits or use_symbols):
        raise ValueError("At least one character set must be selected.")

    char_pool = ''
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    # Exclude unwanted characters
    for ch in exclude_chars:
        char_pool = char_pool.replace(ch, '')

    if not char_pool:
        raise ValueError("Character pool is empty after exclusions.")

    password = ''.join(secrets.choice(char_pool) for _ in range(length))
    return password

# === GUI APPLICATION ===
class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        # Length
        tk.Label(root, text="Password Length:").pack(pady=5)
        self.length_entry = tk.Entry(root)
        self.length_entry.pack()
        self.length_entry.insert(0, "12")

        # Character options
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)

        tk.Checkbutton(root, text="Include Uppercase Letters", variable=self.upper_var).pack(anchor='w', padx=20)
        tk.Checkbutton(root, text="Include Lowercase Letters", variable=self.lower_var).pack(anchor='w', padx=20)
        tk.Checkbutton(root, text="Include Numbers", variable=self.digits_var).pack(anchor='w', padx=20)
        tk.Checkbutton(root, text="Include Symbols", variable=self.symbols_var).pack(anchor='w', padx=20)

        # Exclude characters
        tk.Label(root, text="Exclude Characters (optional):").pack(pady=5)
        self.exclude_entry = tk.Entry(root)
        self.exclude_entry.pack()

        # Output
        self.output_box = tk.Entry(root, font=("Courier", 14), justify='center')
        self.output_box.pack(pady=20, padx=20, fill='x')

        # Buttons
        tk.Button(root, text="Generate Password", command=self.handle_generate).pack(pady=5)
        tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=5)

    def handle_generate(self):
        try:
            length = int(self.length_entry.get())
            if length < 4:
                raise ValueError("Password length must be at least 4 characters.")

            password = generate_password(
                length=length,
                use_upper=self.upper_var.get(),
                use_lower=self.lower_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get(),
                exclude_chars=self.exclude_entry.get()
            )
            self.output_box.delete(0, tk.END)
            self.output_box.insert(0, password)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_to_clipboard(self):
        password = self.output_box.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "Generate a password first.")

# === RUN APP ===
if __name__ == '__main__':
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
