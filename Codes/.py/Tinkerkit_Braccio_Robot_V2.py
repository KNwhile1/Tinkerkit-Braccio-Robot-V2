# =====================================================================================================================
# Name: Tinkerkit_Braccio_Robot_V2
# Description: This program allows control of a Braccio robotic arm through serial communication.
# Target: Arduino Uno
# Compiler: PYcharm
# Usage: Control the Braccio robot using Python
# Restriction(s): None.
# History: 7/05/2024 | E. Zoukou / C. Courtemanche / K. Niamba / Creation;
#          1/28/2025 | K. Niamba / Modification ---> Documentation translation (FR to ENG);
# =====================================================================================================================

# =====================================================================================================================
# Including files
# =====================================================================================================================
import serial
from tkinter import *
import tkinter as tk
from tkinter import ttk
import time

# =====================================================================================================================
# Global variables
# =====================================================================================================================
global sel
combo_box = None

# =====================================================================================================================
# Speed function
# =====================================================================================================================
def Speed(Win):
    global v
    # -------------------------------------------------
    # Initialize the variable to store speed
    # -------------------------------------------------
    v = StringVar(Win, "1")
    options = {"10": "10",
               "20": "20",
               "30": "30"}
    # -------------------------------------------------
    # Create the interface to choose the speed
    # -------------------------------------------------
    Speed_Label = ttk.Label(Win, text="Speed (sec):")
    Speed_Label.pack()
    Speed_Label.place(x=550, y=175, width=125, height=30)

    # -------------------------------------------------
    # Place radio buttons to choose speed
    # -------------------------------------------------
    row_index = 2
    column_index = 1

    for (txt, val) in options.items():
        rb = Radiobutton(Win, text=txt, variable=v, value=val)
        rb.grid(row=row_index, column=column_index, pady=5, padx=625, sticky=W+E+N+S)
        row_index += 1                                # Increment for the next radio button

    return v

# =====================================================================================================================
# Function to select a motor
# =====================================================================================================================
options = ["base", "shoulder", "elbow", "vertical wrist", "rotatory wrist", "gripper"]
def Choice():
    global sel
    global combo_box
    global choice1
    # -------------------------------------------------
    # Internal function to manage selection in the combobox
    # -------------------------------------------------
    def select(event):
        global choice1
        global sel
        sel = combo_box.get()                        # Get the selected item from the combobox
        choice1.set(sel)
        create_scale(choice1)                        # Call the function to create the scale
        return sel

    # -------------------------------------------------
    # Create the combobox to choose the motor
    # -------------------------------------------------
    combo_box = ttk.Combobox(Win, values=options, width= 25)
    combo_box.current(4)                             # Select an item by default
    combo_box.place(x=200, y=225, width=200)

    combo_box.bind('<<ComboboxSelected>>', select)   # Associate the select function to the selection event
    Motor_Label = ttk.Label(Win, text="Choose the servomotor:")
    Motor_Label.place(x=200, y=175, width=200, height=30)

    choice1=StringVar()

    return combo_box

# =====================================================================================================================
# Function for the scale (angle adjustment for motors)
# =====================================================================================================================
def create_scale(choice1):
    global scale

    if choice1:
        v = DoubleVar()
        
        # -------------------------------------------------
        # Create the scale based on the motor choice
        # -------------------------------------------------
        if choice1.get() == "gripper":
            scale = Scale(Win, variable=v, from_=0, to=73, orient=VERTICAL)
        elif choice1.get() == "base":
            scale = Scale(Win, variable=v, from_=0, to=360, orient=VERTICAL)
        else:
            scale = Scale(Win, variable=v, from_=0, to=180, orient=VERTICAL)

        scale.place(x=425, y=250, width=50, height=150)
        return v
    else:
        print("No selection made")                   # Debugging message
        return None

# =====================================================================================================================
# Function to save values
# =====================================================================================================================
M = [0]*6

