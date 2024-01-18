from psychopy import visual, core
import numpy as  np
import src.lib as lib

cursor_size = 0.5
target_size = 1.5
fs = 500
time_limit = 1

win = visual.Window(
    fullscr=True,
    monitor="testMonitor",
    units="pix",
    color="black",
    waitBlanking=False, 
    screen=1,
    size=[1920, 1080],
)

int_cursor = visual.Rect(
    win,
    width=lib.cm_to_pixel(cursor_size),
    height=lib.cm_to_pixel(60),
    fillColor="green",
)
timer = core.Clock()

input_task = lib.configure_input(fs)
input_task.start()
print("starting")
current_pos = [lib.volt_to_pix(lib.get_x(input_task)[-1]), 0]
volts = []
while timer.getTime() < time_limit:
    volts.append(lib.get_x(input_task)[-1])



print(f"mean volts =  {np.mean(volts)}")
input_task.stop()
input_task.close()