import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import time

file_path = None

def generate_forecast(df_temperature):
    # Set the length of the time series and the range of values
    length = df_temperature.shape[0]
    min_val = -0.1
    max_val = 0.1
    # Generate a random time series between 0 and 1
    ts = np.random.rand(length)
    # Scale the time series to be between min_val and max_val
    ts = (ts - np.min(ts)) / (np.max(ts) - np.min(ts)) * (max_val - min_val) + min_val
    # Convert the time series to a pandas DataFrame
    df_noise = pd.DataFrame({'value': ts})
    # Calculate the adjusted temperature values and store them in a new column in the original DataFrame
    df_temperature = df_temperature.assign(forecasted_temperature=df_temperature['Indoor_temperature_room'] + df_temperature['Indoor_temperature_room'] * df_noise['value'])
    y = df_temperature['forecasted_temperature']
    # Smooth the data using a rolling average
    window_size = 5
    y_smooth = np.convolve(y, np.ones(window_size)/window_size, mode='same')
    df_temperature['forecasted_temperature_smothed'] = y_smooth
    return df_temperature


def plot_data(file_path):
    # Read the time series data into a Pandas DataFrame
    df_temperature = pd.read_excel(file_path)
    df_temperature = generate_forecast(df_temperature)

    # Create the Matplotlib figure and plot the time series data
    fig = plt.Figure(figsize=(20,20), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(df_temperature['Indoor_temperature_room'][2:300], color='red', label='Original Temperature')
    ax.plot(df_temperature['forecasted_temperature_smothed'][2:300], color='blue', label='Forecasted Temperature')

    ax.set_xlabel('Time(h)')
    ax.set_ylabel('Temperature')
    ax.set_title('Time Series Forecast')
    ax.legend()

    # Create a new frame for the plot
    plot_frame = tk.Frame(root)
    plot_frame.pack(padx=15, pady=10)

    # Create the Tkinter Canvas widget to display the Matplotlib figure in the new frame
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def show_progress():
    progress_frame = tk.Frame(root)
    progress_frame.pack(pady=10)
    progress_label = tk.Label(progress_frame, text="We're generating predictions for you. This may take a moment.", font=('Bold', 14))
    progress_label.pack(side=tk.TOP, pady=5)
    progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=5)
    progress_percent = tk.Label(progress_frame, text="0%")
    progress_percent.pack(side=tk.BOTTOM, pady=5)

    for i in range(101):
        progress_bar['value'] = i
        progress_percent.config(text=f"{i}%")
        root.update_idletasks()
        time.sleep(0.1)

    progress_frame.destroy()


def upload_file():
    # Get the file path using a file dialog
    global file_path
    file_path = filedialog.askopenfilename()

def submit_file():
    # Show progress bar for 5 seconds
    show_progress()
    # Plot the data
    plot_data(file_path)
# Create the Tkinter window
root = tk.Tk()
root.title('Smart Temperature Forecaster')
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# Create the main frame with a boundary
main_frame = tk.Frame(root, bd=2, relief='groove')
main_frame.pack(padx=20, pady=20)

# Load the image file
img = tk.PhotoImage(file='Resources/background.png')

# Get the width and height of the image
img_width = img.width()
img_height = img.height()

# Create a canvas widget with the same size as the image, inside the main frame
canvas = tk.Canvas(main_frame, width=img_width, height=img_height/2, bg='blue')
canvas.pack()

# Create the background image
canvas.create_image(0, 0, anchor=tk.NW, image=img)

# Create a custom style for the buttons
style = ttk.Style()
style.configure('Custom.TButton', background='#00A1E4', foreground='white', font=('Arial', 12, 'bold'))


# Create a frame for the buttons with a boundary
buttons_frame = tk.Frame(main_frame, bd=1, relief='groove')
buttons_frame.place(x=280, y=100)

# Create the file upload button
upload_button = ttk.Button(buttons_frame, text="Upload Data", command=upload_file, style='Custom.TButton')
upload_button.pack(side=tk.LEFT, padx=5, pady=5)


# Create a button to submit the file
submit_button = ttk.Button(buttons_frame, text='Submit', command=submit_file, style='Custom.TButton')
submit_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a "Powered by AI" label
powered_by_ai_label = tk.Label(root, text="Powered by AI", font=("Arial", 12, "bold"), fg="black", bg="#00A1E4")
powered_by_ai_label.pack(side=tk.BOTTOM, pady=10)

# Run the Tkinter event loop
root.mainloop()