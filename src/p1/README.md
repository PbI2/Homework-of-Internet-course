---
title: README
---

# The Calculator Instructions
After you are successfully connected, the calculator will ask ```Welcome to the calculator server. Input your problem ?```
You may response with one of the keywords:
1. ```{a number} {an operator} {a number}``` 
See **Basic arithmetics** for more details
2. ```matrix```
See **Matrix calculation** for more details
## Basic arithmetics
- The format is ```{a number} {an operator} {a number}```
- Ex:```5 * 3```  , ```6 + 8```...
- The operator choices = ```+``` ```-``` ```*``` ```/```
- There is a space between the number and the operator
- The answer will be printed after you send the response
## Matrix calculation
- You must send ```matrix``` for the first question
- Then the calcular will ask:
```
Please input the code to choose the mode:
det mul adj inv power
``` 
- You may response the mode with:
  - ``det`` for the determinant of a matrix
  - ``mul`` for matrix multipling 
  - ``adj`` for the adjugate matrix of a matrix
  - ``inv`` for the inverse of a matrix
  - ``power`` for calculating the power of a matrix
- Then the calcular will ask```Please input the problem```
- The response has a different format for different modes

### ```det```, ```adj```, ```inv``` mode
- for these modes, what you should response is a matrix, and the calculator can return a number (``det``) or a matrix (``adj``,``inv``) answer 
- How to key in a matrix
  * ``[[1,2],[3,4]]`` represents the matrix
  $$\begin{bmatrix}
    1 & 2\\
    3 & 4\\
  \end{bmatrix}$$
  * ```[[0,1,2],[3,4,5],[6,7,8]]``` represents the matrix　
 $$\begin{bmatrix}
    0 & 1 & 2\\
    3 & 4 & 5\\
    6 & 7 & 8\\
  \end{bmatrix}$$
  * It's not neccessay to add any space

- Some unsupported conditions:
  - ```det```, ```adj```, ```inv``` can only deal with the square matrix
  - ``inv`` can't deal with matrix $M$ with $\det(M)=0$
  - ``adj``,``inv``can't deal with 1x1 matrix

### ``mul``
- ``{matrix A} * {matrix B}``
- It's both feasible whether you enter the space between the matrix and * or not
- Returns the matrix $A \times B$

### ``power``
- ``{matrix} ** {n(a positive integer)}``
- Can only deal with the square matrix
- It's both feasible whether you enter the space between the matrix and ** or not
- Returns the matrix $A^n$

