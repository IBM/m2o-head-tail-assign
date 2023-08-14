# m2pCalculations (temporary name)

This project was developed using [m2p software](https://github.com/NREL/m2p) source code as a base to build a modified version that is able to perform polymerization of monomers assigning the head and tail of the polymers.

The original source-code was structured as the following: 

```
m2p
├── .github
    ├── workflows
        └── pypi_publish.yml
├── build
    ├── lib
        ├── m2p
            └── __init__.py
├── examples
    ├── Example for Creating Thermoplastic Structures.ipynb
    └── Example for Stereoenumerating Ester Monomers.ipynb
├── m2p
    ├── __init__.py
    ├── _version.py
    ├── monomers.py
    ├── polyestimator.py
    ├── polymaker.py
    ├── stereo_reactions.py
    └── utils.py
├── tests
    ├── test_monomers.py
    └── test_rxns.py
├── .gitattributes
├── .gitignore
├── travis.yml
├── Dockerfile
├── LICENSE
├── MANIFEST.in
├── README.md
├── __init__.py
├── environment.yml
├── requirements.txt
├── setup.cfg
├── setup.py
└── versioneer.py
```

The present modified source-code is structured as following (New* and Modified**):

```
m2pCalc
├── datasets*
    ├── monomers.original.csv
    ├── monomers.csv
    ├── output_monomers.csv
    ├── polymerization_output.csv
    └── polymerization.csv
├── examples
    ├── performance.ipynb*
    ├── polymerization.ipynb*
    └── separation-polymerization.ipynb*
├── m2pCalc
    ├── __init__.py
    ├── data.py*
    ├── monomers.py
    ├── performance.py*
    ├── polyestimator.py
    ├── polymaker.py**
    ├── stereo_reactions.py
    └── utils.py
├── tests
    ├── test_monomers.py
    └── test_rxns.py
├── .gitignore**
├── LICENSE**
├── README.md**
├── __init__.py**
├── environment.yml
├── requirements.txt
└── setup.py**
```


## Documentation

### **Installation**

* Download the code file to your desired directory and unzip it


### **Running the script**

* To polymerize: The [polymerization.ipynb](polymerization.ipynb) file has all the steps needed to run the code.

    *By default, head and tail option is False. To enable add head_tail=True to Polymaker class and to thermoplastic function.*

* To polymerize homopolymers and copolymers separately: The [separation-polymerization.ipynb](polymerization.ipynb) file has all the steps needed to run the code.

    *By default, head and tail option is False. To enable add head_tail=True to Polymaker class and to thermoplastic function.*

* To verify results: The [performance.ipynb](performance.ipynb) file has all the steps needed to calculte perfomance, validate and verify all remaining data that was not calculated.

**More information about the functions can be found at the m2pCalc directory**

---
## Authorship


* Author: **Brenda Ferrari** ([bferrari](https://github.ibm.com/bferrari))
* Co-author: **Ronaldo Giro** ([rgiro](https://github.ibm.com/rgiro))
* Co-author: **Mathias Steiner** ([mathiast](https://github.ibm.com/mathiast))