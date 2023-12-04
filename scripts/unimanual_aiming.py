# Imports
from psychopy import visual, core
import numpy as np
import pandas as pd
import src.lib as lib
from datetime import datetime
import copy
import os
import nidaqmx
import matplotlib.pyplot as plt

# from daqmx import NIDAQmxInstrument

# ------------------Blocks to run ------------------
# Use this to run whole protocol
# make sure the strings match the names of the sheets in the excel

# For testing a few trials
ExpBlocks = ["practice"]
ExpBlocks = ["baseline", "main", "post"]

# ----------- Participant info ----------------

# For clamp and rotation direction
rot_direction = 1  # 1 for forwrad, -1 for backward
participant = 1


study_id = "Wrist Visuomotor Rotation"
experimenter = "Gregg"
current_date = datetime.now()
date_time_str = current_date.strftime("%Y-%m-%d %H:%M:%S")


study_info = {
    "Participant ID": participant,
    "Date_Time": date_time_str,
    "Study ID": study_id,
    "Experimenter": experimenter,
}
# experiment_info = pd.DataFrame.from_dict(study_info)

if not participant == 99:
    print(study_info)
    input(
        """
        Make sure changed the participant info is correct before continuing.
        Press enter to continue.
        """
    )

# # Check if directory exists and if it is empty
dir_path = f"data/p{str(participant)}"

if ExpBlocks[0] == "practice":
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(
            """
        Directory didn't exist so one was created. Continuing with program.
        """
        )
    elif len(os.listdir(dir_path)) == 0:
        print(
            """
        Directory already exists and is empty. Continuing with program."""
        )
    elif os.path.exists(dir_path) and not len(dir_path) == 0:
        print(
            """
        This directory exists and isn't empty, exiting program.
        Please check the contents of the directory before continuing.
        """
        )
        exit()

# set up file path
file_path = f"data/p{str(participant)}/p{str(participant)}"
# pd.DataFrame.from_dict(study_info).to_csv(f"{file_path}_study_information.csv")
print("Setting everything up...")

# ------------------------ Set up --------------------------------

# Variables set up
cursor_size = 0.5
target_size = 1.5
home_range_upper = lib.volt_to_pix(4.75)
home_range_lower = lib.volt_to_pix(4.99)
fs = 500
timeLimit = 2
# Home position in volts = 4.9

## Psychopy set up
# Create window
win = visual.Window(
    fullscr=True,
    monitor="testMonitor",
    units="pix",
    color="black",
    waitBlanking=False,
    screen=1,
    size=[1920, 1080],
)


# set up clocks
move_clock = core.Clock()
home_clock = core.Clock()
trial_delay_clock = core.Clock()
rt_clock = core.Clock()

home_indicator = visual.Circle(
    win, radius=lib.cm_to_pixel(1), fillColor="red", pos=[0, 100]
)


int_cursor = visual.Rect(
    win,
    width=lib.cm_to_pixel(cursor_size),
    height=lib.cm_to_pixel(60),
    fillColor="Black",
)

target = visual.Rect(
    win,
    width=lib.cm_to_pixel(target_size),
    height=lib.cm_to_pixel(60),
    lineColor="red",
    fillColor=None,
)


