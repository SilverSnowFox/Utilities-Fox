# Chemistry Utilities Fox
 A discord bot with some basic chemistry functions such as element information, mass calculation and reaction balancing that utilizes chemlib
 
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

Calculates the mass and moles withe the information given.
The value's units can be in g, mg, mol, mmol. For example: ```c!MolarMass H2O 3g```.

### Quadratic Root Calculator
```c!Quadratic [a] [b] [c]```

Calculates the roots, whether real or imaginary, with the values a, b, c from a quadratic equation in the form ax² + bx + c = 0.

### Reaction Balancer
```c!Balance [reaction]```

Balances the inputted reaction.
The reaction must be in the form ```aA + bB -> cC + dD```. For example: ```C3H8 + 5O2 -> 3CO2 + 4H2O```.
