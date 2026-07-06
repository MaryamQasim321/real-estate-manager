import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

NAVY = "#1E3A5F"
BG = "#F5F7FA"
GREEN = "#28A745"
RED = "#DC3545"
BLUE = "#0D6EFD"
BORDER = "#DDDDDD"


class PlotDetailWindow(ctk.CTkToplevel):
    """Popup window showing the full payment history for a single plot,
    with a form to add new installments and a button to remove one."""

    def __init__(self, parent, excel_manager, block_name, plot, on_change=None):
        super().__init__(parent)

        self.excel = excel_manager
        self.block_name = block_name
        self.plot_id = plot["id"]
        self.on_change = on_change

        self.title(f"Plot {plot['plot_no']} - {block_name}")
        self.geometry("780x600")
        self.minsize(700, 550)
        self.configure(fg_color=BG)

        self.grab_set()  # modal-like behaviour

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.create_header(plot)
        self.create_summary_cards(plot)
        self.create_payment_form()
        self.create_table()

        self.refresh()

    # ------------------------------------------------------------------
    def create_header(self, plot):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=25, pady=(20, 10))

        ctk.CTkLabel(header, text=f"Plot {plot['plot_no']}", font=("Arial", 26, "bold"),
                     text_color=NAVY).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text=f"Buyer: {plot['buyer_name'] or 'N/A'}",
            font=("Arial", 15, "bold"), text_color="#1E3A5F"
        ).pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(
            header,
            text=f"{self.block_name}  •  {plot['marla']:g} Marla  •  Rate PKR {plot['rate']:,.2f} / Marla",
            font=("Arial", 14), text_color="gray40"
        ).pack(anchor="w")

    # ------------------------------------------------------------------
    def create_summary_cards(self, plot):
        self.total_var = tk.StringVar(value=f"PKR {plot['total_price']:,.2f}")
        self.paid_var = tk.StringVar(value="PKR 0")
        self.remaining_var = tk.StringVar(value="PKR 0")

        self.make_card("Total Price", self.total_var, BLUE).grid(row=1, column=0, padx=(25, 10), pady=(0, 15), sticky="nsew")
        self.make_card("Paid So Far", self.paid_var, GREEN).grid(row=1, column=1, padx=10, pady=(0, 15), sticky="nsew")
        self.make_card("Remaining", self.remaining_var, RED).grid(row=1, column=2, padx=(10, 25), pady=(0, 15), sticky="nsew")

    def make_card(self, title, value_var, color):
        card = ctk.CTkFrame(self, corner_radius=16, fg_color="white", border_width=1, border_color=BORDER, height=95)
        ctk.CTkLabel(card, text=title, font=("Arial", 13, "bold"), text_color="gray35").pack(
            anchor="w", padx=16, pady=(14, 2))
        ctk.CTkLabel(card, textvariable=value_var, font=("Arial", 20, "bold"), text_color=color).pack(
            anchor="w", padx=16, pady=(0, 14))
        return card

    # ------------------------------------------------------------------
    def create_payment_form(self):
        form = ctk.CTkFrame(self, corner_radius=16, fg_color="white", border_width=1, border_color=BORDER)
        form.grid(row=2, column=0, columnspan=3, padx=25, pady=(0, 15), sticky="ew")
        form.grid_columnconfigure(4, weight=1)

        ctk.CTkLabel(form, text="Add Payment", font=("Arial", 16, "bold"), text_color=NAVY).grid(
            row=0, column=0, columnspan=5, sticky="w", padx=18, pady=(14, 8))

        ctk.CTkLabel(form, text="Date (YYYY-MM-DD)", font=("Arial", 11), text_color="gray40").grid(
            row=1, column=0, sticky="w", padx=(18, 5))
        self.date_entry = ctk.CTkEntry(form, width=130, placeholder_text="YYYY-MM-DD")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=0, padx=(18, 10), pady=(0, 14), sticky="w")

        ctk.CTkLabel(form, text="Description", font=("Arial", 11), text_color="gray40").grid(
            row=1, column=1, sticky="w", padx=5)
        self.desc_entry = ctk.CTkEntry(form, width=220, placeholder_text="e.g. 3rd installment")
        self.desc_entry.grid(row=2, column=1, padx=10, pady=(0, 14), sticky="w")

        ctk.CTkLabel(form, text="Amount (PKR)", font=("Arial", 11), text_color="gray40").grid(
            row=1, column=2, sticky="w", padx=5)
        self.amount_entry = ctk.CTkEntry(form, width=130, placeholder_text="0.00")
        self.amount_entry.grid(row=2, column=2, padx=10, pady=(0, 14), sticky="w")

        ctk.CTkButton(form, text="+ Add Payment", width=140, height=34, command=self.add_payment).grid(
            row=2, column=3, padx=(10, 18), pady=(0, 14), sticky="w")

    # ------------------------------------------------------------------
    def create_table(self):
        container = ctk.CTkFrame(self, corner_radius=16, fg_color="white", border_width=1, border_color=BORDER)
        container.grid(row=3, column=0, columnspan=3, padx=25, pady=(0, 20), sticky="nsew")
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        top_row = ctk.CTkFrame(container, fg_color="transparent")
        top_row.grid(row=0, column=0, columnspan=2, sticky="ew", padx=18, pady=(14, 8))
        top_row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top_row, text="Payment History", font=("Arial", 16, "bold"), text_color=NAVY).grid(
            row=0, column=0, sticky="w")
        ctk.CTkButton(top_row, text="Delete Selected", width=130, fg_color=RED, hover_color="#B02A37",
                      command=self.delete_payment).grid(row=0, column=1, sticky="e")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Payments.Treeview", background="white", fieldbackground="white",
                         foreground="#333333", rowheight=30, borderwidth=0, font=("Arial", 12))
        style.configure("Payments.Treeview.Heading", background="#ECECEC", foreground=NAVY,
                         font=("Arial", 12, "bold"), relief="flat")
        style.map("Payments.Treeview", background=[("selected", "#CDE3FF")], foreground=[("selected", NAVY)])

        columns = ("date", "description", "amount")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", style="Payments.Treeview")

        headers = {"date": ("Date", 110), "description": ("Description", 320), "amount": ("Amount", 130)}
        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w" if col != "amount" else "e")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=(18, 0), pady=(0, 16))
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 16), padx=(0, 12))

        self.empty_label = ctk.CTkLabel(container, text="No payments recorded yet.",
                                         font=("Arial", 13), text_color="gray50")

    # ------------------------------------------------------------------
    def add_payment(self):
        date_str = self.date_entry.get().strip()
        description = self.desc_entry.get().strip()
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

        self.excel.add_payment(self.block_name, self.plot_id, date_str, description, amount)

        self.desc_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.refresh()
        if self.on_change:
            self.on_change()

    def delete_payment(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a payment to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete this payment record?"):
            return
        payment_id = int(self.tree.item(selection[0], "tags")[0])
        self.excel.delete_payment(self.block_name, payment_id)
        self.refresh()
        if self.on_change:
            self.on_change()

    # ------------------------------------------------------------------
    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        payments = self.excel.load_payments(self.block_name, self.plot_id)

        if not payments:
            self.empty_label.grid(row=1, column=0, columnspan=2, sticky="nsew")
        else:
            self.empty_label.grid_forget()

        for p in payments:
            self.tree.insert("", "end", tags=(str(p["id"]),), values=(
                p["date"], p["description"], f"PKR {p['amount']:,.2f}",
            ))

        plots = self.excel.load_plots(self.block_name)
        plot = next((pl for pl in plots if pl["id"] == self.plot_id), None)
        if plot:
            self.paid_var.set(f"PKR {plot['paid']:,.2f}")
            self.remaining_var.set(f"PKR {plot['remaining']:,.2f}")
