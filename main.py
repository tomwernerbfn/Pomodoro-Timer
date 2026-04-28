from tkinter import *
import customtkinter
import datetime
try:
    import winsound #ONLY FOR WINDOWS
except Exception:
    print("sound not possible because of an operating system error!".upper())

customtkinter.set_appearance_mode("dark") #Change to 'light' if you like
customtkinter.set_default_color_theme("blue") #Choose any color you want

root = customtkinter.CTk()

root.title('Pomodoro Timer')
root.geometry('700x400')

yesterday = datetime.timedelta(days=1)
today = datetime.date.today()

running = False
switched = False
menu = False

with open('pomodoros.txt', 'r') as p:
    lines = p.readlines()
    parts = [line.split() for line in lines if line.strip()]
    dates = {datetime.date.fromisoformat(line[0]): line for line in parts}
    #STREAK
    if today in dates:
        pomodoro_val = int(dates[today][1])
    else:
        pomodoro_val = 0

def timer(): #WORKING ON THE GLOBAL MESS
    global num, running, pomodoro_val, today, switched, extent, update
    if running and num != 0:
        label.configure(text=num)
        num -= 1
        canvas.itemconfig(arc, extent=extent) #Making the blue progress bar shrink every second
        extent -= update
        root.after(1000, timer)
    elif running and num == 0:
        running = False
        canvas.itemconfig(arc, extent=extent) #Hiding the blue progress bar
        label.configure(text=num)
        start.configure(text="START")
        winsound.Beep(1000, 300) #ONLY FOR WINDOWS
        winsound.Beep(1000, 300) #ONLY FOR WINDOWS
        with open('pomodoros.txt', 'w') as a:
            pomodoro_val += 1
            a.write(f'{today} {pomodoro_val}')
            pomodoro.configure(text=f"Today's completed Pomodoros: {pomodoro_val} Pomodoros!", font=("Helvetica", 20))
        try:
            with open('options.txt', 'a') as o:
                time = int(entry.get())
        except ValueError:
            entry.configure(placeholder_text='Enter a number!')
            return
        else:
            o.write(f'Date: {today} for {time} seconds!\n')
        label.place_forget()
        entry.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        switched = False

def toggle():
    global running
    if running:
        running = False
        start.configure(text="START")
    else:
        running = True
        entry.place_forget()
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        start.configure(text="PAUSE")
        timer()

def switch():
    global num, switched, extent, update
    if not switched:
        switched = True
        try:
            num = int(entry.get())
        except ValueError:
            entry.configure(placeholder_text='Enter a number!')
            return
        else:
            extent = 359 #customtkinter can't process 360 degrees for some reason
            update = extent / num #The value in degrees of how much the blue progress bar should be shortened
            label.configure(text=num)
    toggle()

def reset():
    global num, running, switched
    running = False
    switched = False
    label.place_forget()
    entry.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
    start.configure(text="START")
    canvas.itemconfig(arc, extent=0)

def option(): #Right now the recent tab isn't a part of the frame. You won't notice while testing, but it's not looking quite well
    global menu, optframe
    if menu:
        menu = False
        optframe.place_forget()
        optbutton.place_forget()
    else:
        menu = True
        optframe.place(relx=0.75, rely=0.58, anchor=customtkinter.CENTER)
        optbutton.place(relx=0.75, rely=0.3, anchor=customtkinter.CENTER)
        
def recent(): #Right now the recent tab isn't a part of the frame. You won't notice while testing, but it's not looking quite well
    global rlines
    with open('options.txt', 'r') as r:
        rlines = str(r.read())
        optlabel.configure(text=rlines, font=("Helvetica", 10))
    if menu:
        optbutton.place_forget()
        optlabel.place(relx=0.75, rely=0.5, anchor=customtkinter.CENTER)

canvas = Canvas(root, width=200, height=200, bg="#252525", highlightthickness=0)
canvas.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

entry = customtkinter.CTkEntry(root, placeholder_text='Enter', font=("Helvetica", 50))
label = customtkinter.CTkLabel(root, text="", font=("Helvetica", 50))
opt = customtkinter.CTkButton(root, text='☰', width=50, height=50, command=option)
start = customtkinter.CTkButton(root, text="START", width=100, height=50, command=switch)
stop = customtkinter.CTkButton(root, text="RESET", width=100, height=50, command=reset)
pomodoro = customtkinter.CTkLabel(root, text=f"Today's completed Pomodoros: {pomodoro_val} Pomodoros!", font=("Helvetica", 20))

optframe = customtkinter.CTkFrame(root, bg_color='#2b2b2b', width=290, height=320)
optbutton = customtkinter.CTkButton(root, text="Recent Pomodoros", width=260, height=50, command=recent)
optlabel = customtkinter.CTkLabel(root, bg_color='#2b2b2b')

# Draw background ring (grey)
canvas.create_oval(10, 10, 190, 190, outline='#3a3a3a', width=12)

# Draw progress arc (blue)
arc = canvas.create_arc(10, 10, 190, 190, start=90, extent=360, outline='#3b8ed0', width=12, style='arc')

opt.place(relx=0.9, rely=0.1, anchor=customtkinter.CENTER)
pomodoro.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
start.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)
stop.place(relx=0.75, rely=0.9, anchor=customtkinter.CENTER)
label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
entry.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

label.place_forget()
optframe.place_forget()

root.mainloop()
