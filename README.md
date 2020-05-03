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

## Errorhandling

## Features

## Used high order functions 

## Inheritance 

## Link to instruction video


## Example
Below is shown an example of the ves++ code. This has been translated to pseudo code (based on c++) to give an impression of how the code works 

### Code in ves++
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

### Translation of the code 
```
vera = 8 ;
test = 0 ;
while ( vera > 2 ) {
	if ( vera / 2 == 3 ) {
		test = test + 1 ;
	} 
	vera = vera - 1 ;
}
if ( vera > 0 ) {
   geslaagd = 1 ;
}
```


