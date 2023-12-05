from daqmx import NIDAQmxInstrument
from psychopy import core, visual
import matplotlib.pyplot as plt
import numpy as np
import nidaqmx
import src.lib as lib

targets = [-900, -600, -300, 0, 300, 600, 900]

fs = 500

win = visual.Window(
    fullscr=True,
    monitor="testMonitor",
    units="pix",
    color="black",
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
    input_task = nidaqmx.Task()
    input_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", min_val=0, max_val=5)
    # input_task.ai_channels.add_ai_voltage_chan("Dev1/ai2", min_val=0, max_val=5)
    input_task.timing.cfg_samp_clk_timing(
    fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS
    )
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