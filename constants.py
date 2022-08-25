#
# Copyright (c) 2022 Apple Inc. All rights reserved.
#
# This document is the property of Apple Inc.
# It is considered confidential and proprietary.
#
# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of
# Apple Inc.
#
from math import pi
import numpy as np

WIDTH, HEIGHT = 800, 600
RESOLUTION = (WIDTH, HEIGHT)
FPS = 60
DT = 1 / FPS
GRAVITY = -1000
BACKGROUND_COLOR = "white"
AIR_MASS = 0.5
LEFT = 0
RIGHT = 1

TRAIN_TIME_SEC = 20  # seconds
TRAIN_TIME_DT = (TRAIN_TIME_SEC / DT)
POLICY_LEN = TRAIN_TIME_DT * 2

ANGULAR_VELOCITY_DECAY = 0.65
DRAG_COEFFICIENT = 0.0001

FULL_OPACITY = 100
YELLOW = (255, 255, 0, FULL_OPACITY)
BLACK = (0, 0, 0, FULL_OPACITY)
BLUE = (0, 0, 255, FULL_OPACITY)
WHITE = (255, 255, 255, FULL_OPACITY)
RED = (255, 0, 0, FULL_OPACITY)
GREEN = (0, 255, 0, FULL_OPACITY)
BROWN = (139, 69, 19, FULL_OPACITY)
PI = pi

TRANSLATE_SPEED = 10
ZOOM_SPEED = 0.1

HELP_TEXT = """Use A,Z to zoom. D,F - control left wing, J,K - control right wing. R for restart. Q for quit"""

phase_len = 50
n_phases = int(POLICY_LEN / (phase_len * 2))
example_policy = np.tile(np.dstack((np.repeat(1, phase_len), np.repeat(-1, phase_len))).reshape((-1,), order='F'), n_phases)
