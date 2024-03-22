import math
import random
# smog calculations
# approximate smog particles as sphere

class Particle: # individual particle
    diameter = 0
    radius = 0
    volume = 0
    velocity = [0, 0, 0]
    position = [0, 0, 0]
    crossSectionalArea = 0
    particleDensity = 1950
    mass = 0
    charge =  1.602 * (10 ** -19)

    def __init__(self, diameter):
        self.diameter = diameter
        self.radius = diameter / 2
        self.volume = 4 / 3 * math.pi * (self.radius ** 3)
        self.crossSectionalArea = math.pi * (self.radius ** 2)
        self.mass = self.volume * self.particleDensity

class ParticleCube: # 1cm by 1cm by 1cm cube, presume all particles are at center
    particle10um = 0
    particle5HalvesUm = 0
    particle10umDensity = 4.89 * 10 ** -8 * (1 / 100) ** 3
    particle5HalvesUmDensity = 2.05 * 10 ** -8 * (1 / 100) ** 3
    numParticles10um = 0
    numParticles5HalvesUm = 0
    charge = 0

    def __init__(self, particle10um, particle5HalvesUm):
        self.particle10um = particle10um
        self.particle5HalvesUm = particle5HalvesUm
        self.numParticles10um = self.particle10umDensity / particle10um.mass
        self.numParticles5HalvesUm = self.particle5HalvesUmDensity / particle5HalvesUm.mass
        self.charge = (self.numParticles10um + self.numParticles5HalvesUm) * particle10um.charge

    def electricField(self):
        pass

class Tower: # approximate the tower as a line charge
    chargeDensity = 0
    height = 0
    
    def __init__(self, chargeDensity, height):
        self.chargeDensity = chargeDensity
        self.height = height

    def electricField(self, particle):
        z = math.sqrt(particle.position[0] ** 2 + particle.position[1] ** 2)
        unitVec = (particle.position) / z
        eMag = 8.98 * 10 ** 9 * self.chargeDensity * particle.position / z * (particle.position[2]/math.sqrt(z ** 2 + particle.position[2] ** 2) + (self.height - particle.position[2])/math.sqrt(z ** 2 + (self.height - particle.position[2] ** 2)))
        return eMag * unitVec

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

# 10 micrometers diameter variant
particle10um = Particle(10 * (10 ** -6))
# 2.5 micrometers diameter variant
particle5HalvesUm = Particle(2.5 * (10 ** -6))

cubes = []

for x in range(0, 3.01, 0.01):
    for y in range(0, 3.01, 0.01):
        for z in range(0, 7.01, 0.01):
            cubes.append(ParticleCube())

# 3 meters radius, 7 meters tall

Tower(1.9 * 10 ** -7, 7)

"""
randZ = -1
while randZ < 0:
    randX = random.random()
    randY = random.random()
    randZ = 1 - randX - randY
windVelocity = [math.sqrt(5.81152 ** 2 * randX) * random.choice((-1, 1)), math.sqrt(5.81152 ** 2 * randY) * random.choice((-1, 1)), math.sqrt(5.81152 ** 2 * randZ) * random.choice((-1, 1))]
"""