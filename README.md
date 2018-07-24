# customTTbuilder
Hack to create your own custom time table (given the courses) from a pdf of a combined TimeTable

### Installations Rqd.
```
pip install Pillow
pip install pdfplumber
```

### To Run
```
python customttbuilder.py --pdfpath <TTpdf-path> --sublist <course-code1> <course-code2> <...> 
```
##### Example
```
python customttbuilder.py --pdfpath "TimeTable.pdf" --sublist ML AI CN IA Tcom EVS
```
![alt text](https://github.com/jainraghav/customTTbuilder/blob/master/example/example.jpg "Example")

