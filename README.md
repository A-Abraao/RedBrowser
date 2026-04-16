#Sobre o RedBrowser#

O **RedBrowser** é um software que roda no Windows e serve para **agendar a execução de publicações em redes sociais** ou **realizar alguma tarefa via web**

A tarefa é agendada por uma interface criada com **JavaScript** e que roda no Windows graças o framework **Electron**. O usuário digita o titulo da tarefa e oque o Software deve fazer. As tarefas podem ser executadas na hora, ou então **serem agendadas em um dia e horário especifico**.

O Software agenda a aexecução de tarefas usando o Agendador de Tarefas do Windows, que define um dia e horário específico para a tarefa ser realizada.

Quando chega o horário e dia certo da tarefa ser executada, o Windows aciona o **script Python que foi criado especialmente para a terefa**. Esse script vai usar o framework **Selenium WebDriver** e arquivos **.bat** criados especificamente para poder realizar a tarefa.

Todo o processo é feito localmente na máquina do usuário.

##Frameworks e ferramentas usadas:
**React** 
**Electron**
**Selenium**
**Agendador de tarefas do Windows**
**Python**
