# Blast results parser

A simple script for processing the .xml results of the blast. 

## Getting started

Download sort_XML_results.py, make sure the file is executable. Example of the start:

`./sort_XML_results.py -in input.xml -o results`. 

### Output 

In the _/output_ you will find six .csv files:
 * archaea_dict.csv, mammalia_dict.csv, insecta_dict.csv, bacteria_dict.csv and others_dict.csv are files with _taxid;name_ structure. 
 There are located the detected species respectively. 
 * frequency_dictionary.csv with _name;frequency_value_ structure for each detected species. 

### Prerequisites

In addition to the standard libraries you will need _BioPython_ and _ete3_. 

To install them run `pip install biopython` and `pip install ete3`. 

### Notice please

For the first run script will download _taxdump.tar.gz_ from NCBI via FTTP and create a database, so Internet connection and additional time are required.
