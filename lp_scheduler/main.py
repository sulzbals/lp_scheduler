import os
import sys

from lp_scheduler.model import Task, Machine, LP

class InvalidInput(Exception):
  '''
  Exceção de entrada inválida
  '''
  def __init__(self, message, fp=sys.stderr):
    # Escreve mensagem de erro no respectivo arquivo (STDERR por padrão):
    fp.write("Entrada inválida: " + message + "\n")

    # Encerra programa:
    quit()


class Line:
  '''
  Linha de entrada/saída
  '''
  def __init__(self):
    self.content = []

  @staticmethod
  def fromString(string):
    '''
    Instancia uma linha dada uma string
    '''
    this = Line()
    this.content = string.split(' ')
    return this

  @staticmethod
  def fromFLoat(flt):
    '''
    Instancia uma linha dado um float ou um conjunto de floats
    '''
    this = Line()

    try:
      for num in flt:
        this.addFloat(num)
    except TypeError:
      this.addFloat(flt)

    return this

  def __len__(self):
    '''
    Definimos tamanho da linha como o número de elementos numéricos dela
    '''
    return len(self.content)

  def __str__(self):
    '''
    Conversão da linha para string (elementos separados por espaço + newline)
    '''
    return " ".join(self.content) + "\n"

  def toInt(self):
    '''
    Conversão da linha para int ou conjunto de ints
    '''
    if len(self) > 1:
      return [int(elm) for elm in self.content]
    else:
      return (int(self.content.pop()))

  def addFloat(self, num):
    '''
    Adiciona um float à linha
    '''
    self.content.append("%.1f" % num)


class Parser:
  '''
  Leitor da entrada do problema
  '''
  def __init__(self, fp=sys.stdin):
    self.fp = fp

  def parse(self):
    '''
    Lê a entrada (STDIN por padrão) linha por linha
    '''
    self.content = self.fp.read()
    self.lines = [Line.fromString(line) for line in self.content.splitlines()]

  def getLine(self, count):
    '''
    Acessa a próxima linha e verifica se o número de valores contidos nela é
    válido
    '''
    try:
      line = self.lines.pop(0)
    except IndexError:
      raise InvalidInput("Fim do arquivo inesperado")

    if len(line) != count:
      raise InvalidInput(
        "%d valor(es) esperado(s) na linha, %d recebido(s)" % (count, len(line))
      )

    return line


class Writer:
  '''
  Escritor da saída do problema
  '''
  def __init__(self, fp=sys.stdout):
    self.fp = fp

  def writeLine(self, line):
    '''
    Escreve uma linha na saída (STDOUT por padrão)
    '''
    self.fp.write(str(line))


def main():
  # Faz o parsing da entrada:
  parser = Parser()
  parser.parse()

  # Lê o número de tarefas (n) e o número de máquinas (l):
  numTasks, numMachines = parser.getLine(2).toInt()

  tasks = []
  machines = []

  # Lê os tempos em horas por tarefa (h):
  for _ in range(numTasks):
    tasks.append(Task(parser.getLine(1).toInt()))

  # Lê os custos (c) e os tempos máximos de uso por máquina (u):
  for _ in range(numMachines):
    c, u = parser.getLine(2).toInt()
    machines.append(Machine(c, u))

  # Lê o número de tarefas executáveis por máquina (s) e seus índices (t):
  for mdx in range(numMachines):
    s = parser.getLine(1).toInt()
    for _ in range(s):
      # Associa a tarefa à máquina que pode executá-la:
      machines[mdx-1].addTask(tasks[parser.getLine(1).toInt()-1])

  lp = LP(tasks, machines)

  # Modela problema:
  lp.model()

  # Resolve problema:
  lp.solve()

  writer = Writer()

  # Escreve os valores de cada variável por máquina:
  for machine in machines:
    line = Line()
    for task in tasks:
      try:
        tdx = machine.tasks.index(task)
        line.addFloat(machine.vars[tdx].varValue)
      except ValueError:
        line.addFloat(0.0)
    writer.writeLine(line)

  # Escreve solução do problema:
  writer.writeLine(Line.fromFLoat(lp.solution))

if __name__ == "__main__":
  main()