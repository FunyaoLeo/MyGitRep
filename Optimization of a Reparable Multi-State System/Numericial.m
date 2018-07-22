A_leftup = -20.3*eye(100)+[zeros(1,100);[20*eye(99),zeros(99,1)]];
A_leftdown = 0.3*eye(100);
A_midup= 0.65*eye(100);
A_middown = -20.65*eye(100)+[zeros(1,100);[20*eye(99),zeros(99,1)]];
A_rightup = eye(100);
A_rightdown = -1*eye(100);
A = [[A_leftup;A_leftdown],[A_midup;A_middown],[A_rightup;A_rightdown]];
b = [-1.795;0.205*ones(99,1);1.795;-0.205*ones(99,1)];
Q = 2*eye(300);

X1 = 0.5*ones(300,1);
lamda1 = 0.5*ones(200,1);
X0 = zeros(300,1);
lamda0 = zeros(200,1);
n=0;

while(norm(lamda1-lamda0)>0.00001||norm(X1-X0)>0.00001)
    X0 = X1;
    lamda0 = lamda1;
    X1 = X0 - 0.001*(Q*X0+A'*lamda0);
    lamda1 = lamda0 + 0.001*(A*X0-b);
    n = n+1;
end

figure(1)
plot(X1(1:100)+0.9*ones(100,1));
figure(2)
plot(X1(101:200)+0.1*ones(100,1));
figure(3)
plot(X1(201:300));
1/2*X1'*Q*X1



