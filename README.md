# MITGUI
Authors: Sione Manulea, Joshua Clarke
- Python version: 3.6.8

This software was created by students at the Otago Polytechnic for our Project 1 & 2 papers in the BIT degree. It is a prototype demo of software that has the potential to allow physically impaired individuals to use a personal computer via facial gestures.

For example they could map a keystroke to the "open mouth" gesture. This would mean that while running the software, they could open their mouth and the keystroke of their choosing would be sent to the computer by the software, rather than by the keyboard.

# Installation instructions
## 1. Git
Download Git for your operating system here: https://git-scm.com/downloads
And depending if your computer is 34-bit or 64-bit, download Git for your particular windows setup.

Once it's downloaded, you need to open the Git.exe file you downloaded.

Here is the step by step instructions on how to install git correctly.

1. GNU General Public License -> Click Next 
2. Selection Destination Location -> Nothing to change here, click Next
3. Select Components -> Nothing to change here, click Next
4. Select Start Menu Folder -> Nothing to change here, click Next
5. Choosing the default editor used by Git -> Unless your a professional, click Next
6. Adjusting your PATH environment -> Again, unless you know what you're doing or your a wizard, click Next
7. Choosing HTTPS transport backend -> click Next
8. Configuring the line ending conversions -> click Next
9. Configuring the terminal emulator to use with Git Bash -> click Next
10. Configuring extra options -> click Next
11. Configuring experimental options -> click Next
12. Click Install

This shouldn't take too long.

Completing the Git Setup Wizard -> Make sure "Launch Git Bash" is checked, and then click Finish

### A wild prompt should appear (if it doesn't, then click the start menu, and while the start menu is active type "Git Bash" and click the Git Bash app)

Once the command prompt is open, click anywhere in the box then type these commands:

* mkdir fr
* cd fr
* git clone https://github.com/manulea/MITGUI

If the command is successful you should beable to see "Cloning into 'MITGUI'"

Okay now you can close the Git Bash app with the X button.


## 2. Anaconda Distribution
Go to this website to install Anaconda Distribution: https://www.anaconda.com/distribution/
While on the page, scroll down a bit until you see Windows, Mac or Linux.
Choose the operating system that you are installing this software on.
Then under Python 3.7 version, you will need to download the Graphical installer.
For windows: if you don't know if you're 64 bit or 32 bit here is a guide: https://www.lifewire.com/am-i-running-a-32-bit-or-64-bit-version-of-windows-2624475

--- TO BE CONTINUED ---

Once it's downloaded and installed, open Anaconda Prompt from the start menu and type in these commands:
* conda update conda
* conda install -c anaconda python

## You are now ready to run the software 

# GUI how to run the software.
Using the Anaconda prompt
cd in to the *MITGUI* directory
* pipenv shell
* pipenv sync

# RUNNING
* python FR2.py

# A special thanks to the following creators of these Libraries:
* [PyQt5 5.13.0](https://pypi.org/project/PyQt5/)
* [dlib 19.17.0](https://pypi.org/project/dlib/)
* [opencv-python 4.1.0.25](https://pypi.org/project/opencv-python/)
* [imutils 0.5.2](https://pypi.org/project/imutils/)
* [numpy 1.17.0 ](https://pypi.org/project/numpy/)
* [pywin32 224](https://pypi.org/project/pywin32/)
* [pygame 1.9.6](https://pypi.org/project/pygame/)
