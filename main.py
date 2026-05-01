from tkinter import *
import customtkinter
import datetime
import random

try:
    import winsound  # ONLY FOR WINDOWS
except ImportError:
    winsound = None
    print("SOUND NOT POSSIBLE BECAUSE OF AN OPERATING SYSTEM ERROR!")


QUOTES = {
    'Franklin D. Roosevelt': "'The only thing we have to fear is fear itself.'",
    'Mahatma Gandhi': "'Be the change that you wish to see in the world.'",
    'Martin Luther King Jr.': "'In the end, we will remember not the words of our enemies, but the silence of our friends.'",
    'Ralph Waldo Emerson': "'To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.'",
    'James Baldwin': "'Not everything that is faced can be changed, but nothing can be changed until it's faced.'",
    'Albert Einstein': "'Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.'",
    'Mother Teresa': "'If you judge people, you have no time to love them.'",
    'Steve Jobs': "'The only way to do great work is to love what you do.'",
    'Confucius': "'It does not matter how slowly you go as long as you do not stop.'",
    'Zig Ziglar': "'What you get by achieving your goals is not as important as what you become by achieving your goals.'",
    'Abraham Lincoln': "'Nearly all men can stand adversity, but if you want to test a man's character, give him power.'",
    'John C. Maxwell': "'A leader is one who knows the way, goes the way, and shows the way.'",
    'Eleanor Roosevelt': "'Do what you feel in your heart to be right - for you'll be criticized anyway.'",
    'Ralph Nader': "'The function of leadership is to produce more leaders, not more followers.'",
    'Peter Ducker': "'Management is doing things right; leadership is doing the right things.'",
    'John F. Kennedy': "'Leadership and learning are indispensable to each other.'",
    'Martin Luther King Jr.': "'A genuine leader is not a searcher for consensus but a molder of consensus.'",
    'Ronald Reagan': "'The greatest leader is not necessarily the one who does the greatest things; he is the one that gets the people to do the greatest things.'",
    'Albert Schweitzer': "'Example is not the main thing in influencing others. It is the only thing.'",
}


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Pomodoro Timer')
        self.root.geometry('700x400')

        self.running = False
        self.switched = False
        self.menu = False
        self.num = 0
        self.extent = 0
        self.update_step = 0
        self.today = datetime.date.today()
        self.canvas_bg = "#252525"
        self.opt_bg = "#2b2b2b"

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        key, value = random.choice(list(QUOTES.items()))
        self.quo = f"{value}     - {key}"

        self.pomodoro_val = self._load_pomodoro_count()

        self._setup_canvas()
        self._setup_widgets()
        self._place_widgets()

    def _load_pomodoro_count(self):
        try:
            with open('pomodoros.txt', 'r') as f:
                lines = f.readlines()
            parts = [line.split() for line in lines if line.strip()]
            dates = {datetime.date.fromisoformat(line[0]): line for line in parts}
            if self.today in dates:
                return int(dates[self.today][1])
        except FileNotFoundError:
            pass
        return 0

    def _save_pomodoro_count(self):
        with open('pomodoros.txt', 'w') as f:
            f.write(f'{self.today} {self.pomodoro_val}')

    def _save_session_to_options(self, duration):
        with open('options.txt', 'a') as f:
            f.write(f'Date: {self.today} for {duration} seconds!\n')

    def _load_recent_sessions(self):
        try:
            with open('options.txt', 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "No sessions recorded yet."

    def timer(self):
        if self.running and self.num != 0:
            self.label.configure(text=self.num)
            self.num -= 1
            self.canvas.itemconfig(self.arc, extent=self.extent)
            self.extent -= self.update_step
            self.root.after(1000, self.timer)
        elif self.running and self.num == 0:
            self._on_timer_complete()

    def _on_timer_complete(self):
        self.running = False
        self.canvas.itemconfig(self.arc, extent=0)
        self.label.configure(text=0)
        self.start.configure(text="START")

        if winsound:
            winsound.Beep(1000, 300)
            winsound.Beep(1000, 300)

        self.pomodoro_val += 1
        self._save_pomodoro_count()
        self.pomodoro.configure(
            text=f"Today's completed Pomodoros: {self.pomodoro_val} Pomodoros!",
            font=("Helvetica", 20)
        )

        try:
            duration = int(self.entry.get())
            self._save_session_to_options(duration)
        except ValueError:
            self.entry.configure(placeholder_text='Enter a number!')
            return

        self.label.place_forget()
        self.entry.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.switched = False

    def toggle(self):
        if self.running:
            self.running = False
            self.start.configure(text="START")
        else:
            self.running = True
            self.entry.place_forget()
            self.label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
            self.start.configure(text="PAUSE")
            self.timer()

    def switch(self):
        if not self.switched:
            self.switched = True
            try:
                self.num = int(self.entry.get())
            except ValueError:
                self.entry.configure(placeholder_text='Enter a number!')
                return
            self.extent = 359  # CustomTkinter can't process 360 degrees
            self.update_step = self.extent / self.num
            self.label.configure(text=self.num)
        self.toggle()

    def reset(self):
        self.running = False
        self.switched = False
        self.label.place_forget()
        self.entry.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.start.configure(text="START")
        self.canvas.itemconfig(self.arc, extent=0)

    def option(self):
        if self.menu:
            self.menu = False
            self.optframe.place_forget()
            self.optbutton.place_forget()
            self.optpref.place_forget()
            self.optboxd.place_forget()
            self.optboxl.place_forget()
        else:
            self.menu = True
            self.optframe.place(relx=0.75, rely=0.58, anchor=customtkinter.CENTER)
            self.optbutton.place(relx=0.75, rely=0.3, anchor=customtkinter.CENTER)
            self.optpref.place(relx=0.75, rely=0.5, anchor=customtkinter.CENTER)

    def recent(self):
        sessions = self._load_recent_sessions()
        self.optlabel.configure(text=sessions, font=("Helvetica", 10))
        if self.menu:
            self.optbutton.place_forget()
            self.optlabel.place(relx=0.75, rely=0.5, anchor=customtkinter.CENTER)

    def preferences(self):
        if self.menu:
            self.optpref.place_forget()
            self.optbutton.place_forget()
            self.optboxl.place(relx=0.75, rely=0.3, anchor=customtkinter.CENTER)
            self.optboxd.place(relx=0.75, rely=0.4, anchor=customtkinter.CENTER)
        else:
            self.optboxd.place_forget()
            self.optboxl.place_forget()

    def dark(self):
        if self.optboxl.get() == 1:
            self.optboxl.deselect()
            customtkinter.set_appearance_mode("dark")
            self.canvas_bg = "#252525"
            self.opt_bg = "#2b2b2b"
            self._apply_theme()
        elif self.optboxd.get() == 0:
            self.optboxd.select()

    def light(self):
        if self.optboxd.get() == 1:
            self.optboxd.deselect()
            customtkinter.set_appearance_mode("light")
            self.canvas_bg = "#ECECEC"
            self.opt_bg = "#DBDBDB"
            self._apply_theme()
        elif self.optboxl.get() == 0:
            self.optboxl.select()

    def _apply_theme(self):
        self.canvas.configure(background=self.canvas_bg)
        self.optboxd.configure(bg_color=self.opt_bg)
        self.optboxl.configure(bg_color=self.opt_bg)

    def _setup_canvas(self):
        self.canvas = Canvas(
            self.root, width=200, height=200,
            bg=self.canvas_bg, highlightthickness=0
        )
        self.canvas.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        self.canvas.create_oval(10, 10, 190, 190, outline='#3a3a3a', width=12)

        self.arc = self.canvas.create_arc(
            10, 10, 190, 190,
            start=90, extent=360,
            outline='#3b8ed0', width=12, style='arc'
        )

    def _setup_widgets(self):
        self.entry = customtkinter.CTkEntry(
            self.root, placeholder_text='Enter', font=("Helvetica", 50)
        )
        self.label = customtkinter.CTkLabel(
            self.root, text="", font=("Helvetica", 50)
        )
        self.opt = customtkinter.CTkButton(
            self.root, text='☰', width=50, height=50, command=self.option
        )
        self.start = customtkinter.CTkButton(
            self.root, text="START", width=100, height=50, command=self.switch
        )
        self.stop = customtkinter.CTkButton(
            self.root, text="RESET", width=100, height=50, command=self.reset
        )
        self.pomodoro = customtkinter.CTkLabel(
            self.root,
            text=f"Today's completed Pomodoros: {self.pomodoro_val} Pomodoros!",
            font=("Helvetica", 20)
        )
        self.quote = customtkinter.CTkLabel(self.root, text=self.quo)

        self.optframe = customtkinter.CTkFrame(
            self.root, bg_color='#2b2b2b', width=290, height=320
        )
        self.optbutton = customtkinter.CTkButton(
            self.root, text="Recent Pomodoros", width=260, height=50, command=self.recent
        )
        self.optpref = customtkinter.CTkButton(
            self.root, text='Preferences', width=260, height=50, command=self.preferences
        )
        self.optlabel = customtkinter.CTkLabel(self.root, bg_color='#2b2b2b')
        self.optboxl = customtkinter.CTkCheckBox(
            self.root, text='Light mode', bg_color=self.opt_bg, command=self.light
        )
        self.optboxd = customtkinter.CTkCheckBox(
            self.root, text='Dark mode', bg_color=self.opt_bg, command=self.dark
        )

    def _place_widgets(self):
        self.opt.place(relx=0.9, rely=0.1, anchor=customtkinter.CENTER)
        self.pomodoro.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
        self.start.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)
        self.stop.place(relx=0.75, rely=0.9, anchor=customtkinter.CENTER)
        self.label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.entry.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.quote.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

        self.label.place_forget()
        self.optframe.place_forget()

        # Default to dark mode
        self.optboxd.select()


if __name__ == "__main__":
    root = customtkinter.CTk()
    app = PomodoroApp(root)
    root.mainloop()