def Save(choice1):
    selected_motor = choice1.get()
    value = scale.get()
    speed = v.get()

    if selected_motor == "base":
        M[0] = value
        Display_M1.config(font=("Arial", 12, "italic"), text="Base: "+str(M[0]))

    elif selected_motor == "shoulder":
        M[1] = value
        Display_M2.config(font=("Arial", 12, "italic"), text="Shoulder: "+str(M[1]))

    elif selected_motor == "elbow":
        M[2] = value
        Display_M3.config(font=("Arial", 12, "italic"), text="Elbow: "+str(M[2]))

    elif selected_motor == "vertical wrist":
        M[3] = value
        Display_M4.config(font=("Arial", 12, "italic"), text="Vertical Wrist: " + str(M[3]))

    elif selected_motor == "rotatory wrist":
        M[4] = value
        Display_M5.config(font=("Arial", 12, "italic"), text="Rotatory Wrist: " + str(M[4]))

    elif selected_motor == "gripper":
        M[5] = value
        Display_M6.config(font=("Arial", 12, "italic"), text="Gripper: " + str(M[5]))

    # -------------------------------------------------
    # Prepare updated lines for the file
    # -------------------------------------------------
    updated_lines = []

    # -------------------------------------------------
    # Update the motor values in the file
    # -------------------------------------------------
    with open('Info_Objets', 'r+') as file:
        lines = file.readlines()
        file.seek(0)

        for line in lines:
            if line.startswith(f"{selected_motor}:"):
                updated_lines.append(f"{selected_motor}: {value}\n")
            else:
                updated_lines.append(line)

        # -------------------------------------------------
        # Update or add the line "speed" with the current value
        # -------------------------------------------------
        for line in updated_lines:
            if line.startswith("speed:"):
                updated_lines.remove(line)
                updated_lines.append(f"speed: {speed}\n")
                break

        # -------------------------------------------------
        # Truncate the file and write the updated content
        # -------------------------------------------------
        file.truncate()
        file.writelines(updated_lines)
    return value

# =====================================================================================================================
# Function to send data to Arduino
# =====================================================================================================================
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
def write_read(data):
    arduino.write(data.encode())
    arduino.flushInput()
    time.sleep(0.5)
    response = arduino.readline().decode().strip()
    print("Response from Arduino:", response)
    return response

# =====================================================================================================================
# Function to reset
# =====================================================================================================================
def Reset():
    send_list = ":".join([str(val) for val in [30,90,90,90,90,90,90]])
    print(send_list)
    response = write_read(send_list + '\n')
    print(send_list)

def Start():
    with open("Info_Objets", "r") as file:
        lines = file.readlines()

    m1 = m2 = m3 = m4 = m5 = m6 = speed = None

    for line in lines:
        parts = line.split(":")
        if len(parts) == 2:
            param = parts[0].strip().lower()
            value = int(parts[1].strip())

            if param == "base":
                m1 = value
            elif param == "shoulder":
                m2 = value
            elif param == "elbow":
                m3 = value
            elif param == "vertical wrist":
                m4 = value
            elif param == "rotatory wrist":
                m5 = value
            elif param == "gripper":
                m6 = value
            elif param == "speed":
                speed = value

    if all([m1, m2, m3, m4, m5, m6, speed]):
        send_list = ":".join([str(val) for val in [speed, m1, m2, m3, m4, m5, m6]])
        print(send_list)
        response = write_read(send_list+'\n')
        print("Response from Arduino:", response)
    else:
        print("Make sure all motor angles are entered and a speed is selected!")

# =====================================================================================================================
# Function to quit
# =====================================================================================================================
def Quit():
    file = open('Info_Objets', 'w')
    file.write("")
    file.close()
    Win.destroy()
    return

