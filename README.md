# VES++
### The language for everybody, yet nobody
I love to learn new languages. My inspiration for this program language is therefore based on my hobby. VES++ has included the most common languages from west-europe (and for some random reason I have added the turkish language).
This way many people are able to understand a part of the code, yet (probably) not everything. In my opinion it is a fun way to get involved with other languages!

### Chosen extra features
- [Error-messaging](https://github.com/vera98x/Interpreter/blob/master/README.md#errorhandling)
- [Advanced language features](https://github.com/vera98x/Interpreter/blob/master/README.md#Advanced-language-features)
- Creating my own language
- [Instruction-and-show-off video](https://github.com/vera98x/Interpreter/blob/master/README.md#link-to-instruction-video)


#### Translation table
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

#### Symbol table
|Symbol | Usage
|---|---|
|$ | Line starting with '$' are comment lines |
|# | This character ends the print-statement |
|@| Every variable starts with an @ | 
| > | Greater than  | 
| >= | Greater than or equal to  | 
| < | Smaller than | 
| <= | Smaller than or equal to | 

## Use of operators
### Math
```
<value> <math-keyword> <value>
```

### Assigning variable
```
@<variable name> er <value/statement> fin
```
	
### If-statement
```
ef haakje_begin <condition> haakje_eind fa_inizio
	<things you want to do>
fa_fine
```
		
### While-loop
```
aika haakje_begin <condition> haakje_eind fa_inizio
	<things you want to do>
fa_fine
```
	
### Printing
```
taispeain 
	<thing to print> fin
	<thing to print> fin
	... 
#
```

## Error-messaging
Ves++ is included with errormessaging. When an error occurs, it shows the errormessage and the line the error has occurred on for debug purposes. An error will be given for the following issues:
- Unknown symbol, such as '=' '&' 'abcd'
- Syntax errors
- Undefined variables
- Assignment to a non-variable, such as: 8 er 5 mas 5 fin
- Division by zero

## Advanced language features
- Calutations can be made with the plus-, min-, multiply- and divide operator. These calculations are according the math rules
- Print statement: you can print multiple variables or expressions
- Comment lines are integrated. Lines starting with '$' are comment lines

## Used high order functions 
The interpreter uses the following high order functions:
- Foldl
- Zip
- Filter
- Map

## Inheritance 
The interpreter has one inheritance, this is for the Node class. This class has two childs: operator_node and value_node


## Examples
Below are examples shown of the VES++ code. 

### Printing statements
```
taispeain 
	2 mas 2 fin
	5 vezes 5 fin
#	
```
Result:
```
4.0
25.0
```

### Math rules
```
taispeain 
	2 mas 2 vezes 5 eksi 4 fin
#
```
Result: 
```
8
```

### Assigning variables
```
$ @test is a variabele
@ATP er 30 fin
@test er @ATP fin
@ATP er 20 fin
taispeain
	@ATP fin
	@test fin
#
```
Result:
```
20.0
30.0
```

### If-statement in If-statement
```
$if-statement in if statement
@vera er 21 fin
ef haakje_begin 2 < 3 haakje_eind fa_inizio
	ef haakje_begin @vera > 18 haakje_eind fa_inizio
		taispeain
			1 fin
		#
	fa_fine
	ef haakje_begin @vera <= 18 haakje_eind fa_inizio
		taispeain
			0 fin
		#
	fa_fine
fa_fine
```
Result:
```1.0```

### If-statement in While-loop

```
$while and if
@ATP er 10 fin
@counter er 0 fin
aika haakje_begin @ATP > 0 haakje_eind fa_inizio
	@ATP er @ATP eksi 1 fin
	ef haakje_begin @ATP >= 5 haakje_eind fa_inizio
		@counter er @counter mas 1 fin
	fa_fine
fa_fine

taispeain
	@ATP fin
	@counter fin
#
```
Result:
```
0.0
5.0
```

### Combining the statements in ves++
```
@ATP er 8 fin
@test er 0 fin
aika haakje_begin @ATP > 2 haakje_eind fa_inizio
	ef haakje_begin @ATP dela 2 lig 3 haakje_eind fa_inizio
		@test er @test mas 1 fin
	fa_fine
	@ATP er @ATP eksi 1 fin
fa_fine
ef haakje_begin @ATP > 0 haakje_eind fa_inizio
   @geslaagd er 1 fin
fa_fine

taispeain
	@ATP fin
	@test fin
	@geslaagd fin
#
```
Result:
```
2.0
1.0
1.0
```

