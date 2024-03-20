import math

# smog calculations
# approximate smog particles as sphere

class Particle: 
    diameter = 0
    radius = 0
    volume = 0
    velocity = [0, 0, 0]
    position = [0, 0, 0]
    crossSectionalArea = 0
    density = 1950
    mass = 0

    def __init__(self, diameter):
        self.diameter = diameter
        self.radius = diameter / 2
        self.volume = 4 / 3 * math.pi * (self.radius ** 3)
        self.crossSectionalArea = math.pi * (self.radius ** 2)
        self.mass = self.volume * self.density

# vector fields

def gravityAccel():
    return [0, 0, -9.81]

def hydroStaticPressureAccel(particle): # needs mass
    atmoPressure = 1.013 * (10 ** 5) - 1.28 * 9.81 * particle.position[2] 
    return [0, 0, -1 * atmoPressure * particle.crossSectionalArea / particle.mass]

def buoyantAccel(particle):
    return [0, 0, 1.28 * 9.81 * particle.volume / particle.mass]

# 10 micrometers diameter variant
particle10um = Particle(10 * (10 ** -6))
# 2.5 micrometers diameter variant
particle5HalvesUm = Particle(2.5 * (10 ** -6))

