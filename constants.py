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

WIDTH, HEIGHT = 800, 600
RESOLUTION = (WIDTH, HEIGHT)
FPS = 60
DT = 1 / FPS
GRAVITY = -1000
BACKGROUND_COLOR = "white"
AIR_MASS = 0.5
LEFT = 0
RIGHT = 1

FULL_OPACITY = 100
YELLOW = (255, 255, 0, FULL_OPACITY)
black = (0, 0, 0, FULL_OPACITY)
blue = (0, 0, 255, FULL_OPACITY)
white = (255, 255, 255, FULL_OPACITY)
red = (255, 0, 0, FULL_OPACITY)

PI = pi

TRANSLATE_SPEED = 10
ZOOM_SPEED = 0.1

HELP_TEXT = """Use A,Z to zoom. D,F - control left wing, J,K - control right wing. R for restart. Q for quit"""