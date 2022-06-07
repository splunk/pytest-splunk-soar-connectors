# pytest-splunk-soar-connectors

A pytest plugin to perform unit testing for Splunk SOAR Apps. Please [review the documentation](https://splunk.github.io/pytest-splunk-soar-connectors/) on how to use this plugin.

## Local Development

It is recommended to create a virtual environment for this plugin. Run the below commands to install the package locally into a Python environment.

```
git clone https://github.com/dfederschmidt/pytest-splunk-soar-connectors
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

```
pytest
```

## Building the Documentation

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdocs serve -a localhost:9090
```

You should be able to access the local documentation at [https://localhost:9090](http://localhost:9090).

## NOTICE File

Generate from requirements.txt
```
pip-licenses --format=markdown  > NOTICE.md
```

## Splunk Copyright Notice

Copyright 2022 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.