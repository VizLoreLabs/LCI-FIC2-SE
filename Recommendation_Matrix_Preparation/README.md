#LCI-FIC2-SE-Recommendation-Matrix-Prep
Source code for Recommendation Matrix Preparation module of the Context Aware recommendation SE

To use this module, one have to install Python 2.7 or bigger and Django. 
Django installation guide: https://docs.djangoproject.com/en/1.7/topics/install/

The main variable in this module is lookup_table defined in conrec/toolbox.py. Table is self explanatory, it can be changed if you have some other context data available. 

Please take care, that the links in the code are hardcoded to our production server. The best practise is to run your start your own server localy and test it on your machine, where you have full acces to all data required. And generaly this access, disable the oportunity to break someones server. 
