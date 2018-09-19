# The Software for Uncertainty Model

## How to join the building of project

- Make sure you have installed the git and have received the github invitation
- Go to the root path and open your bash cmd
- write the following command

```bash
git clone https://github.com/noaRricky/Uncertainty.git # download the whole project
git fetch # provide your username and password to access the project
git branch <name> # build your new exciting branch
git checkout <name> # dive into your branch and write your code
...
git push origin <name> # after you have add and commit your contribution, don't forget to push the remote
```

## Build up environment

- Go to the root path

```cmd
conda create -n <name> python=2.7 # create virtual environment with python 2.7 interpreter
conda install --file=requirement.txt
```