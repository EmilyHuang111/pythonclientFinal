import tkinter as tk
import requests  #imported for python client
from tkinter import ttk  #Imported for updating GUI style
import logging
from tkinter import messagebox
from tkinter import scrolledtext

# Root Menu for user registration and login
root = tk.Tk()
root.title("User Login")
#define style
style = ttk.Style(root)
style.theme_use("clam")

#Create a log file to track activities
# Set up logging
logging.basicConfig(
    filename='activity_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def log_activity(message):
  logging.info(message)


# Function to move the robot forward through Flask App
def move_forward(currentState, userName):
  currentState.config(text="Current State: Forward")
  log_activity(f"{userName} has clicked Forward button.")
  try:
    url_fwd = requests.get("http://192.168.1.17:4444/forward", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_fwd.json()


# Function to move the robot backward through Flask App
def move_backward(currentState, userName):
  currentState.config(text="Current State: Backward")
  log_activity(f"{userName} has clicked Backward button.")
  try:
    url_bwd = requests.get("http://192.168.1.17:4444/backward", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_bwd.json()


# Function to move the robot left through Flask App
def move_left(currentState, userName):
  currentState.config(text="Current State: Left")
  log_activity(f"{userName} has clicked Left Move button.")
  try:
    url_left = requests.get("http://192.168.1.17:4444/left", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_left.json()


# Function to move the robot right through Flask App
def move_right(currentState, userName):
  currentState.config(text="Current State: Right")
  log_activity(f"{userName} has clicked Right Move button.")
  try:
    url_right = requests.get("http://192.168.1.17:4444/right", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_right.json()


# Function to start the robot through Flask App
def move_start(currentState, userName):
  currentState.config(text="Current State: Start")
  log_activity(f"{userName} has clicked Start button.")
  try:
    url_start = requests.get("http://192.168.1.17:4444/start", timeout=1)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_start.json()


# Function to stop the robot through Flask App
def move_stop(currentState, userName):
  currentState.config(text="Current State: Stop")
  log_activity(f"{userName} has clicked Stop button.")
  try:
    url_stop = requests.get("http://192.168.1.17:4444/stop", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_stop.json()


def show_log_file():
  try:
    # Replace 'your_log_file.txt' with the actual name of your log file
    log_file_path = 'activity_log.txt'

    with open(log_file_path, 'r') as file:
      content = file.read()

    # Create a new top-level window for displaying the log content
    log_window = tk.Toplevel()
    log_window.title("Log File Content")

    # Create a scrolled text widget with a scroll bar
    log_text = scrolledtext.ScrolledText(log_window,
                                         wrap=tk.WORD,
                                         width=80,
                                         height=20)
    log_text.pack(expand=True, fill='both')

    # Insert the log content into the scrolled text widget
    log_text.insert(tk.END, content)

  except Exception as e:
    # Handle file not found or other exceptions
    print()
    messagebox.showerror("Error", f"Error opening log file: {e}")


def exit_logout(firstName, lastName, userName, gui_window,
                loggedin_window):  #Function to exit the program
  activity = f"{userName} has logged out."
  log_activity(activity)
  gui_window.destroy()
  loggedin_window.destroy()
  root.deiconify()


def GUI(firstName, lastName, user_name,
        loggedin_win):  #Function to create GUI after user logged in
  global state_label, user_window
  user_window = tk.Toplevel()
  user_window.title("GUI")
  user_window.geometry("450x300")

  # Create four grid cells as Frame widgets without background colors
  frame1 = tk.Frame(user_window,
                    width=400,
                    height=200,
                    relief=tk.SUNKEN,
                    borderwidth=2)
  frame1.grid(row=0, column=1, padx=2, pady=2)

  frame2 = tk.Frame(user_window,
                    width=400,
                    height=200,
                    relief=tk.SUNKEN,
                    borderwidth=2)
  frame2.grid(row=1, column=1, padx=2, pady=2)

  frame3 = tk.Frame(user_window,
                    width=400,
                    height=200,
                    relief=tk.SUNKEN,
                    borderwidth=2)
  frame3.grid(row=0, column=0, padx=2, pady=2)

  frame4 = tk.Frame(user_window,
                    width=400,
                    height=200,
                    relief=tk.SUNKEN,
                    borderwidth=2)
  frame4.grid(row=1, column=0, padx=2, pady=2)

  # Create a frame for direction buttons in the first grid cell
  direction_frame = tk.Frame(frame1)
  direction_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
  # Create a width for all the buttons
  button_width = 3
  # Add direction buttons to the frame
  btn_Label = ttk.Label(direction_frame, text="Direction Control Buttons")
  btn_fwd = ttk.Button(direction_frame,
                       text="↑",
                       command=lambda: move_forward(current_state, user_name),
                       width=button_width)
  btn_bkwd = ttk.Button(
      direction_frame,
      text="↓",
      command=lambda: move_backward(current_state, user_name),
      width=button_width)
  btn_left = ttk.Button(direction_frame,
                        text="←",
                        command=lambda: move_left(current_state, user_name),
                        width=button_width)
  btn_right = ttk.Button(direction_frame,
                         text="→",
                         command=lambda: move_right(current_state, user_name),
                         width=button_width)
  btn_stop = ttk.Button(direction_frame,
                        text="●",
                        command=lambda: move_stop(current_state, user_name),
                        width=button_width,
                        style='Red.TButton')
  btn_start = ttk.Button(direction_frame,
                         text="●",
                         command=lambda: move_start(current_state, user_name),
                         width=button_width,
                         style='Green.TButton')
  btn_Label.grid(row=0, column=0, columnspan=5)

  btn_fwd.grid(row=1, column=2)
  btn_bkwd.grid(row=3, column=2)
  btn_start.grid(row=2, column=1, padx=0)
  btn_stop.grid(row=2, column=3)
  btn_left.grid(row=2, column=0, padx=0)
  btn_right.grid(row=2, column=4)

  # Define the lable for the movement state
  current_state = ttk.Label(direction_frame,
                            text="Current State: No action now")
  current_state.grid(row=4, column=0, columnspan=5)

  log_frame = tk.Frame(frame2)
  log_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
  log_Label = ttk.Label(log_frame,
                        text="Log feed information                 ")
  log_Label.grid(row=0, column=0, columnspan=2)
  show_log_button = ttk.Button(log_frame,
                               text="Show Log File",
                               command=show_log_file)
  show_log_button.grid(row=1, column=0, pady=10)

  video_frame = tk.Frame(frame3)
  video_frame.grid(row=0, column=1, rowspan=2, columnspan=2)
  video_Label = ttk.Label(video_frame, text="Video feed with image overlay")
  video_Label.grid(row=0, column=0, columnspan=2)
  videoinput1_Label = ttk.Label(video_frame, text="")
  videoinput1_Label.grid(row=1, column=0, columnspan=2)
  videoinput2_Label = ttk.Label(video_frame, text="")
  videoinput2_Label.grid(row=2, column=0, columnspan=2)

  blank_frame = tk.Frame(frame4)
  blank_frame.grid(row=0, column=1, rowspan=2, columnspan=2)
  blank_Label = ttk.Label(blank_frame,
                          text="Video Stream                       ")
  blank_Label.grid(row=2, column=0, columnspan=2)
  blankinput1_Label = ttk.Label(blank_frame, text="")
  blankinput1_Label.grid(row=3, column=0, columnspan=2)
  blankinput2_Label = ttk.Label(blank_frame, text="")
  blankinput2_Label.grid(row=4, column=0, columnspan=2)

  #Create an exit button to quite the program
  exit_button = ttk.Button(
      user_window,
      text="Logout",
      command=lambda: exit_logout(firstName, lastName, user_name, user_window,
                                  loggedin_win))
  exit_button.grid(row=3, column=1, columnspan=2, padx=20, pady=10)


# Create a custom style for the red stop button
style.configure('Red.TButton', foreground='red')
# Create a custom style for the green start button
style.configure('Green.TButton', foreground='green')
