# Chemistry Utilities Fox
 A discord bot with some basic chemistry functions such as element information, mass calculation, reaction balancing that utilizes chemlib, and searching through the PubChem database.
 
## Commands
 Prefix: c!
 
### Help 
```c!Help```

Lists all the commands and their information.

### Element
```c!Element [symbol]```

Lists information about the element.

### Molar Mass
```c!MolarMass [formula] [values]```

Calculates the mass and moles with the information given.
The value's units can be in g, mg, mol, mmol. For example ```c!MolarMass H2O 3g```.

### Quadratic Root Calculator
```c!Quadratic [a] [b] [c]```

Calculates the roots, whether real or imaginary, with the values a, b, c from a quadratic equation in the form ax² + bx + c = 0.

### Reaction Balancer
```c!Balance [reaction]```

Balances the inputted reaction.
The reaction must be in the form ```aA + bB -> cC + dD```. For example ```C3H8 + 5O2 -> 3CO2 + 4H2O```.

### Search by Name
```c!Search [name]```

Searches for the compound with such name in the PubChem database and returns a list of the results.
Information returned includes: IUPAC name, CID, Molecular Weight and Molecular Formula

### Search by CID
```c!Info [CID]```

Searches for the compound with such CID in the PubChem database for a more details.
Information returned includes IUPAC name, Molecular Formula, Molecular Weight, Charge and an image of the Lewis Structure as a PNG.
