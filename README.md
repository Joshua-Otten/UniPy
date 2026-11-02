# UniPy Demo (using React-Express)

## Project Overview

This repo contains a demo of our UniPy application.  Currently, it allows a user to type Python code in either editor box and translate across 9 different languages (including English).  Languages can be flipped by using the "swap" feature.  Two output boxes below display the corresponding output after an Execution button is clicked.  

## Prerequisites

- [Node.js](http://nodejs.org/) (v16 or newer recommended)
- [Python 3](https://www.python.org/) (v3.10 or newer)
- pip3

## File Layout

In the main directory, you can find components for the backend, UniPy files, node modules, etc.  The "code1" and "code2" files are for storing the multilingual code to be executed, and the "LanguageData" folder stores lists of data for the supported languages.  In "client", you can find more files and folders relating to the frontend.  Specifically, "src" contains the frontend code.

## Running this Project Locally

*Note the following commands assume a Unix-based enviornment. If you are on Windows, you may need to use something such as Windows Subsystem for Linux (https://docs.microsoft.com/en-us/windows/wsl/about).*

```sh
git clone <repo-name>
cd <repo-name>
npm install
npm run setup
npm start
```

`npm run setup` will automatically install both the Node and Python dependencies (including `googletrans`). After running `npm start`, the Express backend and React frontend will be available at [localhost:3000](http://localhost:3000/).

## Citation / Academic Attribution

UniPy was developed as part of academic research on universal Python and multilingual programming accessibility.

If you use this repository in academic work, derivative research, publications, commercial / production systems, or systems inspired by this implementation, please cite the UniPy paper. If your work specifically uses or builds on the translations or theoretic concepts introduced in the follow-up paper, please cite the arXiv preprint as well.

### UniPy Paper
@inproceedings{otten2023towards,
  title={Towards a Universal Python: Translating the Natural Modality of Python into Other Human Languages},
  author={Otten, Joshua and Anastasopoulos, Antonios and Moran, Kevin},
  booktitle={2023 IEEE International Conference on Software Maintenance and Evolution (ICSME)},
  pages={352--357},
  year={2023},
  organization={IEEE}
}

### Follow-up Paper
@article{otten2025automated,
  title={Automated Python Translation},
  author={Otten, Joshua and Anastasopoulos, Antonios and Moran, Kevin},
  journal={arXiv preprint arXiv:2504.11290},
  year={2025}
}

## License

Copyright 2023 Joshua Otten

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
