import tkinter as tk
from tkinter import PhotoImage
import tkinter.font as tkFont
import pyperclip  # You'll need to install pyperclip for clipboard functionality
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to validate the URL
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

# Function to display the top-level window with the gathered links
def show_gathered_links(links):
    top = tk.Toplevel(root)
    top.title("Gathered Links")
    top.geometry("400x300")
    top.configure(bg="#f9d1d1")
    top.transient(root)  # Make it a child of the main window
    top.grab_set()  # Prevent interaction with the main window while this window is open
    top.resizable(False, False)  # Make it non-resizable
    top.attributes("-topmost", True)  # Keep the window on top of the main window

    # Add a cute title
    title_label = tk.Label(top, text="Gathered Links", font=font_title, fg="white", bg="#f9d1d1")
    title_label.pack(pady=10)

    # Create a Text widget to display the links
    links_text = tk.Text(top, font=font_entry, width=40, height=10, bd=4, relief="solid", bg="#fff0f5", fg="#ff69b4")
    links_text.pack(pady=10)

    # Insert each link into the Text widget
    if links:
        links_text.insert(tk.END, "\n".join(links))
    else:
        links_text.insert(tk.END, "No links found.")

    # Make sure this window is positioned inside the main window
    top.geometry(f'400x300+{root.winfo_x() + 50}+{root.winfo_y() + 50}')  # Position it near the main window
    top.place(x=root.winfo_x() + 50, y=root.winfo_y() + 50)  # Position relative to the main window

# Function to show a custom message box inside the window (for alerts)
def show_alert(message, title="Alert"):
    alert_window = tk.Toplevel(root)
    alert_window.title(title)
    alert_window.geometry("300x150")
    alert_window.configure(bg="#f9d1d1")
    alert_window.transient(root)
    alert_window.grab_set()  # Modal behavior: prevent interaction with other windows
    alert_window.resizable(False, False)  # Make it non-resizable

    # Add a message label with white text
    message_label = tk.Label(alert_window, text=message, font=font_button, fg="white", bg="#f9d1d1")
    message_label.pack(pady=20)

    # Add a "Close" button to dismiss the alert
    close_button = tk.Button(alert_window, text="OK", font=font_button, bg="#ffb6c1", fg="white", relief="raised", bd=5, command=lambda: close_alert(alert_window))
    close_button.pack(pady=10)

    # Ensure the alert window stays on top of the main window
    alert_window.attributes("-topmost", True)

    # Make sure this window is positioned inside the main window
    alert_window.geometry(f'300x150+{root.winfo_x() + 100}+{root.winfo_y() + 100}')  # Position it near the main window
    alert_window.place(x=root.winfo_x() + 100, y=root.winfo_y() + 100)  # Position relative to the main window

# Function to close the alert window and open the gathering links window
def close_alert(alert_window):
    alert_window.destroy()  # Close the alert window
    # Now open the gathering links window after the alert is closed
    show_gathered_links(gathered_links)

# Function to scrape the URL
def start_gathering():
    url = url_entry.get()

    if not url:
        show_alert("Please enter a URL, nya~!", "Error")
        return

    if not is_valid_url(url):
        show_alert("Please enter a valid URL that starts with http:// or https://", "Invalid URL")
        return

    # Set up WebDriver (ensure you have ChromeDriver installed and in PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headlessly (no browser UI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)  # Open the provided URL
        time.sleep(3)  # Wait for the page to load completely

        # Gather all the links on the page
        links = driver.find_elements(By.TAG_NAME, "a")
        global gathered_links  # Make links available globally
        gathered_links = [link.get_attribute("href") for link in links if link.get_attribute("href")]

        # Check if links are found
        if gathered_links:
            show_alert(f"Found {len(gathered_links)} links!", "Yay! Gathered Successfully!")
            print("Gathered Links:", gathered_links)

            # The gathering links window will be shown once the alert is closed
        else:
            show_alert("No links were found on the page.", "No Links Found")
    except Exception as e:
        show_alert(f"Something went wrong while gathering links: {e}", "Error")
    finally:
        driver.quit()  # Make sure to quit the driver

