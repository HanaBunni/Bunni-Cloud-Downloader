import os
import requests
import pyperclip
from tkinter import *
from tkinter import messagebox
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Import webdriver_manager
from PIL import Image, ImageTk

# VirusTotal API key (already provided)
API_KEY = '93701966833a09afb9b7ba93d2f029f98d63c5842011be801fe8d1b292097868'
BASE_URL = 'https://www.virustotal.com/api/v3/urls/'

# Function to update the log window with UwU text
def update_log(message, color="black"):
    log_text.insert(END, f"{message}\n")
    log_text.yview(END)  # Scroll to the bottom
    log_text.tag_add(color, "1.0", END)
    log_text.tag_configure(color, foreground=color)

# Function to display "uwu" loading animation in the main window (on top of the program)
def show_loading_animation():
    global loading_frame
    loading_frame = Frame(root, bg="#F9C7D1", width=400, height=200)
    loading_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the loading frame

    loading_label = Label(loading_frame, text="Loading uwu~", font=("Comic Sans MS", 16, "italic"), fg="#FF99CC", bg="#F9C7D1")
    loading_label.pack(pady=50)

    # Disable main window interaction during loading
    root.attributes('-disabled', True)

def stop_loading_animation():
    loading_frame.destroy()  # Close the loading window
    root.attributes('-disabled', False)  # Re-enable the main window

# Function to paste the URL directly from the clipboard
def paste_url():
    url = pyperclip.paste()  # Get the content from the clipboard
    url_text.delete("1.0", END)  # Clear any current text
    url_text.insert("1.0", url)  # Insert the new URL
    update_log(f"Pasted URL from clipboard: {url}", "blue")  # Optionally log this action

# Function to copy the log content to clipboard
def copy_to_clipboard():
    try:
        log_content = log_text.get("1.0", END).strip()  # Get all the content from the log window
        pyperclip.copy(log_content)  # Copy the log content to clipboard
        update_log("Copied the log to clipboard uwu~", "blue")  # Notify the user
    except Exception as e:
        update_log(f"Failed to copy log to clipboard: {e} nya~", "red")

# Enhanced function to fetch categorized download links from a URL using Selenium
def fetch_download_links(url):
    game_links = []
    extra_links = []
    patch_links = []
    update_log(f"Fetching links from: {url} uwu~", "green")

    # Set up Chrome options to run headlessly (no Chrome window will open)
    options = Options()
    options.headless = True  # Run Chrome in headless mode

    try:
        # Set up the driver with webdriver_manager to automatically download ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Wait for the page to load, specifically look for elements with keywords like "GAME DOWNLOAD LINKS", "download", etc.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Handle Cloudflare or redirection if needed
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        # Grab links only under specific categories (ensure they have specific download patterns)
        links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
        for link in links:
            href = link.get_attribute("href")
            if href:
                # Categorize based on specific patterns for download links
                if re.search(r'(game|download)', href, re.IGNORECASE):
                    game_links.append(href)
                elif re.search(r'(extra|wallpaper|video)', href, re.IGNORECASE):
                    extra_links.append(href)
                elif re.search(r'(patch)', href, re.IGNORECASE):
                    patch_links.append(href)

        driver.quit()  # Close the browser

        if not game_links and not extra_links and not patch_links:
            update_log("No categorized download links found on this page~ uwu", "green")
        else:
            update_log(f"Found {len(game_links)} game download link(s) uwu~", "green")
            update_log(f"Found {len(extra_links)} extra download link(s) uwu~", "green")
            update_log(f"Found {len(patch_links)} patch download link(s) uwu~", "green")

    except Exception as e:
        update_log(f"Failed to fetch download links: {e} nya~", "green")

    return game_links, extra_links, patch_links

# Function to handle user selection and start the download process
def on_paste_and_download():
    url = url_text.get("1.0", "end-1c").strip()  # Get URL from the text field
    
    if not url:
        # If URL is empty, try pasting from clipboard
        url = pyperclip.paste()
        url_text.delete("1.0", END)
        url_text.insert("1.0", url)
    
    if url:
        update_log(f"Processing URL: {url} uwu~", "green")
        show_loading_animation()

        # Fetch categorized download links using Selenium
        game_links, extra_links, patch_links = fetch_download_links(url)
        stop_loading_animation()

        # Display categorized download links in the user interface
        display_download_options(game_links, extra_links, patch_links)

    else:
        update_log("No URL entered, nya~", "green")
        messagebox.showerror("Error", "Please paste or enter a URL to search for download links, nya~!")

