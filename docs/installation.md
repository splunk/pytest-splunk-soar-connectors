This package is not published to the Python Package Index (PyPi) at this time so we'll outline the steps needed to install the plugin from its Github repository. 

#### Prerequisites
- Python 3

It is strongly recommended to install this package in your projects [virtual environment](https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.) as part of your local development. The commands below assume you are located in the root directory of your SOAR app. If you already have an existing virtual environment, you can skip these steps.


#### Create a virtual environment (optional)
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install pytest-splunk-soar-connectors
```
pip install git+https://github.com/splunk/pytest-splunk-soar-connectors
```
