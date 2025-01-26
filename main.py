import tkinter as tk
from tkinter import PhotoImage, messagebox
import tkinter.font as tkFont
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

class BunniCloudDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_fonts()
        self.create_widgets()
        self.gathered_links = []

    def setup_window(self):
        self.root.title("Bunni Cloud Downloader")
        self.root.geometry("600x400")
        self.root.configure(bg="#f9d1d1")
        
        # Use relative path for images
        image_path = os.path.join(os.path.dirname(__file__), "assets", "pink-anime-girl.png")
        if os.path.exists(image_path):
            self.icon_image = PhotoImage(file=image_path)
            self.root.iconphoto(True, self.icon_image)
            self.background_image = PhotoImage(file=image_path)
            background_label = tk.Label(self.root, image=self.background_image)
            background_label.place(relwidth=1, relheight=1)

    def setup_fonts(self):
        self.font_title = tkFont.Font(family="Comic Sans MS", size=26, weight="bold")
        self.font_button = tkFont.Font(family="Comic Sans MS", size=14, weight="bold")
        self.font_label = tkFont.Font(family="Arial", size=14)
        self.font_entry = tkFont.Font(family="Arial", size=12)
        self.font_footer = tkFont.Font(family="Comic Sans MS", size=10)

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Bunni Cloud Downloader", 
                             font=self.font_title, fg="white", bg="#f9d1d1")
        title_label.pack(pady=10)

        # URL Entry
        self.url_frame = tk.Frame(self.root, bg="#f9d1d1")
        self.url_frame.pack(pady=20)

        self.url_entry = tk.Entry(self.url_frame, font=self.font_entry, 
                                width=30, bd=4, relief="solid", 
                                bg="#fff0f5", fg="#ff69b4")
        self.url_entry.insert(0, "Enter URL")
        self.url_entry.bind("<FocusIn>", self.on_entry_click)
        self.url_entry.bind("<FocusOut>", self.on_focus_out)
        self.url_entry.pack(side=tk.LEFT, padx=5)

        # Paste button
        paste_button = tk.Button(self.url_frame, text="📋 Paste", 
                               font=self.font_button, bg="#ffb6c1", 
                               fg="white", command=self.paste_url)
        paste_button.pack(side=tk.LEFT, padx=5)

        # Start button
        self.start_button = tk.Button(self.root, text="✨ Start Gathering", 
                                    font=self.font_button, bg="#f9d1d1", 
                                    fg="white", command=self.start_gathering)
        self.start_button.pack(pady=20)

        # Footer
        footer_label = tk.Label(self.root, text="Powered by Bunni Cloud", 
                              font=self.font_footer, fg="white", bg="#f9d1d1")
        footer_label.pack(side="bottom", pady=10)

    def on_entry_click(self, event):
        if self.url_entry.get() == "Enter URL":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg="#ff69b4")

    def on_focus_out(self, event):
        if self.url_entry.get() == "":
            self.url_entry.insert(0, "Enter URL")
            self.url_entry.config(fg="gray")

    def paste_url(self):
        url = pyperclip.paste()
        if url:
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)

    def is_valid_url(self, url):
        return url.startswith(("http://", "https://"))

    def start_gathering(self):
        url = self.url_entry.get()
        if url == "Enter URL" or not url:
            messagebox.showwarning("Warning", "Please enter a URL!")
            return

        if not self.is_valid_url(url):
            messagebox.showwarning("Warning", "Please enter a valid URL starting with http:// or https://")
            return

        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                                    options=options)
            
            driver.get(url)
            
            # Wait for elements to load with timeout
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
            
            links = driver.find_elements(By.TAG_NAME, "a")
            self.gathered_links = [link.get_attribute("href") for link in links 
                                 if link.get_attribute("href")]
            
            if self.gathered_links:
                self.show_gathered_links()
            else:
                messagebox.showinfo("Info", "No links found on the page.")
                
        except TimeoutException:
            messagebox.showerror("Error", "Timeout while loading the page. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            driver.quit()

    def show_gathered_links(self):
        links_window = tk.Toplevel(self.root)
        links_window.title("Gathered Links")
        links_window.geometry("500x400")
        links_window.configure(bg="#f9d1d1")
        
        # Add scrollbar and text widget
        scrollbar = tk.Scrollbar(links_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(links_window, wrap=tk.WORD, 
                            yscrollcommand=scrollbar.set,
                            font=self.font_entry, bg="#fff0f5", fg="#ff69b4")
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        scrollbar.config(command=text_widget.yview)
        
        # Insert links
        for i, link in enumerate(self.gathered_links, 1):
            text_widget.insert(tk.END, f"{i}. {link}\n")
        
        text_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = BunniCloudDownloader()
    app.root.mainloop()
