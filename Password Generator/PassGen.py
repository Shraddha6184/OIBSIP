import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import re

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TCheckbutton', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Password Generator", 
                              font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Password length frame
        length_frame = ttk.LabelFrame(main_frame, text="Password Length", 
                                    padding="10")
        length_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)
        
        self.length_var = tk.StringVar(value="12")
        length_entry = ttk.Entry(length_frame, textvariable=self.length_var, 
                               width=10)
        length_entry.grid(row=0, column=0, padx=5)
        
        length_scale = ttk.Scale(length_frame, from_=8, to=64, 
                               variable=self.length_var, orient='horizontal')
        length_scale.grid(row=0, column=1, sticky='ew', padx=5)
        
        # Character sets frame
        chars_frame = ttk.LabelFrame(main_frame, text="Character Sets", 
                                   padding="10")
        chars_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)
        
        # Character set checkbuttons
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(chars_frame, text="Uppercase (A-Z)", 
                       variable=self.use_uppercase).grid(row=0, column=0, 
                       sticky='w', pady=2)
        ttk.Checkbutton(chars_frame, text="Lowercase (a-z)", 
                       variable=self.use_lowercase).grid(row=1, column=0, 
                       sticky='w', pady=2)
        ttk.Checkbutton(chars_frame, text="Digits (0-9)", 
                       variable=self.use_digits).grid(row=2, column=0, 
                       sticky='w', pady=2)
        ttk.Checkbutton(chars_frame, text="Symbols (!@#$%^&*)", 
                       variable=self.use_symbols).grid(row=3, column=0, 
                       sticky='w', pady=2)
        
        # Advanced options frame
        advanced_frame = ttk.LabelFrame(main_frame, text="Advanced Options", 
                                      padding="10")
        advanced_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=10)
        
        # Excluded characters
        ttk.Label(advanced_frame, text="Exclude characters:").grid(row=0, 
                                                                 column=0, 
                                                                 sticky='w')
        self.exclude_chars = tk.StringVar()
        ttk.Entry(advanced_frame, textvariable=self.exclude_chars).grid(row=0, 
                                                                      column=1, 
                                                                      sticky='ew', 
                                                                      padx=5)
        
        # Minimum requirements frame
        min_req_frame = ttk.LabelFrame(main_frame, text="Minimum Requirements", 
                                     padding="10")
        min_req_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)
        
        self.min_uppercase = tk.StringVar(value="1")
        self.min_lowercase = tk.StringVar(value="1")
        self.min_digits = tk.StringVar(value="1")
        self.min_symbols = tk.StringVar(value="1")
        
        # Minimum requirements entries
        ttk.Label(min_req_frame, text="Min Uppercase:").grid(row=0, column=0, 
                                                           sticky='w')
        ttk.Entry(min_req_frame, textvariable=self.min_uppercase, 
                 width=5).grid(row=0, column=1, padx=5)
        
        ttk.Label(min_req_frame, text="Min Lowercase:").grid(row=1, column=0, 
                                                           sticky='w')
        ttk.Entry(min_req_frame, textvariable=self.min_lowercase, 
                 width=5).grid(row=1, column=1, padx=5)
        
        ttk.Label(min_req_frame, text="Min Digits:").grid(row=2, column=0, 
                                                        sticky='w')
        ttk.Entry(min_req_frame, textvariable=self.min_digits, 
                 width=5).grid(row=2, column=1, padx=5)
        
        ttk.Label(min_req_frame, text="Min Symbols:").grid(row=3, column=0, 
                                                         sticky='w')
        ttk.Entry(min_req_frame, textvariable=self.min_symbols, 
                 width=5).grid(row=3, column=1, padx=5)
        
        # Generated password frame
        password_frame = ttk.LabelFrame(main_frame, text="Generated Password", 
                                      padding="10")
        password_frame.grid(row=5, column=0, columnspan=2, sticky='ew', pady=10)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, 
                                      textvariable=self.password_var, 
                                      font=('Courier', 12))
        self.password_entry.grid(row=0, column=0, sticky='ew', padx=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(buttons_frame, text="Generate Password", 
                  command=self.generate_password).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).grid(row=0, column=1, padx=5)
        
        # Password strength meter
        strength_frame = ttk.LabelFrame(main_frame, text="Password Strength", 
                                      padding="10")
        strength_frame.grid(row=7, column=0, columnspan=2, sticky='ew', pady=10)
        
        self.strength_var = tk.StringVar(value="No password generated")
        strength_label = ttk.Label(strength_frame, 
                                 textvariable=self.strength_var)
        strength_label.grid(row=0, column=0, sticky='ew')
        
    def generate_password(self):
        try:
            length = int(self.length_var.get())
            if length < 8:
                messagebox.showerror("Error", 
                                   "Password length must be at least 8 characters")
                return
                
            # Build character sets
            chars = ''
            if self.use_uppercase.get():
                chars += string.ascii_uppercase
            if self.use_lowercase.get():
                chars += string.ascii_lowercase
            if self.use_digits.get():
                chars += string.digits
            if self.use_symbols.get():
                chars += string.punctuation
                
            # Remove excluded characters
            excluded = self.exclude_chars.get()
            for char in excluded:
                chars = chars.replace(char, '')
                
            if not chars:
                messagebox.showerror("Error", 
                                   "No character set selected")
                return
                
            # Get minimum requirements
            min_upper = int(self.min_uppercase.get())
            min_lower = int(self.min_lowercase.get())
            min_digits = int(self.min_digits.get())
            min_symbols = int(self.min_symbols.get())
            
            # Generate password meeting minimum requirements
            password = []
            
            # Add required characters
            if self.use_uppercase.get():
                password.extend(random.sample(string.ascii_uppercase, min_upper))
            if self.use_lowercase.get():
                password.extend(random.sample(string.ascii_lowercase, min_lower))
            if self.use_digits.get():
                password.extend(random.sample(string.digits, min_digits))
            if self.use_symbols.get():
                password.extend(random.sample(string.punctuation, min_symbols))
                
            # Fill remaining length with random characters
            remaining = length - len(password)
            if remaining > 0:
                password.extend(random.choices(chars, k=remaining))
                
            # Shuffle the password
            random.shuffle(password)
            password = ''.join(password)
            
            self.password_var.set(password)
            self.evaluate_password_strength(password)
            
        except ValueError as e:
            messagebox.showerror("Error", 
                               "Please enter valid numbers for all fields")
            
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", 
                              "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", 
                                 "No password to copy!")
            
    def evaluate_password_strength(self, password):
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
            feedback.append("Good length")
        elif len(password) >= 8:
            score += 1
            feedback.append("Minimum length met")
        
        # Character variety checks
        if re.search(r'[A-Z]', password):
            score += 1
            feedback.append("Contains uppercase")
        if re.search(r'[a-z]', password):
            score += 1
            feedback.append("Contains lowercase")
        if re.search(r'\d', password):
            score += 1
            feedback.append("Contains digits")
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
            feedback.append("Contains symbols")
            
        # Set strength message based on score
        if score >= 5:
            strength = "Strong"
        elif score >= 3:
            strength = "Moderate"
        else:
            strength = "Weak"
            
        self.strength_var.set(f"Strength: {strength}\n" + 
                            "\n".join(feedback))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
