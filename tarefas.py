import os
import sys

from model import Task, Machine, LP

def parseLine(lines):
  line = [int(num) for num in lines.pop(0).split(' ')]

  if len(line) == 0:
    raise ValueError
  elif len(line) == 1:
    return line.pop(0)
  else:
    return line

def printLine(line):
  print(' '.join(["%.1f" % num for num in line]))

if __name__ == "__main__":
  try:
    path = sys.argv[1]
    inp = open(path, 'r')
  except IndexError:
    path = None
    inp = sys.stdin

  content = inp.read()
  lines = content.splitlines()

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
  for mdx in range(numMachines):
    s = inp.parseLine()
    for _ in range(s):
      machines[mdx-1].addTask(tasks[inp.parseLine()-1])

  # Define problema:
  lp = LP(tasks, machines)

  # Resolve problema:
  lp.solve()

  for machine in machines:
    line = []
    for task in tasks:
      try:
        tdx = machine.tasks.index(task)
        line.append(machine.vars[tdx].varValue)
      except ValueError:
        line.append(0.0)
    printLine(line)

  printLine(lp.solution)