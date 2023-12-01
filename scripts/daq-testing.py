from daqmx import NIDAQmxInstrument
from psychopy import core, visual
import matplotlib.pyplot as plt
import numpy as np
import nidaqmx
import src.lib as lib

# api = 'daqmx'
api = 'nidaq'
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

if api == 'daqmx':
    daq = NIDAQmxInstrument()
    # print(daq)
    daq.ai0.value
    timer = core.Clock()
    collection_timer = core.Clock()
    times =[]
    voltages = []
    collection_timer.reset
    while collection_timer.getTime() < 5:
        timer.reset()
        voltages.append(daq.ai0.value)
        times.append(timer.getTime())


    mean_time = np.mean(times)
    num_samples = len(times)
    std_time = np.std(times)
    print(f"Mean time: {mean_time*1000} ms")
    print(f"Number of samples: {num_samples}")
    print(f"Sampling rate: {num_samples/5} Hz")
    print(f"Standard deviation: {std_time*1000} ms")
    plt.figure()
    plt.hist(times*1000, bins=100)
    # plt.axvline(mean_time*1000, color='k', linestyle='dashed', linewidth=1)
    plt.show()

elif api == 'nidaq':
    input_task = nidaqmx.Task()
    input_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", min_val=0, max_val=5)
    # input_task.ai_channels.add_ai_voltage_chan("Dev1/ai2", min_val=0, max_val=5)
    input_task.timing.cfg_samp_clk_timing(
    fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS
    )
    timer = core.Clock()
    collection_timer = core.Clock()
    times =[]
    voltages = []
    collection_timer.reset
    input_task.start()
    while collection_timer.getTime() < 1:
        timer.reset()
        voltages.append(lib.get_x(input_task)[-1])
        # print(lib.get_x(input_task))
        times.append(timer.getTime())
        win.flip()
    input_task.stop()
    input_task.close()

mean_volts = np.mean(voltages)
print(f"Volts: {mean_volts}")

mean_deg = lib.volt_to_deg(mean_volts)
print(f"Volt to degrees: {mean_deg}")

mean_pix = lib.volt_to_pix(mean_volts)
print(f"Volt to pixels: {mean_pix}")
print("")

mean_cm = lib.pixel_to_cm(mean_pix)
print(f"Pixel to cm: {mean_cm}")

print("")
cm_to_deg = lib.cm_to_deg(mean_cm)
print(f"cm to deg: {cm_to_deg}")

    