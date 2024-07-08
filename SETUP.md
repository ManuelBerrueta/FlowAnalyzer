# Setup
There is a tiny bit of setup to get everything working here after you clone the repo...

## App Registration
First you must setup a new App Registration and secret to be able to play around with this. 

### Setup via Azure Portal:
1. Go to the Azure Portal (https://portal.azure.com)
2. Go to Microsoft Entra ID
3. Select "App registrations" under Manage in the menu blade
4. Click the "➕ New registration" button
    1. For this testing, you can leave it on "Accounts in this organizational directory only (Default Directory only - Single tenant)"
    2. Redirect URI, set it to "Web" and "https://localhost:44321/"
        - You could select a different port on localhost, but this MUST match when you enter it in the Notebook
    3. Click the **Register** button
5. Now go back to App Registration and select the application you just created
6. Go to "Certificates & secrets"
    - To start I would recommend using Client secrets, as it is pretty easy to setup just click "➕ New client secret"
        - Copy and save this secret as you will be using it throughout the notebooks, don't loose it as you won't be able to recover it, but you can create a new one
    - For Certificates authentication, you must first create the certificate and then upload it here.
        - If you are interested in that, check the `/Cert_Setup" directory for more information on how to create and set that up.

---   
## Submodule(s)
The code uses BST Tools ([https://github.com/ManuelBerrueta/BST](https://github.com/ManuelBerrueta/BST)) as a submodule to do some functions that are already part of the code in those tools.

### After Initial clone: Initialize the  Submodule(s)
```Shell
git submodule update --init --recursive
```

## Make sure the Submodule is up to date
To make sure you have the latest submodules:
```Shell
git submodule update --recursive --remote
```
---    
## Python Requirements
You could skip setting up a virtual environment and just install the packages:
```Shell
pip install -r requirements.txt
```

---   
## urlyzer
**urlyzer** is a tool to analyze URLs. It will become very handy for looking at the response URLs from the token requests as well as analyzing the request URLs, as they both often contain multiple parameters. You can get it at [https://github.com/ManuelBerrueta/urlyzer](https://github.com/ManuelBerrueta/urlyzer).

---     
## Python Virtual Environment (Optional)
1. Create a Virtual Environment for the project:
```Shell
python3 -m venv flowAnalyzerEnv
```

2. Activate Your Virtual Environment: Type the following command and press Enter:
```shell
source flowAnalyzerEnv/bin/activate
```
> Now you're inside your virtual environment!

3. Install Packages: You can now use pip to install Python packages, and they'll only be installed in this virtual environment.
- In our cases we can use the `requirements.txt` I have provided:
```Shell
pip install -r requirements.txt
```
- We can verify they are installed by using:
```Shell
pip list
```

4. Exit Your Virtual Environment: Once you're done working on your project, you can exit the virtual environment by typing:
```Shell
deactivate
```    

---     
### Freezing requirements
If you end using other packages in your own development and testing, you can freeze those using:
```Shell
pip freeze > requirements.txt
```
