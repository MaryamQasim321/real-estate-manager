import customtkinter as ctk
from datetime import datetime


class Dashboard(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#F5F7FA")

        self.pack(fill="both", expand=True)

        # Make window responsive
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.create_header()
        self.create_summary_cards()
        self.create_recent_transactions()

    # -------------------------------------------------
    # Header
    # -------------------------------------------------
    def create_header(self):

        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header_frame.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=30,
            pady=(25, 20)
        )

        title = ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=("Arial", 32, "bold"),
            text_color="#1E3A5F"
        )

        title.pack(anchor="w")

        month = datetime.now().strftime("%B %Y")

        subtitle = ctk.CTkLabel(
            header_frame,
            text=f"Financial Summary • {month}",
            font=("Arial", 16),
            text_color="gray40"
        )

        subtitle.pack(anchor="w")

    # -------------------------------------------------
    # Summary Cards
    # -------------------------------------------------
    def create_summary_cards(self):

        revenue = self.create_card(
            title="Total Revenue",
            value="PKR 0",
            color="#28A745"
        )

        revenue.grid(
            row=1,
            column=0,
            padx=20,
            sticky="nsew"
        )

        expense = self.create_card(
            title="Total Expense",
            value="PKR 0",
            color="#DC3545"
        )

        expense.grid(
            row=1,
            column=1,
            padx=20,
            sticky="nsew"
        )

        balance = self.create_card(
            title="Current Balance",
            value="PKR 0",
            color="#0D6EFD"
        )

        balance.grid(
            row=1,
            column=2,
            padx=20,
            sticky="nsew"
        )

    # -------------------------------------------------
    # Create Card
    # -------------------------------------------------
    def create_card(self, title, value, color):

        card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color="white",
            border_width=1,
            border_color="#DDDDDD",
            height=140
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 18, "bold"),
            text_color="gray35"
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 30, "bold"),
            text_color=color
        )

        value_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 20)
        )

        return card

    # -------------------------------------------------
    # Recent Transactions
    # -------------------------------------------------
    def create_recent_transactions(self):

        frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=18
        )

        frame.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=25,
            pady=25,
            sticky="nsew"
        )

        title = ctk.CTkLabel(
            frame,
            text="Recent Transactions",
            font=("Arial", 22, "bold"),
            text_color="#1E3A5F"
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        headers = [
            "Date",
            "Description",
            "Revenue",
            "Expense",
            "Balance"
        ]

        header_frame = ctk.CTkFrame(
            frame,
            fg_color="#ECECEC",
            corner_radius=8
        )

        header_frame.pack(
            fill="x",
            padx=20
        )

        for i, header in enumerate(headers):

            lbl = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 15, "bold")
            )

            lbl.grid(
                row=0,
                column=i,
                padx=25,
                pady=10,
                sticky="w"
            )

        empty = ctk.CTkLabel(
            frame,
            text="\n\nNo transactions available.\n\nAdd your first revenue or expense.\n",
            font=("Arial", 16),
            text_color="gray50"
        )

        empty.pack(
            expand=True,
            fill="both"
        )