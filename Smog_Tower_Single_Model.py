import math
import random
# smog calculations
# approximate smog particles as sphere

class Particle: # 1 centimeter cube with particle info
    diameter = 0
    radius = 0
    volume = 0
    velocity = [0, 0, 0]
    position = [0, 0, 0]
    crossSectionalArea = 0
    particleDensity = 1950
    mass = 0
    charge = -1.602 * (10 ** -19)
    numParticles = 0

    def __init__(self, diameter, massDensity, position):
        self.diameter = diameter
        self.radius = diameter / 2
        self.volume = 4 / 3 * math.pi * (self.radius ** 3)
        self.crossSectionalArea = math.pi * (self.radius ** 2)
        self.mass = self.volume * self.particleDensity
        self.numParticles = massDensity / self.mass
        self.position = position

    def electricField(self, particle): # approx as point
        r = math.sqrt(particle.position[0] ** 2 + particle.position[1] ** 2 + particle.position[2] ** 2)
        unitVec = particle.position / r
        eMag = 8.98 * 10 ** 9 * self.numParticles * self.charge / (r ** 2)
        return eMag * unitVec

class Tower: # approximate the tower as a line charge
    chargeDensity = 0
    totalCharge = 0
    height = 0
    captureParticles = 0
    
    def __init__(self, chargeDensity, height):
        self.chargeDensity = chargeDensity
        self.height = height
        self.totalCharge = chargeDensity * height

    def electricField(self, particle):
        z = math.sqrt(particle.position[0] ** 2 + particle.position[1] ** 2)
        unitVec = (particle.position) / z
        eMag = 8.98 * 10 ** 9 * self.chargeDensity * particle.position / z * (particle.position[2]/math.sqrt(z ** 2 + particle.position[2] ** 2) + (self.height - particle.position[2])/math.sqrt(z ** 2 + (self.height - particle.position[2] ** 2)))
        return eMag * unitVec
    
    def changeCharge(self, particle):
        self.totalCharge += particle.charge * particle.numParticles * 2 * math.pi
        self.chargeDensity = self.totalCharge / self.height

# vector fields
def gravityAccel():
    return [0, 0, -9.81]

def hydroStaticPressureAccel(particle): # needs mass
    atmoPressure = 1.013 * (10 ** 5) - 1.28 * 9.81 * particle.position[2] 
    return [0, 0, -1 * atmoPressure * particle.crossSectionalArea / particle.mass]

def buoyantAccel(particle):
    return [0, 0, 1.28 * 9.81 * particle.volume / particle.mass]

def dragAccel(particle, windVelocity):
    return -6 * math.pi * (1.895 * (10 ** -5)) * particle.diameter * (particle.velocity + windVelocity) / particle.mass

def electricFieldAccel(particle, summedElectricField):
    return summedElectricField * particle.charge / particle.mass

"""
def windAccel(particle, windVelocity): # worry about this later
    return
"""

cubes = []

for x in range(0, 301, 1): # 3 meters radius, 7 meters tall area
    for z in range(0, 701, 1):
        position = [x / 100, 0, z /100]
        # 10 micrometers diameter variant
        cubes.append(Particle(10 * (10 ** -6), 4.89 * 10 ** -8 * (1 / 100) ** 3, position))
        # 2.5 micrometers diameter variant
        cubes.append(Particle(2.5 * (10 ** -6), 2.05 * 10 ** -8 * (1 / 100) ** 3, position))

Tower(1.9 * 10 ** -7, 7)

time = 3600 # 3600 seconds
timeStep = 0.01 



"""
randZ = -1
while randZ < 0:
    randX = random.random()
    randY = random.random()
    randZ = 1 - randX - randY
windVelocity = [math.sqrt(5.81152 ** 2 * randX) * random.choice((-1, 1)), math.sqrt(5.81152 ** 2 * randY) * random.choice((-1, 1)), math.sqrt(5.81152 ** 2 * randZ) * random.choice((-1, 1))]
"""