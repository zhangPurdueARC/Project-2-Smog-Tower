import math

# smog calculations

def diameterToRadius(diameter):
    return diameter / 2

def sphereVolume(radius):
    return 4 / 3 * math.pi * (radius ** 3)

# vector fields

def gravityAccel():
    return 9.8

def hydroStaticPressureAccel():
    pass # return to work on

# approximate smog particles as sphere
# 10 micrometers diameter variant

diameter10um = 10 * (10 ** -6)
radius10um = diameterToRadius(diameter10um)
volume10um = sphereVolume(radius10um)

# 2.5 micrometers diameter variant

diameter5HalvesUm = 2.5 * (10 ** -6)
radius5HalvesUm = diameterToRadius(diameter5HalvesUm)
volume5HalvesUm = sphereVolume(radius10um)

