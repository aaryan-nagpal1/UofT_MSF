%Assignment 1 - Aaryan Nagpal, 1007792596, nagpalaa

%Question 4b - Plot for fourier cosine series approximations

%Define function, fourier cosine series x bounds, sum
x_val = linspace(-1,2,1000);
f = @(x_val) x_val.^2;
f_3_sum = 0;
f_30_sum = 0;
f_300_sum = 0;

%Initializing vector to hold fourier series value for n'th term
%(N=3,30,300)
N_1 = 3;
N_2 = 30;
N_3 = 300;
f_n_3 = zeros(1,length(x_val));
f_n_30 = zeros(1,length(x_val));
f_n_300 = zeros(1,length(x_val));

%Setting up truncated series to different N values
for n = 1:N_1
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_3 = f_n*cos(n*pi*x_val);
    f_3_sum = f_3_sum + f_3;
end

for n = 1:N_2
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_30 = f_n*cos(n*pi*x_val);
    f_30_sum = f_30_sum + f_30;
end

for n = 1:N_3
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_300 = f_n*cos(n*pi*x_val);
    f_300_sum = f_300_sum + f_300;
end

f_n_3  = 1/3+f_n_3+f_3_sum;
f_n_30  = 1/3+f_n_30+f_30_sum;
f_n_300  = 1/3+f_n_300+f_300_sum;

%Plotting and labelling
plot(x_val, f_n_3,'-g', LineWidth=0.5);
hold on
plot(x_val, f_n_30,'-r', LineWidth=0.5);
plot(x_val, f_n_300,'-b', LineWidth=0.5);
plot(x_val, f(x_val),'-m', LineWidth=0.5);
hold off
xlabel('x values');
ylabel('Function Value');
title('Fourier Cosine Series Approximations of f(x) = x^2');
legend('N=3', 'N=30', 'N=300', 'f(x) = x^2', 'Location', 'best');

%% 

%Question 4 - part d (Fourier cosine pointwise error truncated)
% x = 0.5

%Define function, fourier cosine series x bounds, sum
f = @(x) x^2;
f_3_sum_x = 0;
f_30_sum_x = 0;
f_300_sum_x = 0;

%Initializing vector to hold fourier series value for n'th term
%(N=3,30,300)
N_1 = 3;
N_2 = 30;
N_3 = 300;
f_n_3_x = zeros(1,1);
f_n_30_x = zeros(1,1);
f_n_300_x = zeros(1,1);

%Setting up truncated series to different N values
x=0.5;
for n = 1:N_1
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_3_x = f_n*cos(n*pi*x);
    f_3_sum_x = f_3_sum_x + f_3_x;
end

for n = 1:N_2
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_30_x = f_n*cos(n*pi*x);
    f_30_sum_x = f_30_sum_x + f_30_x;
end

for n = 1:N_3
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_300_x = f_n*cos(n*pi*x);
    f_300_sum_x = f_300_sum_x + f_300_x;
end

f_n_3_x  = 1/3+f_n_3_x+f_3_sum_x;
f_n_30_x  = 1/3+f_n_30_x+f_30_sum_x;
f_n_300_x  = 1/3+f_n_300_x+f_300_sum_x;

%Error calculation for N=3,30,300 at x=0.5
%N=3
error_3_cos_x05 = abs(f(x)-f_n_3_x);
%N=30
error_30_cos_x05 = abs(f(x)-f_n_30_x);
%N=300
error_300_cos_x05 = abs(f(x)-f_n_300_x);


%% 

% x = 0.9

%Define function, fourier cosine series x bounds, sum
f = @(x) x^2;
f_3_sum_x = 0;
f_30_sum_x = 0;
f_300_sum_x = 0;

%Initializing vector to hold fourier series value for n'th term
%(N=3,30,300)
N_1 = 3;
N_2 = 30;
N_3 = 300;
f_n_3_x = zeros(1,1);
f_n_30_x = zeros(1,1);
f_n_300_x = zeros(1,1);

%Setting up truncated series to different N values
x=0.9;
for n = 1:N_1
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_3_x = f_n*cos(n*pi*x);
    f_3_sum_x = f_3_sum_x + f_3_x;
end

for n = 1:N_2
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_30_x = f_n*cos(n*pi*x);
    f_30_sum_x = f_30_sum_x + f_30_x;
end

for n = 1:N_3
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_300_x = f_n*cos(n*pi*x);
    f_300_sum_x = f_300_sum_x + f_300_x;
end

f_n_3_x  = 1/3+f_n_3_x+f_3_sum_x;
f_n_30_x  = 1/3+f_n_30_x+f_30_sum_x;
f_n_300_x  = 1/3+f_n_300_x+f_300_sum_x;

%Error calculation for N=3,30,300 at x=0.9
%N=3
error_3_cos_x09 = abs(f(x)-f_n_3_x);
%N=30
error_30_cos_x09 = abs(f(x)-f_n_30_x);
%N=300
error_300_cos_x09 = abs(f(x)-f_n_300_x);

%% 

%Question 4 - part e - Max error on x=[0,1] interval for Fourier cosine
%series approximation

%Define function, fourier cosine series x bounds, sum
x_val_2 = linspace(0,1,1000);
f = @(x_val_2) x_val_2.^2;
f_3_sum = 0;
f_30_sum = 0;
f_300_sum = 0;

%Initializing vector to hold fourier series value for n'th term
N_1 = 3;
N_2 = 30;
N_3 = 300;
f_n_3 = zeros(1,length(x_val_2));
f_n_30 = zeros(1,length(x_val_2));
f_n_300 = zeros(1,length(x_val_2));

%Setting up truncated series to different N values
for n = 1:N_1
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_3 = f_n*cos(n*pi*x_val_2);
    f_3_sum = f_3_sum + f_3;
end

for n = 1:N_2
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_30 = f_n*cos(n*pi*x_val_2);
    f_30_sum = f_30_sum + f_30;
end

for n = 1:N_3
    f_n = (4*(-1)^n)/(n^2*pi^2);
    f_300 = f_n*cos(n*pi*x_val_2);
    f_300_sum = f_300_sum + f_300;
end

f_n_3  = 1/3+f_n_3+f_3_sum;
f_n_30  = 1/3+f_n_30+f_30_sum;
f_n_300  = 1/3+f_n_300+f_300_sum;

%Truncated max error

%N=3
max_error_3 = max(abs(f(x_val_2)-f_n_3));
%N=30
max_error_30 = max(abs(f(x_val_2)-f_n_30));
%N=300
max_error_300 = max(abs(f(x_val_2)-f_n_300));