# Function to paste the URL from clipboard into the entry field
def paste_url():
    url = pyperclip.paste()  # Get URL from clipboard
    if url:
        url_entry.delete(0, tk.END)  # Clear current text
        url_entry.insert(0, url)  # Insert the URL into the entry

# Function to handle the placeholder text behavior
def on_focus_in(event):
    if url_entry.get() == "Enter URL":
        url_entry.delete(0, tk.END)  # Clear the placeholder text

def on_focus_out(event):
    if url_entry.get() == "":
        url_entry.insert(0, "Enter URL")  # Add placeholder text if no input

# Create the main window
root = tk.Tk()
root.title("Bunni Cloud Downloader")
root.geometry("600x400")  # Bigger window size to match the desired layout
root.configure(bg="#f9d1d1")  # Soft pastel pink background

# Set the window icon using the uploaded image (absolute path to the image)
icon_image = PhotoImage(file='C:/Users/rinse/Downloads/Bunni-Cloud-Downloader/pink-anime-girl.png')  # Absolute path
root.iconphoto(True, icon_image)  # Use iconphoto for .png images

# Set the background image (absolute path to the image)
background_image = PhotoImage(file='C:/Users/rinse/Downloads/Bunni-Cloud-Downloader/pink-anime-girl.png')  # Absolute path
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)  # Stretch the background image to cover the window

# Define custom fonts for a cute and readable design
font_title = tkFont.Font(family="Comic Sans MS", size=26, weight="bold")
font_button = tkFont.Font(family="Comic Sans MS", size=14, weight="bold")
font_label = tkFont.Font(family="Arial Rounded", size=14, weight="normal")
font_entry = tkFont.Font(family="Quicksand", size=12, weight="normal")
font_footer = tkFont.Font(family="Comic Sans MS", size=10, weight="normal")

# Add a cute title
title_label = tk.Label(root, text="Bunni Cloud Downloader", font=font_title, fg="white", bg="#f9d1d1")  # White text
title_label.pack(pady=10)

# Add the creator's name
creator_label = tk.Label(root, text="Creator: Rin (Reen)", font=("Arial", 12, "italic"), fg="white", bg="#f9d1d1")  # White text
creator_label.pack(pady=5)

# URL entry field with border styling (No rounded corners, but we can style it)
url_label = tk.Label(root, text="Enter URL:", font=font_label, bg="#f9d1d1", fg="white")  # White text
url_label.pack(pady=5)

# Simple Entry field with placeholder text
url_entry = tk.Entry(root, font=font_entry, width=30, bd=4, relief="solid", bg="#fff0f5", fg="#ff69b4")
url_entry.insert(0, "Enter URL")  # Insert placeholder text
url_entry.bind("<FocusIn>", on_focus_in)  # When focus is in the field, remove placeholder
url_entry.bind("<FocusOut>", on_focus_out)  # When focus is out, check if placeholder should be added
url_entry.pack(pady=10)

# Function to paste link into the text field
paste_button = tk.Button(root, text="Paste Link", font=font_button, bg="#f9d1d1", fg="white", relief="raised", bd=5, command=paste_url)
paste_button.pack(pady=10)

# Start gathering button with pastel colors and cute text
def on_button_hover(event):
    start_button.config(bg="#ff99cc")  # Lighter pink when hovered

def on_button_leave(event):
    start_button.config(bg="#f9d1d1")  # Original color when not hovered

# Update the button text to something more playful and cute
start_button = tk.Button(root, text="Go for it!", font=font_button, bg="#f9d1d1", fg="white",  # Same background as main window
                         relief="raised", bd=5, command=start_gathering)
start_button.pack(pady=20)
start_button.bind("<Enter>", on_button_hover)
start_button.bind("<Leave>", on_button_leave)

# Add a cute footer with "Powered by Bunni Cloud"
footer_label = tk.Label(root, text="Powered by Bunni Cloud", font=font_footer, fg="white", bg="#f9d1d1")  # White text
footer_label.pack(side="bottom", pady=10)

# Run the Tkinter event loop
root.mainloop()
