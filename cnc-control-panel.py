import Tkinter as tk
import pygubu
import ttk
import datetime

class Application:
    ON_STYLE = "on.TButton"
    OFF_STYLE = "off.TButton"

    def __init__(self, master):
        ttk.Style().theme_use("alt")
        ttk.Style().configure("TButton", font=("Helvetica", 14, "bold"))

        ttk.Style().configure(Application.ON_STYLE, relief=tk.SUNKEN, background="green2", foreground="black")
        ttk.Style().map(Application.ON_STYLE, relief=[("active", tk.SUNKEN)], background=[("active", "green3")])
        ttk.Style().configure(Application.OFF_STYLE, relief=tk.RAISED, background="red2", foreground="black")
        ttk.Style().map(Application.OFF_STYLE, relief=[("active", tk.RAISED)], background=[("active", "red3")])

        self.builder = builder = pygubu.Builder()
        builder.add_from_file("cnc-control-panel.ui")
        self.mainwindow = builder.get_object("Main_Frame", master)

        builder.connect_callbacks(self)

        self.stepper = builder.get_object("Button_Stepper")
        self.water = builder.get_object("Button_Water")
        self.vacuum = builder.get_object("Button_Vacuum")
        self.outlet = builder.get_object("Button_Outlet")
        self.status = builder.get_object("Text_Status")
        self.status_log("Started")

    def button_clicked(self, button, gpio_pin):
        self.status_log("Toggle GPIO %d" % gpio_pin)
        if button.cget("style") == Application.ON_STYLE:
            button.configure(style = Application.OFF_STYLE)
        else:
            button.configure(style = Application.ON_STYLE)

    def on_stepper_clicked(self):
        self.button_clicked(self.stepper, 1)

    def on_water_clicked(self):
        self.button_clicked(self.water, 2)

    def on_vacuum_clicked(self):
        self.button_clicked(self.vacuum, 3)

    def on_outlet_clicked(self):
        self.button_clicked(self.outlet, 4)

    def status_log(self, text):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.status['state'] = 'normal'
        self.status.insert('1.0',  timestamp + ": " + text + "\n")
        self.status['state'] = 'disabled'

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CNC Control")
    app = Application(root)
    root.mainloop()