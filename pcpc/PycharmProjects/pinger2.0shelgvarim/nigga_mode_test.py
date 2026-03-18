import tkinter as tk


def create_dark_mode_window():
    # Create the main window
    root = tk.Tk()
    root.title("Dark Mode Window")

    # Set the background color of the window
    root.configure(bg='#2E2E2E')  # Dark gray background

    # Set up a label with white text
    label = tk.Label(root, text="Welcome to Dark Mode!", fg='#FFFFFF', bg='#2E2E2E', font=("Arial", 16))
    label.pack(pady=20)

    # Set up a button with dark background and light text
    button = tk.Button(root, text="Click Me", fg='#FFFFFF', bg='#4C4C4C', font=("Arial", 12))
    button.pack(pady=10)

    # Set up an entry widget with a dark background and light text
    entry = tk.Entry(root, fg='#FFFFFF', bg='#4C4C4C', font=("Arial", 12))
    entry.pack(pady=10, padx=20)

    # Start the main loop
    root.mainloop()


# Call the function to create the window
create_dark_mode_window()
