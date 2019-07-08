# Taxon finder and blast results parser

A simple script for processing the .xml results of the blast. 
It also can find taxons that you mention.

## Getting started

Download _taxon_finder.py_, make sure the file is executable. Example of the start:

`./find_taxon.py --input_taxon taxon.txt --input_xml results.xml --output /res`

This will find all taxons, that are mentioned in _taxon.txt_, example of _taxon.txt_:
```
Phyllobacterium zundukense
Hoplopleura emphereia
Pedicinus badii
Taharana
Bicyclus
```

File _results.xml_ is your blast result. 

Argument `--input_reads` is not required, because it is not supported yet. 
If you mention it, nothing happens. 

### Output 

In the _/output_ you will find six .csv files:
 * archaea_dict.csv, mammalia_dict.csv, insecta_dict.csv, bacteria_dict.csv 
 and others_dict.csv are files with _taxid;name_ structure. 
 There are located the detected species respectively. 
 * frequency_dictionary.csv with _name;frequency_value_ structure for each detected species. 
 * taxons_found.csv with _input_taxon;results_species;query_ structure.

### Prerequisites

In addition to the standard libraries you will need _BioPython_ and _ete3_. 

To install them run `pip install biopython` and `pip install ete3`. 

## Notice please

For the first run script will download _taxdump.tar.gz_ from NCBI via HTTP and create a database,
 so Internet connection and additional time are required. Do not delete _ncbi_db.log_, otherwise script will 
 download and parse database again. _ncbi_db.log_ contains only one row with the date of installation, 
 it seems to be useful to update database sometimes. To update the database, delete the log-file. 
