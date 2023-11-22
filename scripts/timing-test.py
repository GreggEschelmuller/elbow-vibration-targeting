from psychopy import core
import numpy as np

test_dict = {"trial_delay": []}
test_dict2 = {"trial_delay": []}

rand_wait = np.random.randint(300, 701)
test_dict["trial_delay"].append(rand_wait / 1000)
test_dict2["trial_delay"].append(rand_wait / 1000)

times = []

timer = core.Clock()
timer.reset()
rand_wait = np.random.randint(300, 701)
test_dict["trial_delay"].append(rand_wait / 1000)
test_dict2["trial_delay"].append(rand_wait / 1000)
print(timer.getTime() * 1000)
