# customTTbuilder
Hack to create your own custom time table (given the courses) from a pdf of a combined TimeTable

### Installations Rqd.
```
pip install Pillow
pip install pdfplumber
```
#### For mac users
```
brew install imagemagick@6
ln -s /usr/local/Cellar/imagemagick@6/<your specific 6 version>/lib/libMagickWand-6.Q16.dylib /usr/local/lib/libMagickWand.dylib
pip install pdfplumber
```
### To Run
```
python customttbuilder.py --pdfpath <TTpdf-path> --sublist <course-code1> <course-code2> <...> 
```
##### Example
```
python customttbuilder.py --pdfpath "example/TimeTable.pdf" --sublist ML AI CN IA Tcom EVS
```
![alt text](https://github.com/jainraghav/customTTbuilder/blob/master/example/example.jpg "Example")

