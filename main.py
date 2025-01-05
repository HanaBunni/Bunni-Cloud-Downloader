import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import zipfile
import shutil
import tkinter as tk
from tkinter import messagebox
from tqdm import tqdm
import pyshortcuts  # For creating desktop shortcuts
import pyperclip
from PIL import Image, ImageTk

# Function to set up Selenium WebDriver with Chrome DevTools Protocol (CC)
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless Chrome for background operation
    chrome_options.add_argument('--remote-debugging-port=9222')  # Enable remote debugging
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Function to scrape game download links from a URL using Chrome DevTools Protocol (CC)
def scrape_game_links(url):
    try:
        print(f"Scraping game download links from URL: {url}")
        driver = setup_driver()
        driver.get(url)

        # Wait for the page to load completely and check for links
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))  # Wait for <a> tags to be loaded

        # Simulate interaction with the page if needed (e.g., scrolling, clicking a button)
        try:
            more_button = driver.find_element(By.ID, 'more-button')  # Adjust to the actual element ID or class
            more_button.click()  # Simulate clicking a button to reveal links
            time.sleep(2)  # Wait for content to load
        except Exception as e:
            print("No additional interaction needed, proceeding with links...")

        # Simulate scrolling to ensure dynamic content is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Give time for content to load

        # Print the page source for debugging purposes
        page_source = driver.page_source
        print(f"Page Source (first 500 characters):\n{page_source[:500]}")

        # Scrape game download links (filter links based on file types)
        links = driver.find_elements(By.TAG_NAME, 'a')
        game_links = [link.get_attribute('href') for link in links if link.get_attribute('href') and ('.rar' in link.get_attribute('href') or '.exe' in link.get_attribute('href') or '.zip' in link.get_attribute('href'))]

        if not game_links:
            print("No game download links found after scrolling, retrying...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

            # Retry to find game links after additional scrolling
            links = driver.find_elements(By.TAG_NAME, 'a')
            game_links = [link.get_attribute('href') for link in links if link.get_attribute('href') and ('.rar' in link.get_attribute('href') or '.exe' in link.get_attribute('href') or '.zip' in link.get_attribute('href'))]

        driver.quit()
        print(f"Found game download links: {game_links}")
        return game_links
    except Exception as e:
        print(f"Error occurred while scraping game download links: {e}")
        return []

# Function to display clickable links in a floating window
def show_links_window(links):
    root = tk.Tk()
    root.title("Available Links")
    root.geometry("300x300")
    root.config(bg="lavender")

    def on_link_click(link):
        download_file(link)

    for link in links:
        button = tk.Button(root, text=link, command=lambda link=link: on_link_click(link))
        button.pack(fill=tk.X, padx=5, pady=5)

    root.mainloop()

# Function to handle file download and show progress bar
def download_file(url):
    filename = os.path.basename(url)
    file_path = os.path.join(os.getcwd(), filename)

    with requests.get(url, stream=True) as response:
        total_size = int(response.headers.get('content-length', 0))
        with open(file_path, 'wb') as file, tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))

    # Extract the file if it's a zip archive
    if file_path.endswith('.zip'):
        extract_file(file_path)

# Function to extract the downloaded zip file and place it in C:\Games
def extract_file(zip_path):
    extract_folder = r'C:\Games'
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Check for executable file and create a shortcut
    for root_dir, _, files in os.walk(extract_folder):
        for file in files:
            if file.endswith('.exe'):
                executable_path = os.path.join(root_dir, file)
                create_shortcut(executable_path)
                break

    os.remove(zip_path)  # Delete the zip file after extraction

    # Show a cheerful message and close the program
    messagebox.showinfo("Success", "Yay! The file has been extracted successfully! uwu")
    exit()

# Function to create a shortcut on the desktop
def create_shortcut(executable_path):
    shortcut = pyshortcuts.make_shortcut(executable_path, name="Game Shortcut", folder=os.path.expanduser("~/Desktop"))
    shortcut.create()

# Function to force the program to close when the user exits
def close_program(root):
    root.quit()

# Main function to control the flow
def main():
    root = tk.Tk()
    root.title("Link Scraper")
    root.geometry("500x400")
    root.config(bg="lavender")

    # Create a URL input field
    url_var = tk.StringVar()
    url_entry = tk.Entry(root, textvariable=url_var, width=40, font=("Arial", 14))
    url_entry.pack(pady=20)

    # Button to paste the URL into the textbox
    def on_paste_url():
        url = pyperclip.paste()
        print(f"Pasted URL: {url}")
        url_var.set(url)

    paste_button = tk.Button(root, text="Paste URL", command=on_paste_url, font=("Arial", 14), bg="pink")
    paste_button.pack(pady=10)

    # Button to scrape links from the URL in the textbox
    def on_scrape_links():
        url = url_var.get()
        print(f"Scraping URL: {url}")
        links = scrape_game_links(url)
        if links:
            show_links_window(links)
        else:
            messagebox.showerror("Error", "No links found on the page!")

    scrape_button = tk.Button(root, text="Scrape Links", command=on_scrape_links, font=("Arial", 14), bg="lightgreen")
    scrape_button.pack(pady=10)

    # Exit button
    exit_button = tk.Button(root, text="Exit", command=lambda: close_program(root), font=("Arial", 14), bg="lightblue")
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
