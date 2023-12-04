from psychopy import visual, core
import src.lib as lib

cursor_size = 0.5
target_size = 1.5
fs = 500
time_limit = 30

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
    fillColor="Black",
)
timer = core.Clock()

input_task = lib.configure_input(fs)
input_task.start()

while timer < time_limit:
    print("calibration started")
    pot_data = lib.get_x(input_task)
    current_deg = lib.volt_to_deg(pot_data[-1])
    new_pos = lib.volt_to_pix(pot_data[-1])
    current_pos = [lib.exp_filt(current_pos[0], new_pos), 0]
    lib.set_position(current_pos, int_cursor)


print("calibration ended")
input_task.stop()
