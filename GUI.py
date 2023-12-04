import tkinter as tk
import requests #imported for python client
from tkinter import ttk #Imported for updating GUI style
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
def move_forward(currentState):
  currentState.config(text= "Current State: Forward")
  log_activity("Forward button clicked.")
  try:
    url_fwd = requests.get("http://192.168.1.17:4444/forward/", timeout=1) 
  except requests.exceptions.RequestException:
    currentState.config(text= "Current State: No Connection")
  else:
    return url_fwd.json()

# Function to move the robot backward through Flask App
def move_backward(currentState):
  currentState.config(text= "Current State: Backward")
  log_activity("Backward button clicked.")
  try:
    url_bwd = requests.get("http://192.168.1.17:4444/backward/", timeout=1) 
  except requests.exceptions.RequestException:
    currentState.config(text= "Current State: No Connection")
  else:
    return url_bwd.json()

# Function to move the robot left through Flask App
def move_left(currentState):
  currentState.config(text= "Current State: Left")
  log_activity("Move left button clicked.")
  try:
    url_left = requests.get("http://192.168.1.17:4444/left/", timeout=1) 
  except requests.exceptions.RequestException:
    currentState.config(text= "Current State: No Connection")
  else:
    return url_left.json()

# Function to move the robot right through Flask App
def move_right(currentState):
  currentState.config(text= "Current State: Right")
  log_activity("Move right button clicked.")
  try:
    url_right = requests.get("http://192.168.1.17:4444/right/", timeout=1) 
  except requests.exceptions.RequestException:
    currentState.config(text= "Current State: No Connection")
  else:
    return url_right.json()

# Function to stop the robot through Flask App
def move_stop(currentState):
  currentState.config(text= "Current State: Stop")
  log_activity("Stop button clicked.")
  try:
    url_stop = requests.get("http://192.168.1.17:4444/stop/", timeout=1) 
  except requests.exceptions.RequestException:
    currentState.config(text= "Current State: No Connection")
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
      log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=80, height=20)
      log_text.pack(expand=True, fill='both')

      # Insert the log content into the scrolled text widget
      log_text.insert(tk.END, content)

  except Exception as e:
      # Handle file not found or other exceptions
      print()
      messagebox.showerror("Error", f"Error opening log file: {e}")

def exit_logout(firstName,lastName,gui_window,loggedin_window): #Function to exit the program
  activity = f"----- {firstName} {lastName} has logged out.-----"
  log_activity(activity)
  gui_window.destroy()
  loggedin_window.destroy()
  root.deiconify()

def GUI(firstName,lastName,loggedin_win): #Function to create GUI after user logged in
  global state_label,user_window
  user_window = tk.Toplevel()
  user_window.title("GUI")
  user_window.geometry("800x460")

  # Create four grid cells as Frame widgets without background colors
  frame1 = tk.Frame(user_window, width=400, height=200, relief=tk.SUNKEN, borderwidth=2)
  frame1.grid(row=0, column=0, padx=2, pady=2)

  frame2 = tk.Frame(user_window, width=400, height=200, relief=tk.SUNKEN, borderwidth=2)
  frame2.grid(row=0, column=1, padx=2, pady=2)

  frame3 = tk.Frame(user_window, width=400, height=200, relief=tk.SUNKEN, borderwidth=2)
  frame3.grid(row=1, column=0, padx=2, pady=2)

  frame4 = tk.Frame(user_window, width=400, height=200, relief=tk.SUNKEN, borderwidth=2)
  frame4.grid(row=1, column=1, padx=2, pady=2)

  # Create a frame for direction buttons in the first grid cell
  direction_frame = tk.Frame(frame1)
  direction_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
  # Create a width for all the buttons
  button_width = 10
  # Add direction buttons to the frame
  btn_Label = ttk.Label(direction_frame, text="Direction Control Buttons")
  btn_fwd = ttk.Button(direction_frame, text="FWD", command=lambda: move_forward(current_state),width=button_width)
  btn_bkwd = ttk.Button(direction_frame, text="BKWD", command=lambda: move_backward(current_state),width=button_width)
  btn_left = ttk.Button(direction_frame, text="LEFT", command=lambda: move_left(current_state),width=button_width)
  btn_right = ttk.Button(direction_frame, text="RIGHT", command=lambda: move_right(current_state),width=button_width)
  btn_stop = ttk.Button(direction_frame, text="STOP", command=lambda: move_stop(current_state),width=button_width)
  btn_Label.grid(row=0, column=0,columnspan=2)
  btn_fwd.grid(row=1, column=0)
  btn_bkwd.grid(row=2, column=0)
  btn_left.grid(row=1, column=1)
  btn_right.grid(row=2, column=1)
  btn_stop.grid(row=1, column=2)

  # Define the lable for the movement state
  current_state = ttk.Label(direction_frame, text="Current State: No action now")
  current_state.grid(row=3, column=0)

  log_frame = tk.Frame(frame2)
  log_frame.grid(row=2, column=0, rowspan=2, columnspan=2)
  log_Label = ttk.Label(log_frame, text="Log feed information")
  log_Label.grid(row=0, column=0,columnspan=2)
  show_log_button = ttk.Button(log_frame, text="Show Log File", command=show_log_file)
  show_log_button.grid(row=3, column=0, pady=10)

  video_frame = tk.Frame(frame3)
  video_frame.grid(row=0, column=1, rowspan=2, columnspan=2)
  video_Label = ttk.Label(video_frame, text="Video feed information")
  video_Label.grid(row=0, column=0,columnspan=2)
  videoinput1_Label = ttk.Label(video_frame, text="")
  videoinput1_Label.grid(row=1, column=0,columnspan=2)
  videoinput2_Label = ttk.Label(video_frame, text="")
  videoinput2_Label.grid(row=2, column=0,columnspan=2)

  blank_frame = tk.Frame(frame4)
  blank_frame.grid(row=1, column=1, rowspan=2, columnspan=2)
  blank_Label = ttk.Label(blank_frame, text="Blank for future use")
  blank_Label.grid(row=0, column=0,columnspan=2)

  #Create an exit button to quite the program  
  exit_button = ttk.Button(user_window, text="Logout", command=lambda:exit_logout(firstName,lastName,user_window,loggedin_win))
  exit_button.grid(row=3, column=1, columnspan=2, padx=20, pady=10)
