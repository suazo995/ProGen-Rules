# ProGen Rules

ProGen Rules is a command line tool which aims to generate the ProGuard rules needed by an Andorid application project in order to effectively implement ProGuard.

This generation is done by two solutions:
  1. **Dependency Rules Solution**: This solution is in charge of generating rules specific to the third party libraries declared as dependencies of the project. It does so by relying on the croud-sourced wisdom of applications which have already implemented ProGuard
  . The solution detects the projects dependencies, then consults our pool of knowledge to determine which rules have been used for said dependencies in other applications and finally use diverse heuristics in order to select rules relevant for the project.

  2. **Application Specific Rule Solution**: This solution analyses the source code of the project in order. It searches for the use of three common practices known to clash with ProGuard functionality: Data Classes, JNI calls from native side and resource loading from APK. It then redacts appropriate rules for this instances.

## Installation

### Requirements:
  * Python 3.8.3 or compatible.

  * Pip package installer.


### Installation Guide:
1. Download the source-code from GitHub.

2. Add the download location to PYTHONPATH.
```bash
export PYTHONPATH="${PYTHONPATH}:<Path-where-source-code-was-saved>"
```

3. Install requirements using the requirements.txt file included and pip.
```bash
pip install -r requirements.txt
```
## Usage

In order to use ProGen Rules, one must run the desired Python script.

In both cases, one must start the command with python3, followed by the name of the desired scipt and finally the path to the Android project which needs the rule generation. Options may be specified at the end of the command.

The resulting files will be written into the project directory. In order to specify other directory one must use the -d option.

1. Dependency Rules Solution
```bash
python3 generateDependencyRules.py -p <application-project-path> <options>

options:     -v: Makes command verbose.
             -d,--dir: Directory in which to write the rule files.
             -h: Displays this prompt.
```

2. Application Specific Rules Solution
```bash
python3 generateDependencyRules.py -p <application-project-path> <options>

options:      -v: Makes command verbose.
              -d,--dir: Directory in which to write the rule files.
              --noRes: Disables rule generation for APK resource loading.
              --noJNI: Disables rule generation for JNI calls.
              --noData: Disables rule generation for Data Classes.
              -h: Displays this prompt.
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
