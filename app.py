import sys
import os
import customtkinter
import threading
from cf_user import CFUser


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Codeforces User Comparison")
        self.geometry("1280x720")
        self.iconbitmap("codeforces.ico")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Inputs
        self.top_frame = customtkinter.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(2, weight=1)

        self.num_handles_entry = customtkinter.CTkEntry(self.top_frame, placeholder_text="No. of handles. max=5")
        self.num_handles_entry.grid(row=0, column=0, padx=10, pady=10)
        self.num_handles_entry.bind("<Return>", lambda event: self.generate_entries_and_focus())

        self.generate_button = customtkinter.CTkButton(self.top_frame, text="Enter", command=self.create_handle_entries)
        self.generate_button.grid(row=0, column=1, padx=10, pady=10)

        # Handle inputs
        self.handles_frame = customtkinter.CTkFrame(self.top_frame)
        self.handles_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.handle_entries = []

        # Compare Button
        self.compare_button = customtkinter.CTkButton(self.top_frame, text="Compare Stats", command=self.compare_stats_threaded)
        self.compare_button.grid(row=0, column=3, padx=10, pady=10)

        # Results Grid
        self.results_frame = customtkinter.CTkScrollableFrame(self)
        self.results_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Status Label
        self.status_label = customtkinter.CTkLabel(self, text="", anchor="w")
        self.status_label.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.num_handles_entry.insert(0, "1")
        self.create_handle_entries()

    def generate_entries_and_focus(self):
        self.create_handle_entries()
        if self.handle_entries:
            self.handle_entries[0].focus_set()

    def create_handle_entries(self):
        for widget in self.handles_frame.winfo_children():
            widget.destroy()
        self.handle_entries = []

        try:
            num_handles = int(self.num_handles_entry.get())
            if not (1 <= num_handles <= 5):
                self.status_label.configure(text="Please enter a number between 1 and 5.")
                return
        except ValueError:
            self.status_label.configure(text="Please enter a valid number.")
            return

        self.status_label.configure(text="")
        for i in range(num_handles):
            self.handles_frame.grid_columnconfigure(i, weight=1)
            entry = customtkinter.CTkEntry(self.handles_frame, placeholder_text=f"CF Handle {i + 1}")
            entry.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            entry.bind("<Return>", lambda event, index=i: self.handle_entry_return(index))
            self.handle_entries.append(entry)

    def handle_entry_return(self, index):
        if index == len(self.handle_entries) - 1:
            self.compare_button.invoke()
        else:
            self.handle_entries[index + 1].focus_set()

    def compare_stats_threaded(self):
        thread = threading.Thread(target=self.compare_stats)
        thread.start()

    def compare_stats(self):
        handles = [entry.get() for entry in self.handle_entries if entry.get()]
        if not handles:
            self.status_label.configure(text="Please enter at least one handle.")
            return

        self.status_label.configure(text=f"Fetching stats for {', '.join(handles)}...")
        self.compare_button.configure(state="disabled")

        users_metrics = []
        threads = []

        def fetch_user_metrics(handle, result_list):
            user = CFUser(handle)
            metrics = user.get_metrics()
            result_list.append(metrics)

        for handle in handles:
            thread = threading.Thread(target=fetch_user_metrics, args=(handle, users_metrics))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.after(0, self.display_comparison_grid, users_metrics)
        self.status_label.configure(text="Comparison complete.")
        self.compare_button.configure(state="normal")

    def display_comparison_grid(self, users_metrics):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Reset column configurations
        for i in range(self.results_frame.grid_size()[0]):
            self.results_frame.grid_columnconfigure(i, weight=0)

        errors = [m for m in users_metrics if isinstance(m, str)]
        valid_metrics = [m for m in users_metrics if isinstance(m, dict)]

        if errors:
            error_text = "\n".join(errors)
            error_label = customtkinter.CTkLabel(self.results_frame, text=error_text, text_color="red")
            error_label.grid(row=0, column=0, padx=10, pady=10)
            if not valid_metrics:
                return

        if not valid_metrics:
            self.status_label.configure(text="Could not fetch stats for any of the handles.")
            return

        # fit columns to fill result field
        self.results_frame.grid_columnconfigure(0, weight=0)  # Metrics column
        for i in range(len(valid_metrics)):
            self.results_frame.grid_columnconfigure(i + 1, weight=1)  # User columns

        metric_keys = valid_metrics[0].keys()
        handles = [m['User'] for m in valid_metrics]

        # Headers
        header_font = ("Arial", 15, "bold")
        header_frame = customtkinter.CTkFrame(self.results_frame, border_width=3, border_color="#0263b2")
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        header = customtkinter.CTkLabel(header_frame, text="Comparison Metrics", font=header_font, anchor="center")
        header.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        for i, handle in enumerate(handles):
            header_frame = customtkinter.CTkFrame(self.results_frame, border_width=3, border_color="#0263b2")
            header_frame.grid(row=0, column=i + 1, padx=5, pady=5, sticky="ew")
            header = customtkinter.CTkLabel(header_frame, text=handle, font=header_font, anchor="center")
            header.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Data Rows
        for r, key in enumerate(metric_keys, start=1):
            if key != 'User':
                key_frame = customtkinter.CTkFrame(self.results_frame, border_width=3, border_color="#029cfe")
                key_frame.grid(row=r, column=0, padx=5, pady=5, sticky="ew")
                key_label = customtkinter.CTkLabel(key_frame, text=key, anchor="w")
                key_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

                for c, metrics in enumerate(valid_metrics, start=1):
                    value = str(metrics[key])
                    value_frame = customtkinter.CTkFrame(self.results_frame, border_width=1, border_color="gray")
                    value_frame.grid(row=r, column=c, padx=5, pady=5, sticky="ew")
                    value_label = customtkinter.CTkLabel(value_frame, text=value, anchor="center", wraplength=200)
                    value_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
