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
        "elbow_end_volts": [],
        "elbow_end_pix": [],
        "elbow_end_cm": [],
        "elbow_end_deg": [],
        "cursor_end_pix": [],
        "curs_end_cm": [],
        "curs_end_deg": [],
        "error": [],
        "block": [],
        "trial_delay": [],
        "target_cm": [],
        "target_deg": [],
        "target_pix": [],
        "rt": [],
    }
    return template


def generate_position_dict():
    template = {
        "elbow_pos_pix": [],
        "elbow_pos_deg": [],
        "pot_volts": [],
        "time": [],
    }
    return template


def cm_to_pixel(cm):
    return (cm /2.54) * 81.59


def pixel_to_cm(pix):
    return (pix / 81.59) * 2.54


def pixel_to_volt(data):
    data -= 9076.7
    data /= -2258.9
    return data

def volt_to_pix(data):
    # Calibration done on November 29, 2023
    data *= -2173.1
    data += 8515.8
    return data


def volt_to_deg(volt):
    return -62.692*volt + 363.76


def cm_to_deg(data):
    data = cm_to_pixel(data)
    data = pixel_to_volt(data)
    data = volt_to_deg(data)
    # return volt_to_deg(pixel_to_volt(cm_to_pixel(data)))
    return data

def pixel_to_deg(data):
    data = pixel_to_volt(data)
    data = volt_to_deg(data)
    return data

def read_trial_data(file_name, sheet=0):
    # Reads in the trial data from the excel file
    return pd.read_excel(file_name, sheet_name=sheet, engine="openpyxl")


def make_rot_mat(theta):
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def exp_filt(pos0, pos1, alpha=0.5):
    x = (pos0 * alpha) + (pos1 * (1 - alpha))
    return x


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