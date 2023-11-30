"""
This file contains a series of functions used for a wrist-based cursor control experiment.
The experiment is coded in psychopy. The functions and code were written by Gregg Eschelmuller.
"""

import numpy as np
import pandas as pd
import nidaqmx
from daqmx import NIDAQmxInstrument

# 24 inch diag - resololution 1920x1080
# 0.596736 m arc length
# 1 m radius
# total degrees 34.19


def configure_input(fs):
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", min_val=0, max_val=5)
    task.timing.cfg_samp_clk_timing(
        fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS
    )
    return task


def configure_output():
    task = nidaqmx.Task()
    task.do_channels.add_do_chan("Dev1/port0/line0")
    task.do_channels.add_do_chan("Dev1/port0/line1")
    return task


def generate_trial_dict():
    template = {
        "trial_num": [],
        "move_times": [],
        "elbow_end": [],
        "curs_end": [],
        "error": [],
        "block": [],
        "trial_delay": [],
        "target": [],
    }
    return template


def generate_position_dict():
    template = {
        "elbow_pos": [],
        "pot_volts": [],
        "time": [],
    }
    return template


def cm_to_pixel(cm):
    return int((cm /2.54) * 81.59)


def pixel_to_cm(pix):
    return (pix / 81.59) * 2.54


def read_trial_data(file_name, sheet=0):
    # Reads in the trial data from the excel file
    return pd.read_excel(file_name, sheet_name=sheet, engine="openpyxl")


def make_rot_mat(theta):
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def exp_filt(pos0, pos1, alpha=0.5):
    x = (pos0 * alpha) + (pos1 * (1 - alpha))
    return x


# For daqmx
# def get_x(daq):
#     x = daq.ai0.value
#     print(x)
#     x *= -1997.4
#     x += 4733.8
#     return [x, 0]


def get_x(task):
    while True:
        data = task.read(
            number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE
        )
        if len(data) == 0:
            continue
        else:
            # print(data)
            return data


def volt_to_pix(data):
    # Calibration done on November 29, 2023
    data *= -2258.9
    data += 9076.7
    return data


# def get_x(task):
#     while True:
#         vals = task.read(
#             number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE
#         )
#         # print(vals)
#         if len(vals) == 0:
#             continue
#         else:
#             x_data = vals
#             # print(len(vals))
#             # y_data = vals[1]

#             # If buffer contains multiple data points take the lastest one
#             # if len(x_data) > 1:
#             #     x_data = [x_data[-1]]
#             # if len(y_data) > 1:
#             #     y_data = [y_data[-1]]

#             # # I don't remember why this check is here, but it doesn't work without it
#             # if not len(vals[0]) == 0:
#                 # Offset cursor to middle position
#                 # x = 5 - (x_data[0] + 2.7)
#             x = x_data[-1]
#             # print(f"Volatage is {x}")
#             # y = y_data[0] - 2.3

#             # Cursor calibration - October 18, 2023
#             x *= -1997.4
#             x += 4733.8

#             # y *= 1
#             return [x, 0]


def contains(small_circ, large_circ):
    d = np.sqrt(
        (small_circ.pos[0] - large_circ.pos[0]) ** 2
        + (small_circ.pos[1] - large_circ.pos[1]) ** 2
    )
    return (d + small_circ.radius) < large_circ.radius


def set_position(pos, circ):
    circ.pos = pos
    circ.draw()


def calc_target_pos(angle, amp=8):
    # Calculates the target position based on the angle and amplitude
    magnitude = cm_to_pixel(amp)
    x = np.cos(angle * (np.pi / 180)) * magnitude
    y = np.sin(angle * (np.pi / 180)) * magnitude
    return x, y


def calc_amplitude(pos):
    # Calculates the amplitude of the cursor relative to middle
    amp = np.sqrt(np.dot(pos, pos))
    return amp


def save_end_point(data_dict, current_time, current_pos, int_cursor, condition, t_num):
    data_dict["move_times"].append(current_time)
    data_dict["elbow_end"].append(current_pos[0])
    data_dict["curs_end"].append(int_cursor.pos[0])
    data_dict["target_pos"].append(condition.target_pos[t_num])
    data_dict["rotation"].append(condition.rotation[t_num])
    data_dict["vibration"].append(condition.vibration[t_num])
    return data_dict


def save_position_data(data_dict, int_cursor, current_pos, current_time):
    data_dict["curs_pos"].append(int_cursor.pos[0])
    data_dict["elbow_pos"].append(current_pos[0])
    data_dict["time"].append(current_time)
    if len(data_dict["elbow_pos"]) > 1:
        data_dict["velocity"].append(
            (
                round(data_dict["elbow_pos"][-1], 2)
                - round(data_dict["elbow_pos"][-2], 2)
            )
            / (1 / 500)
        )
    else:
        data_dict["velocity"].append(0)
    return data_dict
