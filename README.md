# Python-Module-Installer-Script
Lightweight script which installs modules found in a python script with pip.

## For example:
Let's say a friend gave you his/her python script called foo.py, without a requirements.txt.


```python installer.py foo.py``` 


The script will parse foo.py and locate any instances of 'import' or 'from', and install the declared modules.

```python installer.py foo.py boo.py doo.py```


It is able to parse more than one script at a time, and can also detect specific version changes.

For specific version changes to apply, import and from statements must contain an inline comment that states the specified version.


```import slackclient #1.0.0```


