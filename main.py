# Random Password Generator with GUI (Advanced Version)
# -----------------------------------------------------
# Tech Stack: Python, Tkinter, secrets, string, pyperclip

import tkinter as tk
from tkinter import messagebox, ttk
import string
import secrets
import pyperclip
from tkinter.font import Font

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
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Password settings
        self.current_password = ""
        self.password_visible = False  # Start with hidden password
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#1a1a2e')
        self.style.configure('Custom.TLabel', background='#1a1a2e', foreground='#ffffff', font=('Segoe UI', 10))
        
        # Configure button styles
        self.style.configure('Custom.TButton',
                           background='#4CAF50',
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'),
                           padding=10,
                           borderwidth=0)
        
        self.style.map('Custom.TButton',
                      background=[('active', '#45a049'), ('pressed', '#3d8b40')],
                      foreground=[('active', 'white'), ('pressed', 'white')])
        
        # Main container with padding
        self.main_frame = ttk.Frame(root, style='Custom.TFrame', padding="20")
        self.main_frame.pack(fill='both', expand=True)
        
        # Title
        title_font = Font(family='Segoe UI', size=16, weight='bold')
        title_label = ttk.Label(self.main_frame, 
                              text="Password Generator",
                              font=title_font,
                              style='Custom.TLabel')
        title_label.pack(pady=(0, 20))

        # Length frame
        length_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        length_frame.pack(fill='x', pady=5)
        
        ttk.Label(length_frame, 
                 text="Password Length:",
                 style='Custom.TLabel').pack(side='left', padx=5)
        
        self.length_entry = ttk.Entry(length_frame, 
                                    font=('Segoe UI', 10),
                                    width=10)
        self.length_entry.pack(side='left', padx=5)
        self.length_entry.insert(0, "12")

        # Character options frame
        options_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        options_frame.pack(fill='x', pady=10)
        
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)

        # Custom checkbox style
        checkbox_style = {'font': ('Segoe UI', 10),
                         'bg': '#1a1a2e',
                         'fg': '#ffffff',
                         'selectcolor': '#1a1a2e',
                         'activebackground': '#1a1a2e',
                         'activeforeground': '#ffffff'}

        tk.Checkbutton(options_frame, 
                      text="Include Uppercase Letters",
                      variable=self.upper_var,
                      **checkbox_style).pack(anchor='w', pady=2)
        tk.Checkbutton(options_frame,
                      text="Include Lowercase Letters",
                      variable=self.lower_var,
                      **checkbox_style).pack(anchor='w', pady=2)
        tk.Checkbutton(options_frame,
                      text="Include Numbers",
                      variable=self.digits_var,
                      **checkbox_style).pack(anchor='w', pady=2)
        tk.Checkbutton(options_frame,
                      text="Include Symbols",
                      variable=self.symbols_var,
                      **checkbox_style).pack(anchor='w', pady=2)

        # Exclude characters frame
        exclude_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        exclude_frame.pack(fill='x', pady=10)
        
        ttk.Label(exclude_frame,
                 text="Exclude Characters (optional):",
                 style='Custom.TLabel').pack(anchor='w', pady=5)
        
        self.exclude_entry = ttk.Entry(exclude_frame,
                                     font=('Segoe UI', 10))
        self.exclude_entry.pack(fill='x', pady=5)

        # Generate button frame - moved here
        generate_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        generate_frame.pack(fill='x', pady=10)
        
        generate_btn = tk.Button(generate_frame,
                               text="🔐 Generate New Password",
                               command=self.handle_generate,
                               font=('Segoe UI', 12, 'bold'),
                               bg='#2196F3',
                               fg='white',
                               activebackground='#1976D2',
                               activeforeground='white',
                               relief='flat',
                               padx=25,
                               pady=12,
                               cursor='hand2',
                               width=25)
        generate_btn.pack(fill='x', pady=5)

        # Output frame with visibility toggle
        output_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        output_frame.pack(fill='x', pady=20)
        
        # Password display frame
        password_frame = ttk.Frame(output_frame, style='Custom.TFrame')
        password_frame.pack(fill='x')
        
        # Password entry with custom styling
        self.output_box = ttk.Entry(password_frame,
                                  font=('Segoe UI', 14),
                                  justify='center',
                                  show='*')
        self.output_box.pack(side='left', fill='x', expand=True)
        
        # Enhanced visibility toggle button
        self.eye_btn = tk.Button(password_frame,
                                text="👁️",
                                command=self.toggle_password_visibility,
                                font=('Segoe UI', 16),
                                bg='#1a1a2e',
                                fg='white',
                                activebackground='#2a2a3e',
                                activeforeground='white',
                                relief='flat',
                                padx=12,
                                pady=5,
                                cursor='hand2',
                                width=3)
        self.eye_btn.pack(side='right', padx=(5, 0))

        # Copy button frame
        copy_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        copy_frame.pack(fill='x', pady=10)
        
        copy_btn = tk.Button(copy_frame,
                           text="📋 Copy to Clipboard",
                           command=self.copy_to_clipboard,
                           font=('Segoe UI', 12, 'bold'),
                           bg='#4CAF50',
                           fg='white',
                           activebackground='#45a049',
                           activeforeground='white',
                           relief='flat',
                           padx=25,
                           pady=12,
                           cursor='hand2',
                           width=25)
        copy_btn.pack(fill='x', pady=5)

        # Configure root window
        self.root.configure(bg='#1a1a2e')
        
        # Add hover effects
        for btn in [generate_btn, copy_btn]:
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#1976D2' if b == generate_btn else '#45a049'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='#2196F3' if b == generate_btn else '#4CAF50'))

    def toggle_password_visibility(self):
        """Toggle password visibility with improved icon feedback"""
        if not self.current_password:  # Don't toggle if no password
            return
            
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.output_box.configure(show='')  # Show password
            self.eye_btn.configure(text="🙈")  # See-no-evil monkey when visible
            # Highlight the password field to make it more visible
            self.output_box.configure(foreground='#4CAF50')
        else:
            self.output_box.configure(show='*')  # Hide password
            self.eye_btn.configure(text="👁️")  # Eye when hidden
            self.output_box.configure(foreground='#ffffff')

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
            
            # Store the new password
            self.current_password = password
            
            # Update display
            self.output_box.delete(0, tk.END)
            self.output_box.insert(0, password)
            
            # Start with hidden password
            self.password_visible = False
            self.output_box.configure(show='*')
            self.eye_btn.configure(text="👁️")
            self.output_box.configure(foreground='#ffffff')
            
            # Show success animation
            self.output_box.configure(foreground='#4CAF50')
            self.root.after(1000, lambda: self.output_box.configure(foreground='#ffffff'))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_to_clipboard(self):
        password = self.current_password
        if password:
            pyperclip.copy(password)
            # Show success animation
            self.output_box.configure(foreground='#4CAF50')
            self.root.after(1000, lambda: self.output_box.configure(foreground='#ffffff'))
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "Generate a password first.")

# === RUN APP ===
if __name__ == '__main__':
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
