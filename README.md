# 🚀 RedBrowser

## 📌 Sobre o Projeto

O **RedBrowser** é um software desktop para Windows que permite **agendar a execução de tarefas automatizadas na web**, como publicações em redes sociais.

Toda a automação é executada **localmente na máquina do usuário**, garantindo maior controle e independência de serviços externos.

---

## ⚙️ Funcionamento

O fluxo do sistema funciona da seguinte forma:

1. O usuário cria uma tarefa através de uma interface desenvolvida em **JavaScript** com **Electron**
2. Define:
   - 📝 Título da tarefa  
   - ⚡ A ação que o software deve executar  
   - 🕒 Data e horário (opcional)

3. A tarefa pode ser:
   - Executada imediatamente  
   - Agendada para um horário específico  

4. O sistema utiliza o **Agendador de Tarefas do Windows** para programar a execução

5. No momento definido:
   - O Windows executa um **script Python específico da tarefa**
   - O script utiliza **Selenium WebDriver** para automatizar ações no navegador
   - Scripts auxiliares `.bat` podem ser usados para suporte à execução

---

## 🧠 Arquitetura

O sistema é dividido em três camadas principais:

- **Interface (Frontend)**
  - Desenvolvida com React + Electron
  - Responsável pela criação e gerenciamento das tarefas

- **Agendamento**
  - Integração com o Agendador de Tarefas do Windows

- **Execução**
  - Scripts Python + Selenium WebDriver
  - Automação de ações na web

---

## 🛠️ Tecnologias Utilizadas

- ⚛️ **React**
- 🖥️ **Electron**
- 🐍 **Python**
- 🤖 **Selenium WebDriver**
- 🗓️ **Agendador de Tarefas do Windows**
- 📜 Scripts **.bat**

---

## 🔒 Execução Local

Todo o processamento é feito localmente, sem dependência de servidores externos:
- Maior segurança
- Maior controle das tarefas
- Independência de conexão constante

---
