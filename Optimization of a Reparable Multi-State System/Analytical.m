A_leftup = -20.3*eye(100)+[zeros(1,100);[20*eye(99),zeros(99,1)]];
A_leftdown = 0.3*eye(100);
A_midup= 0.65*eye(100);
A_middown = -20.65*eye(100)+[zeros(1,100);[20*eye(99),zeros(99,1)]];
A_rightup = eye(100);
A_rightdown = -1*eye(100);
A = [[A_leftup;A_leftdown],[A_midup;A_middown],[A_rightup;A_rightdown]];
b = [-1.795;0.205*ones(99,1);1.795;-0.205*ones(99,1)];
Q = 2*eye(300);

Xa = inv(Q)*A'*inv(A*inv(Q)*A')*b;
figure(1)
plot(Xa(1:100)+0.9*ones(100,1));
figure(2)
plot(Xa(101:200)+0.1*ones(100,1));
figure(3)
plot(Xa(201:300));
1/2*Xa'*Q*Xa