# GETTING STARTED
* In this project we are using Langchain to build a few applications from scratch and explore the funtionalities. This Project is entirely written in Python and we are using Poetry for Package Manangement and ruff to get the proper syntaxes and keep the code clean/
## Steps to Install PIPX
* Inorder to install Poetry you will need pipx which can be installed using the below command
```bash
brew install pipx
pipx ensurepath
```
To allow pipx actions global scope
```bash
sudo pipx ensurepath --global
```
To prepend the pipx bin directory to PATH instead of appending it.
```bash
sudo pipx ensurepath --prepend
```
If in case you PIPX is not added to your ZShell the run the below mentioned command
```bash
PATH="$PATH:$HOME/.local/bin"
```
Add this to the existing path else create this vaiable and add it.

## Steps to install Poetry
* Command to install Poetry
```bash
pipx install poetry
```
* basic poetry command
```bash
poetry install # Installs all the packages mentioned in the pyproject.toml in a venv
env activate # Activates teh venv once all installations are done
poetry env info # Gives you the list of venvs installed in the System.
```

## Steps to install ruff
* Ruff is a tool used to maintain the code quality and readability in python. We have used this to format the code in a readble way
```bash
brew install ruff # incase of using mac home brew
pip install ruff # For the pip Installation
```
* Basic commands in ruff
```bash
ruff rule # Explains a specific rule or lists all supported rules.
ruff config # Lists or describes available configuration options.
ruff linter # Lists all supported upstream linters integrated into Ruff.
ruff clean # Clears any caches in the current directory and subdirectories.
ruff server # Runs the Ruff language server, often used with editor integrations.
ruff analyze # Runs analysis over Python source code.
ruff version # Displays the installed Ruff version.
ruff help # Provides general help or help for a specific subcommand.
ruff check --fix <FileName> # Imporves the code readbility
```
## Running the Application locally
The first module fo this project is a basic implementation of the AI API Request where we will make a curl call with out query. In this project we are using the Gemini AI.
Once all the API Keys are imported in to the `.env` file we are good to start up this application.
In the chat_mode module under the conversational_chat_model you will be able to see the API Request to make the API call to gemini with a question. And the response is parsed in the out put. This is a very rudimentary approach where we are making CURL calls and it involves wirting a lot of code.
The second menthod is more of an SDK Approach Where we are using in-built featuress from the langchain module to avoid all the manual codes and to make it a more conversation chat where we can open up a command line ui and it will interact with us.
