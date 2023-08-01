# PK_ADME



## Getting started

Obtaining ADME Information From A List of Chemical Names on Python

## Project Description 
This code was created to obtain information about ADME (Absorption, Distribution, Metabolism, and Excretion) of chemical compounds. Starting with a list of chemical names we were able to obtain important information like Molecular Weight, Molecular Formula, and Canonical SMILES of chemicals using pubchempy (a python package). The Canonical SMILES for the list of chemicals were needed to move on to the next step of predicting chemical ADME using the SwissADME Database. 

Once the Canonical SMILES were obtained from pubchempy we moved on to automating the ADME prediction of chemicals using Selenium, a python package. Once this is complete href links are downloaded from SwissADME and can be viewed on python. 

## Installation
This script requires Firefox and Python 3 with the PubChemPy and Selenium packages installed. A suitable Conda environment may be created using the following command:
```
conda create -n swissadme firefox geckodriver pubchempy selenium
```

## Usage
The script takes an input list of chemical compounds (1 per line), downloads their SMILES notation from PubChem, and generates an accompanying TSV of SwissADME information for each of these compounds. Input lines beginning with the “#” symbol are ignored. Compounds lacking SMILES information will have “NA” returned for all SwissADME columns. The script can be run by calling it from the command line as follows:
```
python3 swissadme.py -i Chemicals_List.tsv -o SwissADME_Information.tsv
```

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

