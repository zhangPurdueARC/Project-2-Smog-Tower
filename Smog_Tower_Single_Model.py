import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 1000000
# smog calculations
# approximate smog particles as sphere

class Particle: # 1 centimeter cube with particle info
    diameter = 0
    radius = 0
    volume = 0
    velocity = np.array([0, 0, 0])
    position = np.array([0, 0, 0])
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

class Tower: # approximate the tower as a line charge
    chargeDensity = 0
    totalCharge = 0
    height = 0
    captureParticles = [[10 * (10 ** -6), 0], [2.5 * (10 ** -6), 0]]
    kgRemoved = [0, 0]
    
    def __init__(self, chargeDensity, height):
        self.chargeDensity = chargeDensity
        self.height = height
        self.totalCharge = chargeDensity * height

    def electricField(self, particle):
        z = math.sqrt(particle.position[0] ** 2 + particle.position[1] ** 2)
        unitVec = np.array(particle.position) / z
        eMag = 8.98 * 10 ** 9 * self.chargeDensity / z * (particle.position[2]/math.sqrt(z ** 2 + particle.position[2] ** 2) + (self.height - particle.position[2])/math.sqrt(z ** 2 + (self.height - particle.position[2]) ** 2))
        return eMag * unitVec
    
    def capture(self, particle):
        self.totalCharge += particle.charge * particle.numParticles * 2 * math.pi
        self.chargeDensity = self.totalCharge / self.height
        for i in range(0, 2, 1):
            if (self.captureParticles[i][0] == particle.diameter):
                self.captureParticles[i][1] += particle.numParticles
                self.kgRemoved[i] += particle.mass
                break

# vector fields
def gravityAccel():
    return np.array([0, 0, -9.81])

def buoyantAccel(particle):
    return np.array([0, 0, 1.28 * 9.81 * particle.volume / particle.mass])

def dragAccel(particle):
    return -6 * math.pi * (1.895 * (10 ** -5)) * particle.diameter * np.array(particle.velocity) / particle.mass

def electricFieldAccel(particle, summedElectricField):
    return summedElectricField * particle.charge / particle.mass

def cubeSort(cubes):
    return sorted(cubes, key = lambda particle : particle.position[2])

cubes = []

for x in range(1, 701, 1): # 7 meters radius, 4 meters tall area
    for z in range(1, 400, 1):
        position = [x / 100, 0, z / 100]
        # 10 micrometers diameter variant
        cubes.append(Particle(10 * (10 ** -6), 4.89 * 10 ** -8, position))
        # 2.5 micrometers diameter variant
        cubes.append(Particle(2.5 * (10 ** -6), 3.35 * 10 ** -8, position))

totalMass = 0
for cube in cubes:
    totalMass += cube.mass

tower = Tower(1.9 * 10 ** -7, 7)

maxTime = 0.1
timeStep = 0.01 
currentTime = 0
with open("results.txt", "w") as file:
    while (currentTime <= maxTime):
        cubes = cubeSort(cubes)
        capturedCubes = []
        x = []
        z = []
        below = 0
        above = 0
        for cube in cubes: # ignoring charge overlaps, calculates density as though it were alone on a layer, ignoring pushes!
            charge = cube.charge * cube.numParticles
            above += charge / 0.01 / 3 / 2 / (8.854 * 10 ** -12)
        file.write(str(currentTime)+": ")
        print(currentTime)
        for cube in cubes:
            charge = cube.charge * cube.numParticles
            below += charge / 0.01 / 3 / 2 / (8.854 * 10 ** -12)
            above -= charge / 0.01 / 3 / 2 / (8.854 * 10 ** -12)
            electricField = tower.electricField(cube) + [0, 0, above] + [0, 0, -1 * below]
            accel = electricFieldAccel(cube, electricField) + dragAccel(cube) + buoyantAccel(cube) + gravityAccel()
            velocity = cube.velocity
            position = cube.position + 0.5 * accel * timeStep ** 2 + velocity * timeStep
            if (position[0] < 0):
                tower.capture(cube)
                capturedCubes.append(cube)
            else:
                if (position[2] < 0):
                    position[2] = 0
                elif (position[2] > 7):
                    position[2] = 7
                cube.velocity = velocity + accel * timeStep
                cube.position = position
                x.append(cube.position[0]) # not quite working, why?, ending up with strage graphs
                z.append(cube.position[2])
        plt.plot(x, z)
        file.write(str(x))
        file.write("\n")
        file.write(str(z))
        file.write("\n")
        plt.savefig(str(currentTime)+".png")
        for cube in capturedCubes:
            cubes.remove(cube)
        file.write(str(len(cubes))+"\n")
        currentTime += timeStep

print(tower.captureParticles)
print(tower.kgRemoved)

print(sum(tower.kgRemoved) / totalMass)