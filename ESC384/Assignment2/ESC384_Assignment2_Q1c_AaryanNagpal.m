%ESC384 Assignment 2, Aaryan Nagpal, 1007792596, nagpalaa

%Question 1c - Checking if series summation is equal to analytical
%calculation
syms k
series = symsum(1/((2*k-1)^2),k,1,Inf);
display(series)
sum = pi^2/8;
tf = isequal(series, sum);
display(tf)

%since the output is logical 0 or true, it can be confirmed!