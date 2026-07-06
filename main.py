import customtkinter as ctk
from tkinter import messagebox

# -------------------------------
# Theme Configuration
# -------------------------------
ctk.set_appearance_mode("Light")      # Light / Dark / System
ctk.set_default_color_theme("blue")   # blue, green, dark-blue


class PropertyManagementApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Property Management System")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create UI
        self.create_sidebar()
        self.create_main_frame()

        # Load Dashboard
        self.show_dashboard()

    # ----------------------------------------
    # Sidebar
    # ----------------------------------------
    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color="#1E3A5F"
        )

        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        # Logo

        logo = ctk.CTkLabel(
            self.sidebar,
            text="🏢",
            font=("Arial", 50)
        )

        logo.pack(pady=(30, 5))

        title = ctk.CTkLabel(
            self.sidebar,
            text="Property\nManagement",
            font=("Arial", 22, "bold"),
            text_color="white"
        )

        title.pack(pady=(0, 30))

        # Dashboard Button

        self.dashboard_btn = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            height=45,
            command=self.show_dashboard
        )

        self.dashboard_btn.pack(fill="x", padx=20, pady=8)

        # Expense Tracker Button

        self.expense_btn = ctk.CTkButton(
            self.sidebar,
            text="Expense Tracker",
            height=45,
            command=self.show_expense_tracker
        )

        self.expense_btn.pack(fill="x", padx=20, pady=8)

        # Plot Manager

        self.property_btn = ctk.CTkButton(
            self.sidebar,
            text="Plot Manager",
            height=45,
            command=self.show_plot_manager
        )

        self.property_btn.pack(fill="x", padx=20, pady=8)

        # Reports

        self.report_btn = ctk.CTkButton(
            self.sidebar,
            text="Reports",
            height=45,
            command=self.show_reports
        )

        self.report_btn.pack(fill="x", padx=20, pady=8)

        # Spacer

        ctk.CTkLabel(self.sidebar, text="").pack(expand=True)

        # Footer

        footer = ctk.CTkLabel(
            self.sidebar,
            text="Version 1.0",
            text_color="white"
        )

        footer.pack(pady=20)

    # ----------------------------------------
    # Main Area
    # ----------------------------------------
    def create_main_frame(self):

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#F5F7FA",
            corner_radius=0
        )

        self.main_frame.grid(row=0, column=1, sticky="nsew")

    # ----------------------------------------
    # Clear Current Page
    # ----------------------------------------
    def clear_main_frame(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ----------------------------------------
    # Dashboard
    # ----------------------------------------
    def show_dashboard(self):

        self.clear_main_frame()

        try:
            from dashboard import Dashboard

            Dashboard(self.main_frame).pack(
                fill="both",
                expand=True
            )

        except ImportError:

            label = ctk.CTkLabel(
                self.main_frame,
                text="Dashboard\n\n(Coming Next)",
                font=("Arial", 30, "bold")
            )

            label.pack(expand=True)

    # ----------------------------------------
    # Expense Tracker
    # ----------------------------------------
    def show_expense_tracker(self):

        self.clear_main_frame()

        from expense_tracker import ExpenseTracker

        ExpenseTracker(self.main_frame)

    # ----------------------------------------
    # Plot Manager
    # ----------------------------------------
    def show_plot_manager(self):

        self.clear_main_frame()

        from plot_manager import PlotManager

        PlotManager(self.main_frame)

    # ----------------------------------------
    # Reports
    # ----------------------------------------
    def show_reports(self):

        self.clear_main_frame()

        from reports import Reports

        Reports(self.main_frame)


# ----------------------------------------
# Run Application
# ----------------------------------------
if __name__ == "__main__":

    app = PropertyManagementApp()

    app.mainloop()