# Function to display categorized download links in the interface
def display_download_options(game_links, extra_links, patch_links):
    # Hide the main window while the user selects a download link
    root.withdraw()

    # Create a new Toplevel window for the download link selection
    category_window = Toplevel(root)
    category_window.title("Select Download Link Category")

    # Create a frame for each category
    game_frame = Frame(category_window, bg="#F9C7D1")
    extra_frame = Frame(category_window, bg="#F9C7D1")
    patch_frame = Frame(category_window, bg="#F9C7D1")

    Label(game_frame, text="GAME DOWNLOAD LINKS:", font=("Comic Sans MS", 14, "bold"), fg="#FF99CC", bg="#F9C7D1").pack(pady=5)
    for link in game_links:
        Button(game_frame, text=link, command=lambda l=link: go_to_download_page(l), font=("Comic Sans MS", 12), fg="#FF99CC", bg="#FFFFFF", relief="solid", bd=2).pack(pady=5)

    Label(extra_frame, text="EXTRA DOWNLOAD LINKS:", font=("Comic Sans MS", 14, "bold"), fg="#FF99CC", bg="#F9C7D1").pack(pady=5)
    for link in extra_links:
        Button(extra_frame, text=link, command=lambda l=link: go_to_download_page(l), font=("Comic Sans MS", 12), fg="#FF99CC", bg="#FFFFFF", relief="solid", bd=2).pack(pady=5)

    Label(patch_frame, text="PATCH DOWNLOAD LINKS:", font=("Comic Sans MS", 14, "bold"), fg="#FF99CC", bg="#F9C7D1").pack(pady=5)
    for link in patch_links:
        Button(patch_frame, text=link, command=lambda l=link: go_to_download_page(l), font=("Comic Sans MS", 12), fg="#FF99CC", bg="#FFFFFF", relief="solid", bd=2).pack(pady=5)

    # Pack frames into the category window
    game_frame.pack(pady=10)
    extra_frame.pack(pady=10)
    patch_frame.pack(pady=10)

# Function to go to the download page from the selected link
def go_to_download_page(link):
    update_log(f"Redirecting to: {link} uwu~", "green")
    # Implement logic to go to the download page and get the actual downloadable file link
    # For example, handle Cloudflare redirection or download buttons
    options = Options()
    options.headless = True  # Use headless mode if you don't want to open a browser window
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(link)
    
    # Wait and handle download link finding (Example: find the download button and click it)
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Download')]"))).click()
    
    driver.quit()  # Close the browser after completing the task

# Setup GUI
root = Tk()
root.title("Bunni Cloud - By Rin (reen)")  # Set the program name and author info
root.configure(bg="#F9C7D1")  # Pastel pink background

# Load the pink cute icon (update the path to the correct one)
icon_image = Image.open("C:/Users/rinse/Downloads/Bunni Installer/rabbit_head_icon.ico")  # Correct the path
icon_image = icon_image.resize((32, 32))  # Resize the icon to fit the window
icon = ImageTk.PhotoImage(icon_image)

# Set the icon for the tkinter window
root.iconphoto(True, icon)

font_style = ("Comic Sans MS", 12)

def create_label(text, bg="#F9C7D1"):
    label = Label(root, text=text, bg=bg, font=("Comic Sans MS", 14, "bold"), fg="#FF99CC")
    label.pack(pady=10)

def create_button(text, command):
    button = Button(root, text=text, command=command, font=("Comic Sans MS", 12, "bold"), bg="#FF99CC", fg="white", relief="solid", bd=2, padx=20, pady=10)
    button.pack(pady=10)
    return button

create_label("UwU, enter the Game Download URL~")
url_text = Text(root, height=1, width=50, font=font_style)
url_text.pack(pady=5)

create_button("Check and Download UwU", on_paste_and_download)  # Use on_paste_and_download for the paste feature
create_button("Paste URL", paste_url)
create_button("UwU Copy Log", copy_to_clipboard)

log_label = Label(root, text="Log Output:", bg="#F9C7D1", font=("Comic Sans MS", 12, "bold"), fg="#FF99CC")
log_label.pack(pady=10)

log_text = Text(root, height=10, width=50, font=font_style, wrap=WORD, state=DISABLED)
log_text.pack(pady=5)

root.mainloop()
