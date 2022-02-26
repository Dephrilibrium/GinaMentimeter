# GinaMentimeter
This python-script is developed for a friend of mine (school-teacher) who wanted to auto-post some terms and defintions to a [mentimeter][MentiMeter]-page for it's students.

## Installation/Tools
For Windows:
Install the following tools:
* Optional: An IDE like [VSCode][VSCode]. You don't have to, it's also possible to run it via CMD/Powershell
* [Python][python] (add them to PATH-Variables to access it from terminal; Tested with [Python3][python3])
  * Custom installation
  * Next
    * Install for all users
    * Associate files with python (requires py launcher)
    * Create shortcuts for install applications
    * Add Python to environment variables
    * Precompile standard library
  * Install

and ensure pip and plugins are available by running on terminal (CMD/Powershell):
* ```python -m pip install --upgrade pip setuptools wheel```
* ```python -m pip install colorama```
* ```python -m pip install requests_html```
* ```python -m pip install json```


For Linux:
* Linux users know how to install python


## How to use
### Preparation before starting the script
1. Open the folder where you saved the repository
2. Open the "vote.py" file
  * change your your MentiMeter-ID (idCode = "<your-ID>")
  * change the time in seconds you want to wait before posting (wait_seconds = "<float>")
  * change the word-list you want to post (words = ["<word-list comma-separated>"];
3. Save "vote.py"

### Running the script
1. Open a CMD/Powershell and change to the repository (```cd "<Path/to/MentiMeter.py>"```)
2. Run ```python MentiMeter.py```
3. The scripts is executed. Python gets the post-HTML from mentimeter, waits the time and posts the word-list
 


[MentiMeter]: https://www.mentimeter.com/
[VSCode]: https://code.visualstudio.com/
[python]: https://www.python.org/downloads/
[python3]: https://www.python.org/downloads/release/python-3102/