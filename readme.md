# README

## Simulex: the simulation exercise of executive simultaneous exchange

Lachlan Pham, Peter Mahhov, Mathilde Simoni <br/>
Software Engineering <br/>
Spring 2022 <br/>

### Project Description
A Scenario-based financial literacy learning tool to address the barriers in learning about financial markets and help individuals know the risks of investing in the stock market.
![Alt text](screenshots/screenshot1.jpg?raw=true "Menu")
![Alt text](screenshots/screenshot2.jpg?raw=true "Game")

### Instructions to run the code
Assuming you have python 3.9.* and pip, please download the following using "pip install" or "pip3 install" in terminal. Tested version numbers are in brackets. If you are having difficulties with dependencies, specify the version number as well e.g. "pip install pygame=2.1.2":
* pygame (2.1.2)
* pygame_gui (0.6.4)
* numpy (1.21.5)
* matplotlib (3.5.1)

Then, navigate in the SE_project folder and run the following command: `python3 source/main.py`

### Instruction for development and testing
Simulex was developed within a conda environment. To set this up, type these commands into terminal, whilst in the SE_project folder:
* pip install conda OR pip3 install conda (installing conda if you don't already have it)
* conda create -n simulex python=3.9 (creating conda environment)
* conda activate simulex (activating conda environment)
* conda install invoke
* invoke bootstrap (will install all necessary development libraries)

Now you may use the following commands to develop
* invoke test (uses pytest to run tests in tests folder)
* invoke check (checks if python files are well-formatted)
* invoke format (automatically formats python files)


### TODO list
- [X] functions to restart scenario and go to next scenario
- [X] copy data loan
- [X] set scroll when splitting
- [X] text box default test "enter the amount"
- [X] menu 
- [X] create risk table
- [X] Update Gantt chart
- [X] write text with informaiton about loan and stocks (in config.yaml)
- [X] implement change in trends for stocks and loans
- [X] create level module
- [X] finish writing tutorials 
- [X] add html syntax to tutorials
- [X] implement level module 3
- [X] finish implementation level module 2 (name stocks)
- [X] update all game messages
- [X] update subtitle
- [X] finish comments (lachlan)
- [X] update gantt chart
- [ ] add code for logs (lachlan)
- [X] Finish validation test plan
- [X] Finish test cases
- [X] write test results
- [X] ending message after level 3 (go back to level 1)
- [X] explain you can open tutorial any time (Peter)
- [X] examine def of netcash flow (Peter)
- [X] screenshots readme file (Peter)

