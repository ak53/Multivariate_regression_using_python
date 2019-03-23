PROBLEM STATEMENT:
To find a combination of input values that gives minimum Mean Absolute error and minimum Mean Squared error.

FILE DESCRIPTIONS:
1) found.txt
	draw data containing impact factors anf journals
2) README.txt
3) output.csv
	displays all combinations along with their Mean Absolute errors and Mean Squared errors
4) scimagojr 2017 Subject Area - Computer Science.txt
	contains raw data of journals extracted from Scimago.com
5) script.py
	contains the code


SOLUTION
The code uses all combinations possible of the available input values on 80%(training) data and calculates coefficients using 
x=[{A(t)A^-1}A(t)](training_y)
Then the code uses these coefficients on 20%(testing) data to calculate error.
Using these errors (absolute and squared) we find the best combination i.e. combination that has minimum mean absolute error and minimum mean squared error


DEPENDENCIES
The code requires:
	numpy
	csv module
	itertools
	itemgetter from operator module