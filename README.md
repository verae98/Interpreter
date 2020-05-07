# Ves++
### The language for everybody, yet nobody
This language has included the most common languages from west-europe (and for some random reason I have added the turkish language).
This way many understands a part of the code, yet (probably) not everything. In my opinion it is a fun way to get involved with other languages!

Translation table
|Type| Word in this language | Language where it comes from
|---|---|---|
|Plus operator | mas | Spanish|
|Minus operator | eksi | Turkish | 
|Multiply operator | vezes | Portugese |
|Division operator| dela | Swedish |
| Assignment | er | Norwegian |
| If | ef | Icelandic |
| Else | annars | Icelandic | 
| While | aika | Finnish | 
| Equal operator | lig | Danish | 
| Not equal operator | unterschiedlich | German | 
| Terminate character (;) | fin | French | 
| Left parenthesis | haakje_begin | Dutch | 
| Right parenthesis | haakje_eind | Dutch | 
| Left bracet | fa_inizio | Italian | 
| Right bracet | fa_fine | Italian | 
| Print statement | taispeain | Irish | 

## Errorhandling
Ves++ has a small error handling included. When an error occurs, it show the errormessage and the line the error has occurred for debug purposes. An error will be given for the following issues:
- Unknown symbol
- Syntax error with for example two numbers after each other without operator between them
- Variables that have not been defined

## Features
- Calutations can be made with the plus, min multyply and divide operator. These calculations are according the math rules
- Print statement: you can print variables or expressions
- Comment lines are integrated. Lines with '$' before it are comment lines

## Used high order functions 
The interpreter is using the following high order functions:
- Foldl
- Zip
- Filter

## Inheritance 
The interpreter has one inheritance, this is for the Node class. This class has two childs: operator_node and value_node

## Link to instruction video


## Example
Below is shown an example of the ves++ code. 

#### Code in ves++
```
vera er 8 fin
test er 0 fin
aika haakje_begin vera > 2 haakje_eind fa_inizio
	ef haakje_begin vera dela 2 lig 3 haakje_eind fa_inizio
		test er test mas 1 fin
	fa_fine
	vera er vera eksi 1 fin
fa_fine
ef haakje_begin vera > 0 haakje_eind fa_inizio
   geslaagd er 1 fin
fa_fine
```


