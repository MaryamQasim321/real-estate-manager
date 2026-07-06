import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar

from excel_manager import ExcelManager

NAVY = "#1E3A5F"
BG = "#F5F7FA"
GREEN = "#28A745"
RED = "#DC3545"
BLUE = "#0D6EFD"
BORDER = "#DDDDDD"

MONTH_NAMES = list(calendar.month_name)[1:]  # January .. December


class ExpenseTracker(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=BG)
        self.pack(fill="both", expand=True)

        self.excel = ExcelManager()

        now = datetime.now()
        self.selected_year = now.year
        self.selected_month = now.month

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.create_header()
        self.create_summary_cards()
        self.create_add_form()
        self.create_table()

        self.refresh()

    # ------------------------------------------------------------------
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=30, pady=(25, 15))
        header.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(title_box, text="Expense Tracker", font=("Arial", 32, "bold"),
                     text_color=NAVY).pack(anchor="w")
        ctk.CTkLabel(title_box, text="Track revenue, expenses, and balance by month",
                     font=("Arial", 16), text_color="gray40").pack(anchor="w")

        selector_box = ctk.CTkFrame(header, fg_color="transparent")
        selector_box.grid(row=0, column=1, sticky="e")

        self.month_var = tk.StringVar(value=MONTH_NAMES[self.selected_month - 1])
        self.year_var = tk.StringVar(value=str(self.selected_year))

        ctk.CTkOptionMenu(
            selector_box, values=MONTH_NAMES, variable=self.month_var,
            width=140, command=self.on_period_change
        ).pack(side="left", padx=(0, 10))

        years = [str(y) for y in range(self.selected_year - 5, self.selected_year + 2)]
        ctk.CTkOptionMenu(
            selector_box, values=years, variable=self.year_var,
            width=100, command=self.on_period_change
        ).pack(side="left")

    def on_period_change(self, _=None):
        self.selected_month = MONTH_NAMES.index(self.month_var.get()) + 1
        self.selected_year = int(self.year_var.get())
        self.refresh()

    # ------------------------------------------------------------------
    def create_summary_cards(self):
        self.revenue_value = tk.StringVar(value="PKR 0")
        self.expense_value = tk.StringVar(value="PKR 0")
        self.balance_value = tk.StringVar(value="PKR 0")

        self.make_card("Total Revenue", self.revenue_value, GREEN).grid(
            row=1, column=0, padx=(30, 15), pady=(0, 15), sticky="nsew")
        self.make_card("Total Expense", self.expense_value, RED).grid(
            row=1, column=1, padx=15, pady=(0, 15), sticky="nsew")
        self.make_card("Current Balance", self.balance_value, BLUE).grid(
            row=1, column=2, padx=(15, 30), pady=(0, 15), sticky="nsew")

    def make_card(self, title, value_var, color):
        card = ctk.CTkFrame(self, corner_radius=18, fg_color="white",
                             border_width=1, border_color=BORDER, height=120)
        ctk.CTkLabel(card, text=title, font=("Arial", 16, "bold"), text_color="gray35").pack(
            anchor="w", padx=20, pady=(18, 4))
        ctk.CTkLabel(card, textvariable=value_var, font=("Arial", 26, "bold"), text_color=color).pack(
            anchor="w", padx=20, pady=(0, 18))
        return card

    # ------------------------------------------------------------------
    def create_add_form(self):
        form = ctk.CTkFrame(self, corner_radius=18, fg_color="white",
                             border_width=1, border_color=BORDER)
        form.grid(row=2, column=0, columnspan=3, padx=30, pady=(0, 15), sticky="ew")
        form.grid_columnconfigure(5, weight=1)

        ctk.CTkLabel(form, text="Add Transaction", font=("Arial", 18, "bold"), text_color=NAVY).grid(
            row=0, column=0, columnspan=6, sticky="w", padx=20, pady=(15, 10))

        ctk.CTkLabel(form, text="Date (YYYY-MM-DD)", font=("Arial", 12), text_color="gray40").grid(
            row=1, column=0, sticky="w", padx=(20, 5))
        self.date_entry = ctk.CTkEntry(form, width=140, placeholder_text="YYYY-MM-DD")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=0, padx=(20, 10), pady=(0, 15), sticky="w")

        ctk.CTkLabel(form, text="Description", font=("Arial", 12), text_color="gray40").grid(
            row=1, column=1, sticky="w", padx=5)
        self.desc_entry = ctk.CTkEntry(form, width=220, placeholder_text="e.g. Rent received")
        self.desc_entry.grid(row=2, column=1, padx=10, pady=(0, 15), sticky="w")

        ctk.CTkLabel(form, text="Type", font=("Arial", 12), text_color="gray40").grid(
            row=1, column=2, sticky="w", padx=5)
        self.type_var = tk.StringVar(value="Revenue")
        ctk.CTkSegmentedButton(form, values=["Revenue", "Expense"], variable=self.type_var,
                                width=180).grid(row=2, column=2, padx=10, pady=(0, 15), sticky="w")

        ctk.CTkLabel(form, text="Amount (PKR)", font=("Arial", 12), text_color="gray40").grid(
            row=1, column=3, sticky="w", padx=5)
        self.amount_entry = ctk.CTkEntry(form, width=140, placeholder_text="0.00")
        self.amount_entry.grid(row=2, column=3, padx=10, pady=(0, 15), sticky="w")

        ctk.CTkButton(form, text="+ Add Transaction", width=160, height=36,
                      command=self.add_transaction).grid(
            row=2, column=4, padx=(10, 20), pady=(0, 15), sticky="w")

    # ------------------------------------------------------------------
    def create_table(self):
        container = ctk.CTkFrame(self, corner_radius=18, fg_color="white",
                                  border_width=1, border_color=BORDER)
        container.grid(row=3, column=0, columnspan=3, padx=30, pady=(0, 25), sticky="nsew")
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        top_row = ctk.CTkFrame(container, fg_color="transparent")
        top_row.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(18, 10))
        top_row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top_row, text="Transactions", font=("Arial", 20, "bold"), text_color=NAVY).grid(
            row=0, column=0, sticky="w")

        ctk.CTkButton(top_row, text="Delete Selected", width=140, height=32,
                      fg_color=RED, hover_color="#B02A37",
                      command=self.delete_selected).grid(row=0, column=1, sticky="e")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview", background="white", fieldbackground="white",
                         foreground="#333333", rowheight=32, borderwidth=0, font=("Arial", 12))
        style.configure("Custom.Treeview.Heading", background="#ECECEC", foreground=NAVY,
                         font=("Arial", 12, "bold"), relief="flat")
        style.map("Custom.Treeview", background=[("selected", "#CDE3FF")],
                  foreground=[("selected", NAVY)])

        columns = ("date", "description", "type", "revenue", "expense", "balance")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", style="Custom.Treeview")

        headers = {
            "date": ("Date", 100),
            "description": ("Description", 260),
            "type": ("Type", 100),
            "revenue": ("Revenue", 120),
            "expense": ("Expense", 120),
            "balance": ("Balance", 120),
        }
        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w" if col in ("date", "description", "type") else "e")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=(20, 0), pady=(0, 20))
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 20), padx=(0, 15))

        self.empty_label = ctk.CTkLabel(container, text="No transactions yet for this month.\nAdd your first revenue or expense above.",
                                         font=("Arial", 14), text_color="gray50")

    # ------------------------------------------------------------------
    def add_transaction(self):
        date_str = self.date_entry.get().strip()
        description = self.desc_entry.get().strip()
        ttype = self.type_var.get()
        amount_str = self.amount_entry.get().strip()

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the date as YYYY-MM-DD.")
            return

        if not description:
            messagebox.showerror("Missing Description", "Please enter a description.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid positive number.")
            return

        entry_year, entry_month = map(int, date_str.split("-")[:2])
        self.excel.add_transaction(entry_year, entry_month, date_str, description, ttype, amount)

        self.desc_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        if entry_year == self.selected_year and entry_month == self.selected_month:
            self.refresh()
        else:
            messagebox.showinfo("Saved", f"Transaction saved to the {entry_year}-{entry_month:02d} sheet.")

    # ------------------------------------------------------------------
    def delete_selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a transaction to delete.")
            return

        item = selection[0]
        transaction_id = self.tree.item(item, "tags")[0]

        if not messagebox.askyesno("Confirm Delete", "Delete this transaction? This cannot be undone."):
            return

        self.excel.delete_transaction(self.selected_year, self.selected_month, int(transaction_id))
        self.refresh()

    # ------------------------------------------------------------------
    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        transactions = self.excel.load_transactions(self.selected_year, self.selected_month)

        if not transactions:
            self.empty_label.grid(row=1, column=0, columnspan=2, sticky="nsew")
        else:
            self.empty_label.grid_forget()

        for t in transactions:
            self.tree.insert("", "end", tags=(str(t["id"]),), values=(
                t["date"], t["description"], t["type"],
                f"PKR {t['revenue']:,.2f}" if t["revenue"] else "-",
                f"PKR {t['expense']:,.2f}" if t["expense"] else "-",
                f"PKR {t['balance']:,.2f}",
            ))

        total_revenue, total_expense, balance = self.excel.get_summary(self.selected_year, self.selected_month)
        self.revenue_value.set(f"PKR {total_revenue:,.2f}")
        self.expense_value.set(f"PKR {total_expense:,.2f}")
        self.balance_value.set(f"PKR {balance:,.2f}")
