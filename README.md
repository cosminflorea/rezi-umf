# Parse and display tables for Residency Medicine Faculty of Romania

## Description

This project written in Streamlit and Python is created to help medicine students to visualize and filter data( domain,
specialities and availabe places) for their residency. The data is parsed from .pdf privided by Ministery of Health on 
website [Rezidentiat.ms.ro](https://rezidentiat.ms.ro/).

## Dependencies
### packages
1. python 3.7
2. streamlit
3. pandas
4. camelot
5. unidecode 
6. altair

### how-to install packages

```Bash
python -m pip install <package>
```

## How to use 

The usage is very simple: Select from sidebar desired option to display data. Some of options are implemented using 
multiselector to compare different data. 

## Heroku dependencies
### buildpacks
1.heroku/python
2.https://github.com/heroku/heroku-buildpack-apt
