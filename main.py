import itertools
import json
import time
import multiprocessing as mp
import psutil
import tkinter as tk
from tkinter import ttk

def send_progress(progress, total_combinations, start_time):
    window = tk.Tk()
    window.title("Password Generation Progress")

    style = ttk.Style()
    style.theme_use('clam')  # Use a different theme (change 'clam' to your preferred theme)

    # Configure the style for the labels and frame
    style.configure("TLabel", font=("Arial", 14), foreground="black")
    style.configure("TFrame", background="white")

    frame = ttk.Frame(window)
    frame.grid(row=0, column=0, padx=10, pady=10)

    # Create labels with flexible columns
    progress_label = ttk.Label(frame, text="Progress: 0%", style="TLabel")
    progress_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    count_label = ttk.Label(frame, text="Count: 0", style="TLabel")
    count_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    rate_label = ttk.Label(frame, text="Generation Rate: 0 per second", style="TLabel")
    rate_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    # Function to update labels
    def update_labels():
        current_time = time.time()
        elapsed_time = current_time - start_time
        with progress.get_lock():
            generated_count = progress.value
            percentage = (generated_count / total_combinations) * 100
        generation_rate = generated_count / elapsed_time

        progress_str = f"Progress: {percentage:.2f}%"
        progress_label.config(text=progress_str)

        count_str = f"Count: {generated_count}"
        count_label.config(text=count_str)

        rate_str = f"Generation Rate: {generation_rate:.2f} per second"
        rate_label.config(text=rate_str)

        if generated_count < total_combinations:
            window.after(1000, update_labels)

    window.after(1000, update_labels)

    # Resize the frame and its contents when the window is resized
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(3, weight=1)

    window.mainloop()

def generate_passwords_worker(start, end, progress, total_combinations, digits, max_digits, delay, cpu_percentage):
    passwords = itertools.product(digits, repeat=max_digits)
    local_progress = 0

    with open("wordlist.txt", "a") as file:
        for idx, password in enumerate(passwords):
            if start <= idx < end:
                password_str = "".join(password)
                file.write(password_str + "\n")

                local_progress += 1
                with progress.get_lock():
                    progress.value += 1

                if delay > 0:
                    time.sleep(delay)

            # Check CPU usage and adjust sleep time to limit CPU percentage
            while psutil.cpu_percent() >= cpu_percentage:
                time.sleep(0.1)

def generate_passwords():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    
    digits = "0123456789"
    min_digits = config.get("min_digits", 8)
    max_digits = config.get("max_digits", 8)
    delay = config.get("delay", 0)
    cpu_percentage = config.get("cpu_percentage", 40)
    num_processes = config.get("num_processes", mp.cpu_count())

    total_combinations = 0
    for length in range(min_digits, max_digits + 1):
        total_combinations += len(digits) ** length

    progress = mp.Value('i', 0)

    # Start the progress update process
    start_time = time.time()
    progress_process = mp.Process(target=send_progress, args=(progress, total_combinations, start_time))
    progress_process.start()

    # Divide the work among multiple processes
    processes = []
    chunk_size = total_combinations // num_processes
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else total_combinations
        process = mp.Process(target=generate_passwords_worker,
                             args=(start, end, progress, total_combinations, digits, max_digits, delay, cpu_percentage))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Terminate the progress update process
    progress_process.terminate()

    print("Wordlist generation completed!")

if __name__ == '__main__':
    generate_passwords()
