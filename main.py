from random import random, randint
from math import log, e, floor, ceil
from datetime import datetime

ln = lambda x : log(x)
roundToInf = lambda x : ceil(x) if x > 0 else floor(x)

ReproductionRate = 0.6
MultationRate = 0.01

GlobalPopulationId = 0

Log = []

def addLog(args: tuple):
    Log.append(args)
    print(reprLog(args))

def reprLog(args: tuple):
    text = ""
    if args[0] == "BiomeCreated":
        text = "群落“{}”已创建。".format(args[1])
    elif args[0] == "BiomeStartUpdate":
        text = "###-----------------\n群落“{}”开始第{}次更新。\n###-----------------".format(args[1], args[2])
    elif args[0] == "BiomeEndUpdate":
        text = "群落“{}”更新完毕。".format(args[1])
    elif args[0] == "NicheCreated":
        text = "群落“{}”中新增了规模为{}的生态位“{}”。".format(args[3].Name, args[2], args[1])
    elif args[0] == "NicheStartUpdate":
        text = "生态位“{}”开始更新。".format(args[1])
    elif args[0] == "NicheEndUpdate":
        text = "生态位“{}”更新完毕。".format(args[1])
    elif args[0] == "PopulationCreated":
        text = "生态位“{}”中新增了种群数量为{}的种群“{}”。".format(args[3].Name, args[2], args[1])
    elif args[0] == "PopulationStartUpdate":
        text = "种群“{}”开始更新。".format(args[1])
    elif args[0] == "PopulationExtincted":
        text = "种群“{}”已灭绝。".format(args[1])
    elif args[0] == "PopulationEndUpdate":
        text = "种群“{}”已完成更新，当前：N={}, ΔN={}, K={}".format(args[1], args[2], args[3], args[4])
    return text

class Biome:

    def __init__(self, name: str):
        self.Name = name
        self.Niches = []
        self.UpdateCounter = 0
        addLog(("BiomeCreated", self.Name))
    
    def Update(self):
        self.UpdateCounter += 1
        addLog(("BiomeStartUpdate", self.Name, self.UpdateCounter))
        for niche in self.Niches:
            niche.Update()
        addLog(("BiomeEndUpdate", self.Name))

class Niche:
    
    def __init__(self, name: str, size: int, biome: Biome):
        self.Name = name
        self.Size = size
        self.Biome = biome
        self.Populations = []
        addLog(("NicheCreated", self.Name, self.Size, self.Biome))
        
    def Update(self):
        addLog(("NicheStartUpdate", self.Name))
        for population in self.Populations:
            population.Update()
        addLog(("NicheEndUpdate", self.Name))

class Population:

    def __init__(self, n: int, niche: Niche):
        global GlobalPopulationId
        self.Name = str(GlobalPopulationId)
        GlobalPopulationId += 1
        self.N = n
        self.K = 0
        self.Niche = niche
        addLog(("PopulationCreated", self.Name, self.N, self.Niche))

    def Update(self):
        addLog(("PopulationStartUpdate", self.Name))
        k = self.Niche.Size
        for population in self.Niche.Populations:
            if population is not self:
                k -= population.N
        self.K = k if k > 0 else 0
        if self.K > 0:
            deltaN = roundToInf(ReproductionRate * self.N * (self.K - self.N) / self.K)
#           if deltaN > 0 and random() < 1 - (1 - MultationRate) ** deltaN:
            if deltaN > 0 and random() < 1 - e ** (deltaN * ln(1 - MultationRate)):
                self.Niche.Populations.append(Population(randint(1, 10), self.Niche))
        else:
            deltaN = roundToInf(ReproductionRate * (K - N))
        self.N += deltaN
        if self.N <= 0:
            self.Niche.remove(self)
            addLog(("PopulationExtincted", self.Name))
        addLog(("PopulationEndUpdate", self.Name, self.N, deltaN, self.K))




TheBiome = Biome("主群落")
TheBiome.Niches.append(Niche("猎物", 1000, TheBiome))
TheBiome.Niches.append(Niche("弱小", 2000, TheBiome))
TheBiome.Niches.append(Niche("远程", 600, TheBiome))
TheBiome.Niches.append(Niche("坚硬", 800, TheBiome))
TheBiome.Niches.append(Niche("精英", 100, TheBiome))
for niche in TheBiome.Niches:
    for i in range(5):
        niche.Populations.append(Population(round(niche.Size / 10 * (random() * 0.4 + 0.8)), niche))

while True:
    text = input("--> ")
    args = text.split(" ")
    if len(args) == 0:
        TheBiome.Update()
    elif args[0] == "help":
        pass
    elif args[0] == "export":
        if len(args) >= 2:
            filename = " ".join(args[1:])
        else:
            filename = datetime.now().strftime("BiomeLog-%Y-%m-%d-%H-%M-%S")
        f = open(filename + ".txt", "x")
        logText = ""
        for x in Log:
            logText += reprLog(x) + "\n"
        f.write(logText)
        f.close()
    elif args[0] == "shutdown":
        break
    else:
        TheBiome.Update()