print("Done set up")
# -------------- start main experiment loop ------------------------------------
input("Press enter to continue to first block ... ")
for block in range(len(ExpBlocks)):
    condition = lib.read_trial_data("Trials.xlsx", ExpBlocks[block])
    file_ext = ExpBlocks[block]

    # Summary data dictionaries for this block
    block_data = lib.generate_trial_dict()

    for i in range(len(condition.trial_num)):
        # Creates dictionary for single trial
        current_trial = lib.generate_trial_dict()
        position_data = lib.generate_position_dict()

        # Set up vibration output
        if condition.vibration[i] == 0:
            vib_output = [False, False]
        elif condition.vibration[i] == 1:
            vib_output = [True, True]
        elif condition.vibration[i] == 2:
            vib_output = [True, False]  # BICEPS
        elif condition.vibration[i] == 3:
            vib_output = [False, True]  # TRICEPS

        int_cursor.color = None
        int_cursor.draw()
        win.flip()

        # Sets up target position
        target_jitter = np.random.uniform(-0.5, 0.5)  # jitter target position
        target_amplitude = condition.target_amp[i] + target_jitter
        current_target_pos = lib.calc_target_pos(0, target_amplitude)

        # Run trial

        # configure input/output
        input_task = lib.configure_input(fs)
        output_task = lib.configure_output()

        # start daq tasks for input/output
        input_task.start()
        output_task.start()
        # input(f"Press enter to start trial # {i+1} ... ")

        in_home_timer = core.Clock()
        current_pos = [lib.volt_to_pix(lib.get_x(input_task)[-1]), 0]
        print("waiting for home position")
        while True:
            home_indicator.color = "red"
            home_indicator.draw()
            win.flip()
            pot_data = lib.get_x(input_task)
            new_pos = lib.volt_to_pix(pot_data[-1])
            current_pos = [lib.exp_filt(current_pos[0], new_pos), 0]
            if current_pos[0] > home_range_lower and current_pos[0] < home_range_upper:
                in_home_timer.reset()
                home_indicator.color = "green"
                home_indicator.draw()
                win.flip()
                print("cursor in home position")
                break

        # randomly delay trial start
        rand_wait = np.random.randint(2000, 3000)
        current_trial["trial_delay"].append(rand_wait / 1000)
        block_data["trial_delay"].append(rand_wait / 1000)
        trial_delay_clock.reset()
        print(f"rand delay is {rand_wait / 1000} seconds")
        while trial_delay_clock.getTime() < (rand_wait / 1000):
            continue

        if not condition.full_feedback[i]:
            int_cursor.color = "None"

        # Start vibration
        output_task.write(vib_output)

        # Display target position
        home_indicator.color = "black"
        lib.set_position(current_target_pos, target)
        win.flip()

        rt_clock.reset()
        current_pos = [lib.volt_to_pix(lib.get_x(input_task)[-1]), 0]
        while True:
            pot_data = lib.get_x(input_task)
            new_pos = lib.volt_to_pix(pot_data[-1])
            current_pos = [lib.exp_filt(current_pos[0], new_pos), 0]
            if current_pos[0] > home_range_upper:
                break
        rt = rt_clock.getTime()

        print("Cursor left home, trial started")
        # run trial until time limit is reached or target is reached
        move_clock.reset()
        current_pos = [lib.volt_to_pix(lib.get_x(input_task)[-1]), 0]
        velocities = []
        while move_clock.getTime() < timeLimit:
            previous_position = current_pos

            # Run trial
            current_time = move_clock.getTime()
            pot_data = lib.get_x(input_task)
            current_deg = lib.volt_to_deg(pot_data[-1])
            new_pos = lib.volt_to_pix(pot_data[-1])
            current_pos = [lib.exp_filt(current_pos[0], new_pos), 0]
            target.draw()
            lib.set_position(current_pos, int_cursor)
            win.flip()
            current_vel = current_pos[0] - previous_position[0]
            velocities.append(current_vel)

            # Save position data
            position_data["elbow_pos_pix"].append(current_pos[0])
            position_data["pot_volts"].append(pot_data[-1])
            position_data["time"].append(current_time)
            position_data["elbow_pos_deg"].append(current_deg)

            if np.mean(velocities[-20:]) < 0.05 and current_time > 0.5:
                break

        # if current_vel <= 20:
        output_task.write([False, False])
        # Append trial data to storage variables
        if condition.terminal_feedback[i]:
            int_cursor.color = "Green"
            int_cursor.draw()
            target.draw()
            win.flip()

        # Leave current window for 200ms
        input_task.stop()
        output_task.stop()
        core.wait(0.2, hogCPUperiod=0.2)
        int_cursor.color = None
        int_cursor.draw()
        win.flip()
        input_task.close()

        # Print trial information
        print(f"Trial {i+1} done.")
        print(f"Movement time: {round((current_time*1000),1)} ms")
        print(
            f"Target position: {round(lib.cm_to_deg(condition.target_amp[i]), 3)} deg    Cursor Position: {round(current_deg,3)} deg"
        )
        print(
            f"Error: {round(current_deg - lib.cm_to_deg(condition.target_amp[i]), 3)} deg"
        )
        print(" ")

        # Write and save data for individual trial
        current_trial["move_times"].append(current_time)
        current_trial["elbow_end_cm"].append(lib.pixel_to_cm(current_pos[0]))
        current_trial["elbow_end_deg"].append(current_deg)
        current_trial["curs_end_cm"].append(lib.pixel_to_cm(int_cursor.pos[0]))
        current_trial["curs_end_deg"].append(lib.pixel_to_deg(int_cursor.pos[0]))
        current_trial["error"].append(
            current_deg - lib.cm_to_deg(condition.target_amp[i])
        )
        current_trial["trial_num"].append(i + 1)
        current_trial["block"].append(ExpBlocks[block])
        current_trial["target_cm"].append(target_amplitude)
        current_trial["target_deg"].append(lib.cm_to_deg(target_amplitude))
        current_trial["rt"].append(rt)
        # Save data to CSV
        pd.DataFrame.from_dict(current_trial).to_csv(
            f"{file_path}_trial_{str(i+1)}_{file_ext}.csv", index=False
        )
        pd.DataFrame.from_dict(position_data).to_csv(
            f"{file_path}_position_{str(i+1)}_{file_ext}.csv", index=False
        )

        # Append data for whole block
        block_data["move_times"].append(current_time)
        block_data["elbow_end_cm"].append(lib.pixel_to_cm(current_pos[0]))
        block_data["elbow_end_deg"].append(current_deg)
        block_data["curs_end_cm"].append(lib.pixel_to_cm(int_cursor.pos[0]))
        block_data["curs_end_deg"].append(lib.pixel_to_deg(int_cursor.pos[0]))
        block_data["error"].append(current_deg - lib.cm_to_deg(condition.target_amp[i]))
        block_data["trial_num"].append(i + 1)
        block_data["block"].append(ExpBlocks[block])
        block_data["target_cm"].append(target_amplitude)
        block_data["target_deg"].append(lib.cm_to_deg(target_amplitude))
        block_data["rt"].append(rt)

        del current_trial, position_data

        if (i + 1) % 40 == 0:
            input("Break before veridical trials - press enter to continue")

    # End of bock saving
    print("Saving Data")
    trial_data = pd.merge(
        pd.DataFrame.from_dict(block_data),
        pd.DataFrame.from_dict(condition),
        on="trial_num",
    )

    trial_data.to_csv(file_path + "_" + file_ext + ".csv", index=False)

    print("Data Succesfully Saved")

    del condition, trial_data, block_data
    # input_task.stop()
    # output_task.stop()
    input("Press enter to continue to next block ... ")

input_task.close()
output_task.close()
print("Experiment Done")
