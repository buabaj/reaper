# Reaper - Fast Dead Code Analyser

Reaper is a python utility tool designed for analysis of python codebases. It finds dead(unused) code in python programs. Reaper might omit some dead code or report code that as been implicitly called as unused.

## Features
* Performs checks on unused imports, functions, classes, methods, attributes, locals, and globals within Python code.
* Enables analysis of individual Python files or entire directories containing Python scripts.
* Utilizes multiprocessing to process multiple files concurrently.
* Users can configure specific checks to perform based on their requirements.

## Usage
* Set up your config.json file for specific requirements:
```
{
    "checks": [
      "functions",
      "classes",
      "methods",
      "attributes" 
    ]
}
```
* Run reaper using:
```
python3 reaper.py [files/directory] -c config.json
```

* add the `-h` option the command to check out the available options.

```bash
positional arguments:
  paths                 Files or directory path(s) containing Python code

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
```

## Contributing

- Fork this repository to your GitHub account.
- Clone the forked repository to your local machine.
- Create a new branch for the feature you want to work on.
- Make your contributions.
- Push your local branch to your remote repository.
- Open a pull request to the develop branch of this repository.


