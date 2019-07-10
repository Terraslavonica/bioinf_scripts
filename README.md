# Bioinformatics scripts

Here you can find some scripts, that were written to solve certain problems, which revealed themselves during our research. 
It's better to warn in advance that these programs are not general-purpose, most of them were written in order to adapt to 
the situatuion, not to the algorithm. Sometimes input and output are weired, so pay attention to __README__, if you dare to 
use them. 

## Table of content

* __taxon_finder__ is a script that allows to extract some information about your blast result, if it's given in _.xml_
extension. You can sort out species or find taxons. More information is given in __/taxon_finder/README__. 

* __kraken_to_krona.py__ is a script that allows to pull out the information about the query and taxid from
[Kraken2](https://github.com/DerrickWood/kraken2) results. At this moment _#score_ is equal to _1_ by default.

* __xml_split.py__ allows to split your blast results into several parts. We had to do it, because our blast result
was too big to use it in [Megan](https://github.com/danielhuson/megan-ce) with our computational resources. 

## Getting started with:
* __kraken_to_krona.py__
    
    Example of the start:
    
    `./kraken_to_krona.py -i /file.fastq -o /output_dir`
    
    The result will be in __/output_dir/out.tsv__. It has _#query #taxID #score_ structure to be suitable for use with 
    [Krona](https://github.com/marbl/Krona/). 
    
    Being used with 122 Mb file, it showed _real 0m3.651s; user 0m3.178s; sys 0m0.472s_. 
    
* __xml_split.py__

    Example of the start:
    
    `./xml_split.py -i /file.xml -n 2 -o /output_dir`
    
    An argument `-n` shows the number of parts the file needs to be divided into. 
    
    The results will be in __output_dir/*.xml__. 
    
    Being used with 2.7 Gb file, it showed _real 11m33.394s; user 7m36.722s; sys 3m44.815s_. 
    
    Notice, that output files contain only the _`<Iteration> .. </Iteration>`_ blocks. 
    
### P.S.:

I hope some day this all will become more structured and complicated. But not today `:-)`
    
    
