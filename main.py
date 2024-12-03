import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from PIL import Image, ImageTk


class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("870x850")
        self.root.configure(bg="white")

        self.transactions = []
        self.load_transactions()

        # Logo
        logo_image = Image.open("/Users/galileaalmaraz/PycharmProjects/budgetTracker/logo.png")
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_label = tk.Label(root, image=self.logo_photo, bg="white")
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Title
        self.title_label = tk.Label(root, text="", font=("Helvetica", 24, "bold"), fg="#1D83FF", bg="white")
        self.title_label.grid(row=0, column=1, pady=10, sticky="w")

        # Tabs for Expenses, Income, and Savings
        self.tab_control = ttk.Notebook(root)
        self.expense_frame = tk.Frame(self.tab_control, bg="white")
        self.income_frame = tk.Frame(self.tab_control, bg="white")
        self.savings_frame = tk.Frame(self.tab_control, bg="white")

        # Add tabs with their respective frames
        self.tab_control.add(self.expense_frame, text='Expenses')
        self.tab_control.add(self.income_frame, text='Income')
        self.tab_control.add(self.savings_frame, text='Savings')
        self.tab_control.grid(row=1, column=0, padx=20, pady=10, sticky="nw")

        # Inputs for each tab
        self.create_input_section(self.expense_frame, has_category=True)
        self.create_input_section(self.income_frame, has_category=False)
        self.create_input_section(self.savings_frame, has_category=False)

        # Pie Chart
        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        self.pie_canvas = FigureCanvasTkAgg(self.fig, root)
        self.pie_canvas.get_tk_widget().grid(row=1, column=1, padx=10, pady=10, sticky="ne")
        self.update_pie_chart()

        # Transaction Log
        self.transaction_log_label = tk.Label(root, text="Transaction Log", font=("Helvetica", 16, "bold"),
                                              fg="#1D83FF", bg="white")
        self.transaction_log_label.grid(row=2, column=0, columnspan=2, pady=(20, 5))

        columns = ('Date', 'Type', 'Amount', 'Category', 'Notes')
        self.transaction_tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
        for col in columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=150)
        self.transaction_tree.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
        self.populate_transaction_log()

        # Scrollbar for transaction log
        self.scrollbar = ttk.Scrollbar(root, orient='vertical', command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=3, column=2, sticky='ns', pady=10)

        # Edit and Delete Buttons
        self.edit_button = tk.Button(root, text="Edit", command=self.edit_transaction)
        self.edit_button.grid(row=4, column=0, padx=20, pady=10, sticky='w')

        self.delete_button = tk.Button(root, text="Delete", command=self.delete_transaction)
        self.delete_button.grid(row=4, column=1, padx=20, pady=10, sticky='e')

    def create_input_section(self, frame, has_category):
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Date input
        tk.Label(frame, text="Date", bg="white").grid(row=0, column=0, sticky='w', pady=5)
        cal = Calendar(frame, selectmode='day')
        cal.grid(row=0, column=1, pady=5)

        # Category input (only for Expenses)
        if has_category:
            tk.Label(frame, text="Category", bg="white").grid(row=1, column=0, sticky='w', pady=5)
            category_input = ttk.Combobox(frame)
            category_input['values'] = ('Rent', 'Groceries', 'Travel', 'Utilities', 'Others')
            category_input.grid(row=1, column=1, pady=5)
        else:
            category_input = None

        # Amount input
        tk.Label(frame, text="Amount", bg="white").grid(row=2, column=0, sticky='w', pady=5)
        amount_input = tk.Entry(frame)
        amount_input.grid(row=2, column=1, pady=5)

        # Notes input
        tk.Label(frame, text="Notes", bg="white").grid(row=3, column=0, sticky='w', pady=5)
        notes_input = tk.Entry(frame)
        notes_input.grid(row=3, column=1, pady=5)

        # Submit button
        submit_button = tk.Button(frame, text="Submit", command=lambda: self.add_transaction(cal, amount_input, category_input, notes_input, frame))
        submit_button.grid(row=4, column=1, pady=10)

    def add_transaction(self, cal, amount_input, category_input, notes_input, parent):
        date = cal.get_date()
        amount = amount_input.get()
        notes = notes_input.get()
        category = category_input.get() if category_input else ''
        t_type = 'Expenses' if parent == self.expense_frame else ('Income' if parent == self.income_frame else 'Savings')

        if date and amount:
            try:
                amount = float(amount)
            except ValueError:
                return  # If amount is not a number, do nothing

            transaction = {
                'date': date,
                'type': t_type,
                'amount': amount,
                'category': category,
                'notes': notes
            }
            self.transactions.append(transaction)
            self.save_transactions()
            self.populate_transaction_log()
            self.update_pie_chart()

    def populate_transaction_log(self):
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        for i, transaction in enumerate(self.transactions):
            if isinstance(transaction, dict):  # Ensure each transaction is a dictionary
                self.transaction_tree.insert('', 'end', iid=i, values=(
                    transaction.get('date', ''), transaction.get('type', ''), transaction.get('amount', 0),
                    transaction.get('category', ''), transaction.get('notes', '')
                ))

    def edit_transaction(self):
        selected_items = self.transaction_tree.selection()
        if not selected_items:
            return
        item = selected_items[0]
        selected_transaction = self.transactions[int(item)]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Transaction")
        edit_window.geometry("300x300")

        tk.Label(edit_window, text="Date").grid(row=0, column=0, pady=5)
        cal = Calendar(edit_window, selectmode='day')
        cal.grid(row=0, column=1, pady=5)
        cal.set_date(selected_transaction.get('date', ''))

        tk.Label(edit_window, text="Amount").grid(row=1, column=0, pady=5)
        amount_entry = tk.Entry(edit_window)
        amount_entry.grid(row=1, column=1, pady=5)
        amount_entry.insert(0, selected_transaction.get('amount', 0))

        tk.Label(edit_window, text="Category").grid(row=2, column=0, pady=5)
        category_entry = ttk.Combobox(edit_window)
        category_entry['values'] = ('Rent', 'Groceries', 'Travel', 'Utilities', 'Others')
        category_entry.grid(row=2, column=1, pady=5)
        category_entry.set(selected_transaction.get('category', ''))

        tk.Label(edit_window, text="Notes").grid(row=3, column=0, pady=5)
        notes_entry = tk.Entry(edit_window)
        notes_entry.grid(row=3, column=1, pady=5)
        notes_entry.insert(0, selected_transaction.get('notes', ''))

        def save_changes():
            try:
                selected_transaction['date'] = cal.get_date()
                selected_transaction['amount'] = float(amount_entry.get())
                selected_transaction['category'] = category_entry.get()
                selected_transaction['notes'] = notes_entry.get()
                self.save_transactions()
                self.populate_transaction_log()
                self.update_pie_chart()
                edit_window.destroy()
            except ValueError:
                return  # If amount is not valid, do nothing

        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=4, column=1, pady=10)

    def delete_transaction(self):
        selected_items = self.transaction_tree.selection()
        if not selected_items:
            return
        item = selected_items[0]
        del self.transactions[int(item)]
        self.save_transactions()
        self.populate_transaction_log()
        self.update_pie_chart()

    def update_pie_chart(self):
        self.ax.clear()
        income = sum(float(t['amount']) for t in self.transactions if isinstance(t, dict) and t.get('type') == 'Income')
        expenses = sum(float(t['amount']) for t in self.transactions if isinstance(t, dict) and t.get('type') == 'Expenses')
        savings = max(income - expenses, 0)

        if income == 0 and expenses == 0 and savings == 0:
            sizes = []
            labels = []
        else:
            sizes = [income, expenses, savings]
            labels = ['Income', 'Expenses', 'Savings']
            colors = ['#DE7ED1', '#1D83FF', '#FFA857']
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            self.ax.axis('equal')
        self.pie_canvas.draw()

    def save_transactions(self):
        with open('transactions.json', 'w') as f:
            json.dump(self.transactions, f)

    def load_transactions(self):
        try:
            with open('transactions.json', 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.transactions = [t for t in data if isinstance(t, dict)]
                else:
                    self.transactions = []
        except FileNotFoundError:
            self.transactions = []


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTracker(root)
    root.mainloop()
