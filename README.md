lp_scheduler
============

Um simples escalonador de tarefas usando programação linear.

O relatório do trabalho se encontra em `./relatorio.pdf`.

Instalação
----------

O processo de instalação ao rodar o comando `make` consiste em:

* Criar links simbólicos em `.` apontando para os exemplos em `./assets/`;
* Criar um ambiente virtual `venv` (ou `virtualenv`) em um subdiretório do projeto (`./venv`);
* Ativar o `venv`;
* Instalar o pacote `lp_scheduler` e sua única dependência (`pulp`) dentro do `venv` (deixando, portanto, o ambiente do sistema e do usuário intactos no processo);
* Criar um script executável `./tarefas` que executa o programa `lp_schedule` recém instalado dentro do `venv`.

Os executáveis para criação de ambientes virtuais para `python3` variam de sistema para sistema, então a linha de comando utilizada no `makefile` (`virtualenv -p python3 venv`) é a que funciona na máquina virtual `macalan`. Caso se deseje realizar a instalação em outro ambiente, aonde o `makefile` falhe, é recomendado instalar o pacote `python3-virtualenv` ou `python3-venv` via `apt-get` ou o pacote `virtualenv` via `pip3` e criar o ambiente manualmente em `./venv` para então rodar novamente o `makefile`. Outra alternativa é apenas instalar o pacote no ambiente do sistema ou do usuário através de `pip3 install .` e utilizar o executável `lp_schedule` instalado.

Uso
---

Conforme instalação especificada no enunciado do trabalho:

`./tarefas < exemplo1.txt`

`./tarefas < exemplo2.txt`

Instalando apenas o pacote `lp_scheduler`:

`lp_schedule < assets/exemplo1.txt`

`lp_schedule < assets/exemplo2.txt`