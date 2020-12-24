from pulp import LpProblem, LpMinimize, LpVariable, PULP_CBC_CMD

class Task:
  '''
  Tarefa a ser executada
  '''
  def __init__(self, runTime):
    self.runTime = runTime
    self.vars = []

  def addVar(self, var):
    '''
    Associa variável tempo de locação à tarefa
    '''
    self.vars.append(var)


class Machine:
  '''
  Máquina a executar tarefas
  '''
  def __init__(self, cost, maxTime):
    self.cost = cost
    self.maxTime = maxTime

    self.tasks = []
    self.vars = []

  def addTask(self, task):
    '''
    Associa tarefa a ser executada à máquina
    '''
    self.tasks.append(task)

  def addVar(self, var):
    '''
    Associa variável tempo de locação à máquina
    '''
    self.vars.append(var)


class LP:
  '''
  Programa Linear
  '''
  def __init__(self, tasks, machines):
    self.machines = machines
    self.tasks = tasks

  def model(self):
    '''
    Modela o programa linear
    '''
    # Problema de minimização:
    self.problem = LpProblem(sense=LpMinimize)

    # Para cada máquina no problema:
    for mdx, machine in enumerate(self.machines):
      # Para cada tarefa executável pela máquina:
      for tdx, task in enumerate(machine.tasks):
        # Nome da variável representando a locação:
        varName = "xm{}t{}".format(mdx+1, tdx+1)

        # Cria variável para o tempo de locação (>= 0):
        var = LpVariable(varName, lowBound=0)

        # Associa variável a suas respectivas máquina e tarefa:
        machine.addVar(var)
        task.addVar(var)

    # Para cada máquina no problema:
    for machine in self.machines:
      # Soma dos tempos de locação da máquina <= tempo máximo de uso da máquina:
      self.problem += sum(machine.vars) <= machine.maxTime

    # Para cada tarefa no problema:
    for task in self.tasks:
      # Soma dos tempos de locação para a tarefa = tempo de execução da tarefa:
      self.problem += sum(task.vars) == task.runTime

    # Soma dos tempos de locação multiplicados pelos seus custos (objetivo):
    self.problem += sum([
      sum([
        m.cost * var for var in m.vars
      ]) for m in self.machines
    ])

  def solve(self):
    '''
    Resolve o programa linear
    '''
    self.problem.solve(PULP_CBC_CMD(msg=False))
    self.solution = self.problem.objective.value()