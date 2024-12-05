# RLProject
Code for my project and instructions on how to use it

# Requirement(s):
Have Pycharm installed on your system

# Installation of testing version of Minecraft:
1) Extract the zipped folders labelled bin, bin2 and bin3 in ffmpeg
2) Put the .exe files from bin2 and bin3 into bin
3) Add bin path to environment variables
3AA) ![Step 1](https://github.com/PawanPaul/RLProject/blob/main/Pictures/FFMPEGtoPathStep1.png)
3A) Copy path to bin
3BA) ![Step 2](https://github.com/PawanPaul/RLProject/blob/main/Pictures/FFMPEGtoPathStep2.png)
3B) Search for environment variables in system search bar
3CA) ![Step 3](https://github.com/PawanPaul/RLProject/blob/main/Pictures/FFMPEGtoPathStep3.png)
3C) Click on the 'Environment Variables' option
3DA) ![Step 4](https://github.com/PawanPaul/RLProject/blob/main/Pictures/FFMPEGtoPathStep4.png)
3D) Double click on 'Path'
3EA) ![Step 5](https://github.com/PawanPaul/RLProject/blob/main/Pictures/FFMPEGtoPathStep5.png)
3E) Paste path into the list, or click 'New' and insert from there
4) Open up powershell in admin mode
5) Run cmd: Set-ExecutionPolicy -Scope CurrentUser Unrestricted
6) cd into scripts folder (navigate to scripts folder)
7) Run cmd: .\malmo_install.ps1
8) To run Minecraft, go to 'Minecraft' folder and run launchClient.bat (if you are on windows). It will start loading. (N. This version of Minecraft operates on the MinecraftForge plugin and thus counts as a game. If your Wi-Fi prevents access to games, it will cause launch to fail. Kindly switch to your mobile network, or a non-restricted Wi-Fi if that is the case)

# Setting up the coding/testing environment
1) Open Pycharm
2) Open Project as the 'Python Examples' folder
3A) ![Step 1](https://github.com/PawanPaul/RLProject/blob/main/Pictures/malmoInstallStep1.png)
3) Click on the gear icon on the top-right of the window and select 'Settings'
4A) ![Step 2](https://github.com/PawanPaul/RLProject/blob/main/Pictures/malmoInstallStep2.png)
4) Go to 'Python Interpreter'
5) Set interpreter to Python 3.6
6) Click on the '+' icon below the Python interpreter select or use the shortcut 'Alt + Insert'
7A) ![Step 1](https://github.com/PawanPaul/RLProject/blob/main/Pictures/malmoInstallStep3.png)
7) Search for malmo and select the pack
8) Check 'specify version' button and enter version 0.35.6.0
9) Install the package
10) Search for pytest and select the pack
11) Install the package
12) Open tutorial_2.py
13) Ctrl + F and search for C:/Users/pawan/Documents/RLMEMORY
14) Replace with local location of RLMEMORY
15) Repeat steps 13 and 14 in RLAIMainFunc.py

# Running the RL AI
1) Open tutorial_2.py
2) Ensure Minecraft is set up and running (Do only Step #8 in Installation of testing version of Minecraft if setup is already complete)
3) Run tutorial_2.py

# Running function test cases
1) Open RLAItester.py
2) Run RLAItester.py

# Data Flow Diagrams of current active system
The AI is too huge to show simply in a single DFD, so it has been divided into major subcomponents for easier viewing. Refer to RLDataFlowDiagram.mdj if you would like to see the large DFD
1) ![Supercontroller](https://github.com/PawanPaul/RLProject/blob/main/Pictures/SupercontrollerDFD.png)
2) ![Learning Handler](https://github.com/PawanPaul/RLProject/blob/main/Pictures/LearningHandlerDFD.png)
3) ![Move Eval](https://github.com/PawanPaul/RLProject/blob/main/Pictures/MoveEvalDFD.png)
4) ![Move Handler](https://github.com/PawanPaul/RLProject/blob/main/Pictures/MoveHandlerDFD.png)
5) ![Move Post Action Evaluator](https://github.com/PawanPaul/RLProject/blob/main/Pictures/MovePostActionEvalDFD.png)
6) ![Mine Eval](https://github.com/PawanPaul/RLProject/blob/main/Pictures/MineEvalDFD.png)
7) ![Mine Handler](https://github.com/PawanPaul/RLProject/blob/main/Pictures/MineHandlerDFD.png)
8) ![Mine Post Action Evaluator](https://github.com/PawanPaul/RLProject/blob/main/Pictures/MinePostActionEvalDFD.png)
9) ![Craft Eval](https://github.com/PawanPaul/RLProject/blob/main/Pictures/CraftEvalDFD.png)
10) ![Craft Handler](https://github.com/PawanPaul/RLProject/blob/main/Pictures/CraftHandlerDFD.png)
11) ![Craft Post Action Evaluator](https://github.com/PawanPaul/RLProject/blob/main/Pictures/CraftPostActionEvalDFD.png)
12) ![Request Handler](https://github.com/PawanPaul/RLProject/blob/main/Pictures/RequestHandlerDFD.png)
13) ![Move Request Handler](https://github.com/PawanPaul/RLProject/blob/main/Pictures/MoveRequestHandlerDFD.png)
14) ![Move Request Eval](https://github.com/PawanPaul/RLProject/blob/main/Pictures/MoveRequestEvalDFD.png)
15) ![Mine Request Handler](https://github.com/PawanPaul/RLProject/blob/main/Pictures/MineRequestHandlerDFD.png)
16) ![Craft Request Handler](https://github.com/PawanPaul/RLProject/blob/main/Pictures/CraftRequestHandlerDFD.png)
