import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import time
import threading
import pygame
from pygame.locals import *
#check this out @enderplayz05
#this is a pull request
#this is a comment by @CIFamisaran

# Alarm sound not yet included 
pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("alarm.wav")

class PomodoroApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Pomodoro Timer")
        self.geometry("400x500")

        self.default_work_time = 25 * 60  # Default: 25 minutes in seconds
        self.default_break_time = 5 * 60  # Default: 5 minutes in seconds
        self.current_time = self.default_work_time
        self.is_work_time = True
        self.timer_running = False
        self.completed_cycles = 0


        # Timer Display
        self.timer_label = tk.Label(self, text=self.format_time(self.current_time), font=("Arial", 48))
        self.timer_label.pack(pady=20)

        # Cycle Counter
        self.cycle_counter_label = tk.Label(self, text=f"Cycles: {self.completed_cycles}")
        self.cycle_counter_label.pack()

        # Start/Stop Button
        self.start_stop_button = tk.Button(self, text="Start", command=self.toggle_timer)
        self.start_stop_button.pack(pady=10)

        # Timer Customization
        self.work_time_input = tk.Entry(self)
        self.work_time_input_label = tk.Label(self, text="WORK IN MINUTES",font=("Arial", 12))
        self.work_time_input.insert(0, "")
        self.work_time_input_label.pack()
        self.work_time_input.pack()

        self.break_time_input = tk.Entry(self)
        self.break_time_input_label = tk.Label(self, text="BREAK IN MINUTES",font=("Arial", 12))
        self.break_time_input.insert(0, "")
        self.break_time_input_label.pack()
        self.break_time_input.pack()

        set_timer_button = tk.Button(self, text="Set Timer", command=self.set_custom_times)
        set_timer_button.pack()

        # Task Input
        self.task_input_label = tk.Label(self, text="ADD A TASK",font=("Arial", 12))
        self.task_input = tk.Entry(self)
        self.task_input.insert(0, "")
        self.task_input_label.pack()
        self.task_input.pack()

        add_task_button = tk.Button(self, text="Add Task", command=self.add_task)
        add_task_button.pack()

        # Task List
        self.task_list = tk.Listbox(self, justify="center",font=("Arial", 20))
        self.task_list.pack(pady=10, fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02}:{int(seconds):02}"

    def toggle_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.start_stop_button.config(text="Start")
        else:
            self.timer_running = True
            self.start_stop_button.config(text="Pause")
            self.run_timer()

    def run_timer(self):
        def update_timer():
            while self.timer_running and self.current_time > 0:
                self.current_time -= 1
                self.timer_label.config(text=self.format_time(self.current_time))
                time.sleep(1)

            if self.current_time <= 0:
                self.show_alarm()

        timer_thread = threading.Thread(target=update_timer)
        timer_thread.start()

    def set_custom_times(self):
        try:
            work_minutes = int(self.work_time_input.get())
            break_minutes = int(self.break_time_input.get())
            if work_minutes > 0:
                self.default_work_time = work_minutes * 60
            if break_minutes > 0:
                self.default_break_time = break_minutes * 60
            self.current_time = self.default_work_time
            self.timer_label.config(text=self.format_time(self.current_time))
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def add_task(self):
        task_text = self.task_input.get()
        if task_text:
            self.task_list.insert(tk.END, task_text)
            self.task_input.delete(0, tk.END)

    def show_alarm(self):
        self.timer_running = False
        self.start_stop_button.config(text="Start")
        pygame.mixer.Sound.play(alarm_sound)

        # Alarm notification
        messagebox.showinfo("Time's Up", "The timer has ended!")

        # Switch between work and break time
        self.is_work_time = not self.is_work_time
        self.current_time = self.default_work_time if self.is_work_time else self.default_break_time
        if self.is_work_time:
            self.completed_cycles += 1
            self.cycle_counter_label.config(text=f"Cycles: {self.completed_cycles}")
        self.timer_label.config(text=self.format_time(self.current_time))
        pygame.mixer.stop()

    def on_closing(self):
        self.timer_running = False
        self.destroy()

if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
