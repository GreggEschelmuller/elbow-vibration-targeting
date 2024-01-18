import src.lib as lib
from psychopy import core

output_task = lib.configure_output()
condition = 2

output_task.start()
# Set up vibration output
if condition == 0:
    vib_output = [False, False]
elif condition == 1:
    vib_output = [True, True]
elif condition == 2:
    vib_output = [True, False]  # Triceps
elif condition == 3:
    vib_output = [False, True]  # Biceps

timer = core.Clock()

output_task.write(vib_output)
print(f"outputed {vib_output}")
timer.reset()

while timer.getTime() < 1:
    continue

output_task.write([False, False])
output_task.stop()
output_task.close()
