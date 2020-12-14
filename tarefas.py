#! /usr/bin/env python3

import os
import sys
import tempfile
import subprocess

class Input:
  def __init__(self):
    try:
      self.path = sys.argv[1]
      self.file = open(self.path, 'r')
    except IndexError:
      self.path = None
      self.file = sys.stdin

    self.content = self.file.read()
    self.lines = self.content.splitlines()

  def parseLine(self):
    line = [int(num) for num in self.lines.pop(0).split(' ')]

    if len(line) == 0:
      raise ValueError
    elif len(line) == 1:
      return line.pop(0)
    else:
      return line


class Task:
  def __init__(self, runTime):
    self.runTime = runTime


class Machine:
  def __init__(self, cost, maxTime):
    self.cost = cost
    self.maxTime = maxTime

    self.tasks = []

  def addTask(self, task):
    self.tasks.append(task)


class LP:
  def __init__(self, tasks, machines):
    objFunc = ""
    for idx in range(1, len(machines)+1):
      for jdx in range(1, len(tasks)+1):
        if machines[idx-1].cost:
          objFunc += " + {}m{}t{}".format(machines[idx-1].cost, idx, jdx)
    objFunc = "min:" + objFunc[2:] + ";"

    restrictions = []

    for idx in range(1, len(machines)+1):
      for jdx in range(1, len(tasks)+1):
        restrictions.append("m{}t{} >= 0;".format(idx, jdx))

    for idx in range(1, len(machines)+1):
      rest = ""
      for jdx in range(1, len(tasks)+1):
        rest += " + m{}t{}".format(idx, jdx)
      restrictions.append(rest[3:] + " <= {};".format(machines[idx-1].maxTime))

    for jdx in range(1, len(tasks)+1):
      rest = ""
      for idx in range(1, len(machines)+1):
        if tasks[jdx-1] in machines[idx-1].tasks:
          rest += " + m{}t{}".format(idx, jdx)
      restrictions.append(rest[3:] + " = {};".format(tasks[jdx-1].runTime))

    self.model = objFunc + "\n\n" + '\n'.join(restrictions)

  def print(self):
    print(self.model)

  def save(self):
    fd, path = tempfile.mkstemp()
    fp = open(path, 'w')
    fp.write(self.model)
    fp.close()
    os.close(fd)
    return path


class Solver:
  def __init__(self, path, numMachines, numTasks):
    self.path = path
    self.numMachines = numMachines
    self.numTasks = numTasks

  def solve(self):
    self.sol = subprocess.run(["lp_solve", self.path], stdout=subprocess.PIPE).stdout.decode("utf-8").splitlines()

  def parse(self):
    out = []

    for idx in range(1, self.numMachines+1):
      m = []
      for jdx in range(1, self.numTasks+1):
        for line in self.sol:
          if "m{}t{}".format(idx, jdx) in line:
            m.append(line.split(' ').pop())
            break
      out.append(' '.join(m))

    for line in self.sol:
      if "Value of objective function" in line:
        out.append(str(int(float(line.split(' ').pop()))))
        break

    return out


if __name__ == "__main__":
  inp = Input()

  # Número de tarefas (n)
  # Número de máquinas (l)
  numTasks, numMachines = inp.parseLine()

  tasks = []
  machines = []

  # Tempo em horas por tarefa (h)
  for _ in range(numTasks):
    tasks.append(Task(inp.parseLine()))

  # Custo por hora por máquina (c)
  # Tempo máximo em horas de uso por máquina (u)
  for _ in range(numMachines):
    c, u = inp.parseLine()
    machines.append(Machine(c, u))

  # Número de tarefas por máquina (s)
  # Índices das tarefas suportadas por máquina (t)
  for idx in range(numMachines):
    s = inp.parseLine()
    for _ in range(s):
      machines[idx-1].addTask(tasks[inp.parseLine()-1])

  lp = LP(tasks, machines)

  path = lp.save()

  solver = Solver(path, numMachines, numTasks)
  solver.solve()

  os.remove(path)

  print('\n'.join(solver.parse()))
