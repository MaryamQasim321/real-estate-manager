import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

from plot_excel_manager import PlotExcelManager
from plot_detail_window import PlotDetailWindow

NAVY = "#1E3A5F"
BG = "#F5F7FA"
GREEN = "#28A745"
RED = "#DC3545"
BLUE = "#0D6EFD"
BORDER = "#DDDDDD"


class PlotManager(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=BG)
        self.pack(fill="both", expand=True)

        self.excel = PlotExcelManager()
        self.selected_block = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.create_header()
        self.create_summary_cards()
        self.create_add_plot_form()
        self.create_table()

        self.refresh_block_list(select_first=True)

    # ------------------------------------------------------------------
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=4, sticky="ew", padx=30, pady=(25, 15))
        header.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_box, text="Plot Manager", font=("Arial", 32, "bold"), text_color=NAVY).pack(anchor="w")
        ctk.CTkLabel(title_box, text="Manage blocks, plots, and installment payments",
                     font=("Arial", 16), text_color="gray40").pack(anchor="w")

        control_box = ctk.CTkFrame(header, fg_color="transparent")
        control_box.grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(control_box, text="Block:", font=("Arial", 14), text_color="gray30").pack(
            side="left", padx=(0, 8))

        self.block_var = tk.StringVar(value="")
        self.block_menu = ctk.CTkOptionMenu(control_box, values=[""], variable=self.block_var,
                                             width=160, command=self.on_block_change)
        self.block_menu.pack(side="left", padx=(0, 10))

        ctk.CTkButton(control_box, text="+ New Block", width=120, command=self.new_block).pack(
            side="left", padx=(0, 8))
        ctk.CTkButton(control_box, text="Delete Block", width=120, fg_color=RED, hover_color="#B02A37",
                      command=self.delete_block).pack(side="left")

    # ------------------------------------------------------------------
    def create_summary_cards(self):
        self.plots_count_var = tk.StringVar(value="0")
        self.total_price_var = tk.StringVar(value="PKR 0")
        self.total_paid_var = tk.StringVar(value="PKR 0")
        self.total_remaining_var = tk.StringVar(value="PKR 0")

        self.make_card("Total Plots", self.plots_count_var, NAVY).grid(
            row=1, column=0, padx=(30, 10), pady=(0, 15), sticky="nsew")
        self.make_card("Total Price", self.total_price_var, BLUE).grid(
            row=1, column=1, padx=10, pady=(0, 15), sticky="nsew")
        self.make_card("Total Paid", self.total_paid_var, GREEN).grid(
            row=1, column=2, padx=10, pady=(0, 15), sticky="nsew")
        self.make_card("Total Remaining", self.total_remaining_var, RED).grid(
            row=1, column=3, padx=(10, 30), pady=(0, 15), sticky="nsew")

    def make_card(self, title, value_var, color):
        card = ctk.CTkFrame(self, corner_radius=18, fg_color="white", border_width=1,
                             border_color=BORDER, height=110)
        ctk.CTkLabel(card, text=title, font=("Arial", 14, "bold"), text_color="gray35").pack(
            anchor="w", padx=18, pady=(16, 4))
        ctk.CTkLabel(card, textvariable=value_var, font=("Arial", 22, "bold"), text_color=color).pack(
            anchor="w", padx=18, pady=(0, 16))
        return card

    # ------------------------------------------------------------------
    def create_add_plot_form(self):
        form = ctk.CTkFrame(self, corner_radius=18, fg_color="white", border_width=1, border_color=BORDER)
        form.grid(row=2, column=0, columnspan=4, padx=30, pady=(0, 15), sticky="ew")
        form.grid_columnconfigure(6, weight=1)

        ctk.CTkLabel(form, text="Add Plot", font=("Arial", 18, "bold"), text_color=NAVY).grid(
            row=0, column=0, columnspan=7, sticky="w", padx=20, pady=(15, 10))

        ctk.CTkLabel(form, text="Plot No.", font=("Arial", 12), text_color="gray40").grid(
            row=1, column=0, sticky="w", padx=(20, 5))
        self.plot_no_entry = ctk.CTkEntry(form, width=110, placeholder_text="e.g. P-101")
        self.plot_no_entry.grid(row=2, column=0, padx=(20, 10), pady=(0, 15), sticky="w")

        ctk.CTkLabel(form, text="Buyer Name", font=("Arial", 12), text_color="gray40").grid(
            row=1, column=1, sticky="w", padx=5)
        self.buyer_entry = ctk.CTkEntry(form, width=170, placeholder_text="e.g. Ahmed Khan")
        self.buyer_entry.grid(row=2, column=1, padx=10, pady=(0, 15), sticky="w")

        ctk.CTkLabel(form, text="Rate / Marla (PKR)", font=("Arial", 12), text_color="gray40").grid(
            row=1, column=2, sticky="w", padx=5)
        self.rate_entry = ctk.CTkEntry(form, width=130, placeholder_text="0.00")
        self.rate_entry.grid(row=2, column=2, padx=10, pady=(0, 15), sticky="w")
        self.rate_entry.bind("<KeyRelease>", self.update_price_preview)

        ctk.CTkLabel(form, text="Marla", font=("Arial", 12), text_color="gray40").grid(
            row=1, column=3, sticky="w", padx=5)
        self.marla_entry = ctk.CTkEntry(form, width=90, placeholder_text="0")
        self.marla_entry.grid(row=2, column=3, padx=10, pady=(0, 15), sticky="w")
        self.marla_entry.bind("<KeyRelease>", self.update_price_preview)

        ctk.CTkLabel(form, text="Total Price", font=("Arial", 12), text_color="gray40").grid(
            row=1, column=4, sticky="w", padx=5)
        self.price_preview_var = tk.StringVar(value="PKR 0")
        ctk.CTkLabel(form, textvariable=self.price_preview_var, font=("Arial", 14, "bold"), text_color=BLUE).grid(
            row=2, column=4, padx=10, pady=(0, 15), sticky="w")

        ctk.CTkButton(form, text="+ Add Plot", width=140, height=36, command=self.add_plot).grid(
            row=2, column=5, padx=(10, 20), pady=(0, 15), sticky="w")

    def update_price_preview(self, _=None):
        try:
            rate = float(self.rate_entry.get())
            marla = float(self.marla_entry.get())
            self.price_preview_var.set(f"PKR {rate * marla:,.2f}")
        except ValueError:
            self.price_preview_var.set("PKR 0")

    # ------------------------------------------------------------------
    def create_table(self):
        container = ctk.CTkFrame(self, corner_radius=18, fg_color="white", border_width=1, border_color=BORDER)
        container.grid(row=3, column=0, columnspan=4, padx=30, pady=(0, 25), sticky="nsew")
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        top_row = ctk.CTkFrame(container, fg_color="transparent")
        top_row.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(18, 10))
        top_row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top_row, text="Plots", font=("Arial", 20, "bold"), text_color=NAVY).grid(
            row=0, column=0, sticky="w")

        btn_box = ctk.CTkFrame(top_row, fg_color="transparent")
        btn_box.grid(row=0, column=1, sticky="e")
        ctk.CTkButton(btn_box, text="View Payments", width=140, command=self.open_plot_detail).pack(
            side="left", padx=(0, 8))
        ctk.CTkButton(btn_box, text="Delete Plot", width=120, fg_color=RED, hover_color="#B02A37",
                      command=self.delete_plot).pack(side="left")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Plots.Treeview", background="white", fieldbackground="white",
                         foreground="#333333", rowheight=32, borderwidth=0, font=("Arial", 12))
        style.configure("Plots.Treeview.Heading", background="#ECECEC", foreground=NAVY,
                         font=("Arial", 12, "bold"), relief="flat")
        style.map("Plots.Treeview", background=[("selected", "#CDE3FF")], foreground=[("selected", NAVY)])

        columns = ("plot_no", "buyer", "marla", "rate", "total", "paid", "remaining", "status")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", style="Plots.Treeview")

        headers = {
            "plot_no": ("Plot No.", 100),
            "buyer": ("Buyer Name", 150),
            "marla": ("Marla", 70),
            "rate": ("Rate / Marla", 120),
            "total": ("Total Price", 120),
            "paid": ("Paid", 120),
            "remaining": ("Remaining", 120),
            "status": ("Status", 100),
        }
        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w" if col in ("plot_no", "buyer", "status") else "e")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=(20, 0), pady=(0, 20))
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 20), padx=(0, 15))
        self.tree.bind("<Double-1>", lambda e: self.open_plot_detail())

        self.empty_label = ctk.CTkLabel(container, text="No plots yet.\nAdd a plot above to get started.",
                                         font=("Arial", 14), text_color="gray50")

    # ------------------------------------------------------------------
    # Block operations
    # ------------------------------------------------------------------
    def refresh_block_list(self, select_first=False):
        blocks = self.excel.list_blocks()
        if not blocks:
            self.block_menu.configure(values=["No blocks"])
            self.block_var.set("No blocks")
            self.selected_block = None
            self.refresh_plots()
            return

        self.block_menu.configure(values=blocks)
        if select_first or self.block_var.get() not in blocks:
            self.block_var.set(blocks[0])
        self.selected_block = self.block_var.get()
        self.refresh_plots()

    def on_block_change(self, _=None):
        self.selected_block = self.block_var.get()
        self.refresh_plots()

    def new_block(self):
        dialog = ctk.CTkInputDialog(text="Enter block name (e.g. Block A):", title="New Block")
        name = dialog.get_input()
        if not name:
            return
        name = name.strip()
        if not name:
            return
        if self.excel.block_exists(name):
            messagebox.showerror("Already Exists", f"Block '{name}' already exists.")
            return
        self.excel.create_block(name)
        self.refresh_block_list()
        self.block_var.set(name)
        self.on_block_change()

    def delete_block(self):
        if not self.selected_block or self.selected_block == "No blocks":
            return
        if not messagebox.askyesno(
                "Confirm Delete",
                f"Delete block '{self.selected_block}' and all its plots and payments?\nThis cannot be undone."):
            return
        self.excel.delete_block(self.selected_block)
        self.refresh_block_list(select_first=True)

    # ------------------------------------------------------------------
    # Plot operations
    # ------------------------------------------------------------------
    def add_plot(self):
        if not self.selected_block or self.selected_block == "No blocks":
            messagebox.showwarning("No Block Selected", "Please create or select a block first.")
            return

        plot_no = self.plot_no_entry.get().strip()
        if not plot_no:
            messagebox.showerror("Missing Plot No.", "Please enter a plot number.")
            return

        buyer_name = self.buyer_entry.get().strip()
        if not buyer_name:
            messagebox.showerror("Missing Buyer Name", "Please enter the name of the person buying this plot.")
            return

        try:
            rate = float(self.rate_entry.get())
            marla = float(self.marla_entry.get())
            if rate <= 0 or marla <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers for rate and marla.")
            return

        self.excel.add_plot(self.selected_block, plot_no, buyer_name, rate, marla)

        self.plot_no_entry.delete(0, "end")
        self.buyer_entry.delete(0, "end")
        self.rate_entry.delete(0, "end")
        self.marla_entry.delete(0, "end")
        self.price_preview_var.set("PKR 0")

        self.refresh_plots()

    def delete_plot(self):
        plot_id = self.get_selected_plot_id()
        if plot_id is None:
            messagebox.showwarning("No Selection", "Please select a plot to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete this plot and all its payment records?"):
            return
        self.excel.delete_plot(self.selected_block, plot_id)
        self.refresh_plots()

    def get_selected_plot_id(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return int(self.tree.item(selection[0], "tags")[0])

    def open_plot_detail(self):
        plot_id = self.get_selected_plot_id()
        if plot_id is None:
            messagebox.showwarning("No Selection", "Please select a plot to view its payments.")
            return
        plots = self.excel.load_plots(self.selected_block)
        plot = next((p for p in plots if p["id"] == plot_id), None)
        if plot is None:
            return
        PlotDetailWindow(self, self.excel, self.selected_block, plot, on_change=self.refresh_plots)

    # ------------------------------------------------------------------
    def refresh_plots(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not self.selected_block or self.selected_block == "No blocks":
            self.empty_label.grid(row=1, column=0, columnspan=2, sticky="nsew")
            self.plots_count_var.set("0")
            self.total_price_var.set("PKR 0")
            self.total_paid_var.set("PKR 0")
            self.total_remaining_var.set("PKR 0")
            return

        plots = self.excel.load_plots(self.selected_block)

        if not plots:
            self.empty_label.grid(row=1, column=0, columnspan=2, sticky="nsew")
        else:
            self.empty_label.grid_forget()

        for p in plots:
            status = "Paid Off" if p["remaining"] <= 0 else "Pending"
            self.tree.insert("", "end", tags=(str(p["id"]),), values=(
                p["plot_no"], p["buyer_name"], f"{p['marla']:g}", f"PKR {p['rate']:,.2f}",
                f"PKR {p['total_price']:,.2f}", f"PKR {p['paid']:,.2f}",
                f"PKR {p['remaining']:,.2f}", status,
            ))

        count, total_price, total_paid, total_remaining = self.excel.get_block_summary(self.selected_block)
        self.plots_count_var.set(str(count))
        self.total_price_var.set(f"PKR {total_price:,.2f}")
        self.total_paid_var.set(f"PKR {total_paid:,.2f}")
        self.total_remaining_var.set(f"PKR {total_remaining:,.2f}")
