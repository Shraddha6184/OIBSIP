import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator and Tracker")
        self.root.geometry("800x600")
        
        self.init_database()
        
        self.create_frames()
        
        self.create_input_form()
        
        self.create_results_section()
        
        self.create_history_section()
        
        self.create_plot()
        
    def init_database(self):
        """Initialize SQLite database and create necessary tables"""
        self.conn = sqlite3.connect('bmi_data.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date DATETIME,
                weight REAL,
                height REAL,
                bmi REAL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()
    
    def create_frames(self):
        """Create main layout frames"""
        self.left_frame = ttk.Frame(self.root, padding="10")
        self.left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def create_input_form(self):
        """Create input form with validation"""
        ttk.Label(self.left_frame, text="User Name:").grid(row=0, column=0, pady=5)
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(self.left_frame, textvariable=self.user_var)
        self.user_combo.grid(row=0, column=1, pady=5)
        self.update_user_list()
        
        ttk.Label(self.left_frame, text="Weight (kg):").grid(row=1, column=0, pady=5)
        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(self.left_frame, textvariable=self.weight_var)
        self.weight_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.left_frame, text="Height (cm):").grid(row=2, column=0, pady=5)
        self.height_var = tk.StringVar()
        self.height_entry = ttk.Entry(self.left_frame, textvariable=self.height_var)
        self.height_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(self.left_frame, text="Calculate BMI", command=self.calculate_bmi).grid(row=3, column=0, columnspan=2, pady=10)
        
    def create_results_section(self):
        """Create results display section"""
        self.results_frame = ttk.LabelFrame(self.left_frame, text="Results", padding="10")
        self.results_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.bmi_label = ttk.Label(self.results_frame, text="BMI: --")
        self.bmi_label.grid(row=0, column=0, pady=5)
        
        self.category_label = ttk.Label(self.results_frame, text="Category: --")
        self.category_label.grid(row=1, column=0, pady=5)
        
    def create_history_section(self):
        """Create history table view"""
        history_frame = ttk.LabelFrame(self.right_frame, text="History", padding="10")
        history_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.history_tree = ttk.Treeview(history_frame, columns=('Date', 'Weight', 'Height', 'BMI'), show='headings')
        self.history_tree.heading('Date', text='Date')
        self.history_tree.heading('Weight', text='Weight (kg)')
        self.history_tree.heading('Height', text='Height (cm)')
        self.history_tree.heading('BMI', text='BMI')
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
    def create_plot(self):
        """Create matplotlib plot for BMI trend"""
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=10)
        
    def update_user_list(self):
        """Update the user dropdown with all users from database"""
        self.cursor.execute("SELECT name FROM users")
        users = [row[0] for row in self.cursor.fetchall()]
        self.user_combo['values'] = users
        
    def get_or_create_user(self, name):
        """Get user ID or create new user if doesn't exist"""
        self.cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            self.cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            self.conn.commit()
            return self.cursor.lastrowid
            
    def calculate_bmi(self):
        """Calculate BMI and save results"""
        try:
            # Validate inputs
            user_name = self.user_var.get().strip()
            if not user_name:
                messagebox.showerror("Error", "Please enter a user name")
                return
                
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())
            
            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers")
                
            height_m = height / 100
            bmi = weight / (height_m * height_m)
            
            category = self.get_bmi_category(bmi)
            
            self.bmi_label.config(text=f"BMI: {bmi:.1f}")
            self.category_label.config(text=f"Category: {category}")
            
            user_id = self.get_or_create_user(user_name)
            self.cursor.execute("""
                INSERT INTO measurements (user_id, date, weight, height, bmi)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, datetime.now(), weight, height, bmi))
            self.conn.commit()
            
            self.update_history(user_id)
            self.update_plot(user_id)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def get_bmi_category(self, bmi):
        """Determine BMI category"""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
            
    def update_history(self, user_id):
        """Update history table with user's measurements"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        self.cursor.execute("""
            SELECT date, weight, height, bmi 
            FROM measurements 
            WHERE user_id = ? 
            ORDER BY date DESC
        """, (user_id,))
        
        for row in self.cursor.fetchall():
            date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M')
            self.history_tree.insert('', 'end', values=(date, f"{row[1]:.1f}", f"{row[2]:.1f}", f"{row[3]:.1f}"))
            
    def update_plot(self, user_id):
        """Update BMI trend plot"""
        self.cursor.execute("""
            SELECT date, bmi 
            FROM measurements 
            WHERE user_id = ? 
            ORDER BY date ASC
        """, (user_id,))
        
        dates, bmis = zip(*self.cursor.fetchall())
        dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') for date in dates]
        
        self.ax.clear()
        self.ax.plot(dates, bmis, 'b-o')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('BMI')
        self.ax.set_title('BMI Trend')
        plt.xticks(rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
