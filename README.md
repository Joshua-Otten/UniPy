# UniPy Demo (using React-Express)

## Project Overview

This repo contains a demo of our UniPy application.  (Note that the most recent version resides in the "multilingual" branch.)  Currently, it allows a user to type Python code in either editor box and translate across 6 different languages (including English).  Languages can be flipped by using the "swap" feature.  Two output boxes below display the corresponding output after an Execution button is clicked.  

## File Layout

In the main directory, you can find components for the backend, UniPy files, node modules, etc.  The "code1" and "code2" files are for storing the multilingual code to be executed, and the "LanguageData" folder stores lists of data for the supported languages.  In "client", you can find more files and folders relating to the frontend.  Specifically, "src" contains the frontend code.

## Running this Project Locally

Make sure you have [Node.js](http://nodejs.org/).

*Note the following commands assume a Unix-based enviornment. If you are on windows, you may need to use something such as Windows Subsystem for Linux (https://docs.microsoft.com/en-us/windows/wsl/about).*

```sh
$ git clone <repo-name>
$ cd <repo-name>
$ npm install
$ npm run setup
$ npm start
```

After executing these commands, the express backend and React frontend should now be running on [localhost:3000](http://localhost:3000/). You can visit this page in your web browser to view the demo user interface.
