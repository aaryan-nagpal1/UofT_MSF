clc
clear all
format short

% Program Start
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% PART 1: Data pre-processing 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Load the sample historical data
load('lab2data.mat')

% Calculate the asset and factor returns (factor models use returns, not
% prices)
rets    = prices( 2:end, : ) ./ prices( 1:end - 1, : ) - 1;
facRets = sp500price( 2:end , 1 ) ./ sp500price( 1:end - 1, 1 ) - 1;

% Number of assets
n = size(rets,2);

% Number of observations;
N = size(rets, 1);

% Calculate the factor expected excess return from historical data using
% the geometric mean
mu = (geomean(rets + 1) - 1)';

% Calculate the asset covariance matrix
Q = cov(rets);

% Calculate the factor expected excess return from historical data using
% the geometric mean. Use this as the portfolio target return
targetRet = geomean(facRets + 1) - 1;

theta = ((1/N)*diag(Q).*eye(n)).^0.5;
alpha = 0.9;
epsilon = sqrt(chi2inv(alpha,n));
lambda = 20;
%use fmincon
fun = @(x) lambda*transpose(x)*Q*x - (transpose(mu)*x-epsilon*norm(theta*x,2));
x0 = 1/n.*(ones(n,1));

A = [];
b = [];
Aeq = ones(1,n);
beq = 1;
lb = zeros(n,1);
ub = [];
x = fmincon(fun,x0,A,b,Aeq,beq,lb, ub);
x
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Program End


