clc;
clear all;

%%%% load data %%%%

%load MNIST_Train.mat
load MNIST_Train.mat;
S_Train = S_Train+1;
%load MNIST_Test.mat
load MNIST_Test.mat;
S_Test = S_Test+1;

%%%% dimension reduction %%%%
%{
Y_Train_set = [];
for index = 1:20000
    a = Y_Train(:,index);
    Y_Train_Image = [];
    for i = 0:9
        for j = 0:9
            avg = (a(40*i+j*2+1)+a(40*i+(j+1)*2)+a(40*i+20+j*2+1)+a(40*i+20+(j+1)*2))/4.0;
            Y_Train_Image = [Y_Train_Image;avg];
        end
    end
    Y_Train_set = [Y_Train_set, Y_Train_Image];
end
Y_Train = Y_Train_set;

Y_Test_set = [];
for index = 1:10000
    a = Y_Test(:,index);
    Y_Test_Image = [];
    for i = 0:9
        for j = 0:9
            avg = (a(40*i+j*2+1)+a(40*i+(j+1)*2)+a(40*i+20+j*2+1)+a(40*i+20+(j+1)*2))/4.0;
            Y_Test_Image = [Y_Test_Image;avg];
        end
    end
    Y_Test_set = [Y_Test_set, Y_Test_Image];
end
Y_Test = Y_Test_set;
%}

%creating two classifiers
obj1 = MyClassifier1(10, 100)
obj2 = MyClassifier2(10, 100)

%%%% 10 fold cross validation %%%%
%{
%%%%%%%%%%%%%%%%cross-validation start%%%%%%%%%%%%%%%%%%%%%%
%create two vectors to contain precision
precision1 = [];
precision2 = [];
validation = [1:10];
for i = (0:9)
    obj1 = obj1.train(Y_Train(:,1+1000*i:1000*(i+1)), S_Train(1+1000*i:1000*(i+1)));
    obj2 = obj2.train(Y_Train(:,1+1000*i:1000*(i+1)), S_Train(1+1000*i:1000*(i+1)));
    
    [testResults1] = obj1.classify(Y_Train(:,[1:1000*i,1000*(i+1)+1:10000]));
    [testResults2] = obj2.classify(Y_Train(:,[1:1000*i,1000*(i+1)+1:10000]));
    
    hit1 = 0;
    hit2 = 0;
    corrections1 = testResults1-S_Train([1:1000*i,1000*(i+1)+1:10000]);
    corrections2 = testResults2-S_Train([1:1000*i,1000*(i+1)+1:10000]);
    for index = (1:length(testResults1))
        if corrections1(index) == 0
            hit1 = hit1+1;
        end
        if corrections2(index) == 0
            hit2 = hit2+1;
        end
    end
    precision1 = [precision1, hit1];
    precision2 = [precision2, hit2];
end

plot(validation, precision1*1.0/9000);
hold on;
plot(validation, precision2*1.0/9000);
hold off;
legend('ovo', 'ovr');
%}

%train and classify
obj1 = obj1.train(Y_Train(:,1:6000), S_Train(1:6000));
obj2 = obj2.train(Y_Train(:,1:6000), S_Train(1:6000));
[testResults1] = obj1.classify(Y_Test);
[testResults2] = obj2.classify(Y_Test);
hit1 = 0;
hit2 = 0;
corrections1 = testResults1-S_Test;
corrections2 = testResults2-S_Test;
for index = (1:length(testResults2))
    if corrections1(index) == 0
        hit1 = hit1+1;
    end
    if corrections2(index) == 0
        hit2 = hit2+1;
    end
end