# =====================================================================================================================
# Main program #1
# =====================================================================================================================
Win = Tk()
Win.title("BRACCIO ROBOT ARM CONTROL")
Win.option_add("*Font", "Helvetica 12 bold")
Win.geometry("900x550")
Win.configure(bg="#FF69B4")
Win.grid_columnconfigure(0, weight=1)
Win.grid_columnconfigure(6, weight=1)
Win.grid_rowconfigure(0, weight=1)
Win.grid_rowconfigure(6, weight=1)

# -------------------------------------------------
# Label to display the selected angle for each motor
# -------------------------------------------------
Display_M1 = ttk.Label(Win, text="")
Display_M1.pack()
Display_M1.place(x=25, y=175, width=150, height=30)

Display_M2 = ttk.Label(Win, text="")
Display_M2.pack()
Display_M2.place(x=25, y=225, width=150, height=30)

Display_M3 = ttk.Label(Win, text="")
Display_M3.pack()
Display_M3.place(x=25, y=275, width=150, height=30)

Display_M4 = ttk.Label(Win, text="")
Display_M4.pack()
Display_M4.place(x=25, y=325, width=150, height=30)

Display_M5 = ttk.Label(Win, text="")
Display_M5.pack()
Display_M5.place(x=25, y=375, width=150, height=30)

Display_M6 = ttk.Label(Win, text="")
Display_M6.pack()
Display_M6.place(x=25, y=425, width=150, height=30)

# -------------------------------------------------
# Font for labels
# -------------------------------------------------
Display_M1.config(font=("Arial", 12, "italic"))
Display_M2.config(font=("Arial", 12, "italic"))
Display_M3.config(font=("Arial", 12, "italic"))
Display_M4.config(font=("Arial", 12, "italic"))
Display_M5.config(font=("Arial", 12, "italic"))
Display_M6.config(font=("Arial", 12, "italic"))

# =====================================================================================================================
# Function to get the active COM port
# =====================================================================================================================
def get_active_com_port():
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "COM3" in port.device:
            return port.device
    return "No active COM port found"                # Default message if COM3 is not found

def update_label_text():
    Port_Serie.config(text="Active COM port: " + get_active_com_port())
    Win.after(1000, update_label_text)               # Update every second

Port_Serie = ttk.Label(Win, text="Active COM port: " + get_active_com_port())
Port_Serie.pack()
Port_Serie.place(x=350, y=75, width=175, height=30)  # Creating the Tkinter window

Transmission_Speed = ttk.Label(Win, text="Transmission speed: 9600 baud")
Transmission_Speed.pack()
Transmission_Speed.place(x=300, y=25, width=290, height=30)

# =====================================================================================================================
# Create buttons
# =====================================================================================================================
def set_font_style(widget, size):
    widget.config(font=("Comic Sans MS", size))

save_button = tk.Button(Win, text="Save", command=lambda: Save(choice1), bg="white")
Win.bind("<Control-e>", lambda event: Save(choice1)) # Shortcut to activate the function
set_font_style(save_button, 12)
save_button.pack()
save_button.place(x=775, y=175, width=100, height=30)

start_button = tk.Button(Win, text="Start", command=lambda: Start(), bg="white")
Win.bind("<Control-l>", lambda event: Start())       # Shortcut to activate the function
set_font_style(start_button, 12)
start_button.pack()
start_button.place(x=775, y=225, width=100, height=30)

reset_button = tk.Button(Win, text="Reset", command=lambda: Reset(), bg="white")
Win.bind("<Control-r>", lambda event: Reset())       # Shortcut to activate the function
set_font_style(reset_button, 12)
reset_button.pack()
reset_button.place(x=775, y=275, width=100, height=30)

quit_button = tk.Button(Win, text="Quit", command=Quit, bg="white")
Win.bind("<Control-q>", lambda event: Quit())        # Shortcut to activate the function
set_font_style(quit_button, 12)
quit_button.pack()
quit_button.place(x=775, y=500, width=100, height=30)

choice1 = Choice()
value = create_scale(choice1)
selected_option = Speed(Win)

Win.mainloop()
