from daqmx import NIDAQmxInstrument
from psychopy import core, visual
import matplotlib.pyplot as plt
import numpy as np
import nidaqmx
import src.lib as lib

targets = [-900, -400, 0, 400, 900]
# targets = [900]

fs = 500

win = visual.Window(
    fullscr=True,
    monitor="testMonitor",
    units="pix",
    color="Black",
    waitBlanking=False,
    screen=1,
    size=[1920, 1080],
)

target = visual.Rect(
    win,
    width=lib.cm_to_pixel(1.5),
    height=lib.cm_to_pixel(100),
    lineColor="red",
    fillColor=None,
)


pot_voltages = []
for t in targets:
    target.pos = [t]
    target.draw()
    win.flip()
    input("Press enter when the manipulandum is aligned")
    input_task = lib.configure_input(fs)
    collection_timer = core.Clock()
    voltages = []
    input_task.start()
    collection_timer.reset()
    while collection_timer.getTime() < 1:
        voltages.append(lib.get_x(input_task)[-1])
        target.draw()
        win.flip()
    input_task.stop()
    input_task.close()
    pot_voltages.append(np.mean(voltages))

print(pot_voltages)