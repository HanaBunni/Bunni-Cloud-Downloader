import os
import subprocess
import sys
import random
import threading

# Ensure rarfile module is installed
try:
    import rarfile
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rarfile"])
    import rarfile

import pyperclip
import requests
import shutil
import time
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Setup GUI
root = Tk()
root.title("Bunni Cloud Downloader - By Rin (reen)")  # Set the program name and author info
root.configure(bg="#F9C7D1")  # Pastel pink background

# Load the pink cute icon (update the path to the correct one)
icon_image = Image.open("C:/Users/rinse/Downloads/Bunni-Cloud-Downloader/bunni_cloud_downloader.ico")  # Correct the path
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

def paste_url():
    url = pyperclip.paste()  # Get the content from the clipboard
    url_text.delete("1.0", END)  # Clear any current text
    url_text.insert("1.0", url)  # Insert the new URL

def fetch_links():
    url = url_text.get("1.0", "end-1c").strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        ])
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        time.sleep(random.uniform(1, 3))  # Random delay to mimic human behavior
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

        if not links:
            messagebox.showerror("Error", "No links found.")
            return

        display_links(links)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch links: {e}")

def fetch_gog_games_links():
    url = url_text.get("1.0", "end-1c").strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        ])
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if 'gog-games.to' in a['href']]

        if not links:
            messagebox.showerror("Error", "No links found.")
            return

        display_links(links)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch links: {e}")

def display_links(links):
    link_window = Toplevel(root)
    link_window.title("Select Download Link")
    link_window.configure(bg="#FFB6C1")

    for link in links:
        link_button = Button(link_window, text=link, font=("Comic Sans MS", 12), fg="#FF69B4", bg="#FFFFFF", relief="solid", bd=2, wraplength=400, command=lambda l=link: start_download(l))
        link_button.pack(pady=5)

def start_download(link):
    download_window = Toplevel(root)
    download_window.title("Downloading...")
    download_window.configure(bg="#FFB6C1")

    progress_label = Label(download_window, text="Downloading...", font=("Comic Sans MS", 14, "bold"), fg="#FF69B4", bg="#FFB6C1")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(download_window, orient=HORIZONTAL, length=300, mode='determinate')
    progress_bar.pack(pady=10)

    def download_file():
        local_filename = link.split('/')[-1]
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
            ])
        }
        with requests.get(link, headers=headers, stream=True) as r:
            total_length = int(r.headers.get('content-length', 0))
            progress_bar['maximum'] = total_length
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        progress_bar['value'] += len(chunk)
                        download_window.update_idletasks()

        extract_and_setup(local_filename)
        download_window.destroy()

    download_thread = threading.Thread(target=download_file)
    download_thread.start()

def extract_and_setup(filename):
    extract_path = "C:/Games"
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    with rarfile.RarFile(filename) as rf:
        rf.extractall(extract_path)

    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if file.endswith('.exe'):
                exe_path = os.path.join(root, file)
                create_shortcut(exe_path, "Bunni Cloud Downloader")

    os.remove(filename)
    show_completion_message()

def create_shortcut(target, name):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shortcut_path = os.path.join(desktop, f"{name}.lnk")
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.save()

def show_completion_message():
    messagebox.showinfo("Success", "Download and setup complete! UwU")
    root.destroy()

def force_close():
    root.destroy()
    os._exit(0)

create_label("UwU, enter the Game Download URL~")
url_text = Text(root, height=1, width=50, font=font_style)
url_text.pack(pady=5)

create_button("Check and Download UwU", fetch_links)
create_button("Paste URL", paste_url)
create_button("UwU Copy Log", lambda: None)  # Placeholder command

log_label = Label(root, text="Log Output:", bg="#F9C7D1", font=("Comic Sans MS", 12, "bold"), fg="#FF99CC")
log_label.pack(pady=10)

# Make the log window look like a terminal
log_text = Text(root, height=10, width=50, font=("Courier New", 12), wrap=WORD, state=DISABLED, bg="black", fg="white")
log_text.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", force_close)
root.mainloop()