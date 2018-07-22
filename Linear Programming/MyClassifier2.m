classdef MyClassifier2 < handle
    
    properties (Access = public)
        K                     % Number of classes
        N                     % Number of features
        W                     % Hyperplanes vectors
        w                     % Hyperplane biases
        
        
        % You can add any extra properties you would like
        
    end
    
        
    methods (Access = public)
        
        function obj = MyClassifier2(K,N)    % Class Constructor
            obj.K = K;
            obj.N = N;
            obj.W = [];
            obj.w = [];
            
            % You can initialize other properties that you added here
        end
        
        
        function obj = train(obj,trainData,trainLabel)
            
            %%% THIS IS WHERE YOU SHOULD WRITE YOUR TRAINING FUNCTION
            %
            % The inputs to this function are:
            %
            % obj: a reference to the classifier object.
            % trainData: a matrix of dimesions N x N_train, where N_train
            % is the number of inputs used for training. Each column is an
            % input vector.
            % trainLabel: a vector of length N_train. Each element is the
            % label for the corresponding input column vector in trainData.
            %
            % Make sure that your code sets the classifier parameters after
            % training. For example, your code should include a line that
            % looks like "obj.W = a" and "obj.W = b" for some variables "a"
            % and "b".
            for i=(1:obj.K)
                newTrainLabel = [];
                newTrainData = [];
                for index = (1:length(trainLabel))
                    if trainLabel(index)==i
                        newTrainLabel = [newTrainLabel;1];
                        newTrainData =  [newTrainData, trainData(:,index)];
                    else
                        newTrainLabel = [newTrainLabel;-1];
                        newTrainData =  [newTrainData, trainData(:,index)];
                    end 
                end
                [a,b] = SeparatingHyperplane(newTrainData', newTrainLabel);
                obj.W = [obj.W, [a;b]];
                obj.w = [obj.w, i];
            end
        end
        
        function [testResults] = classify(obj,testData)
            
            if (isempty(obj.W) || isempty(obj.w))
                error('Classifier is not trained yet.');
            end
            
            %%% THIS IS WHERE YOU SHOULD WRITE YOUR CLASSIFICATION FUNCTION
            %
            % The inputs to this function are:
            %
            % obj: a reference to the classifier object.
            % testData: a matrix of dimesions N x N_test, where N_test
            % is the number of inputs used for testing. Each column is an
            % input vector.
            %
            % The outputs of this function are:
            %
            % testResults: this should be a vector of length N_test,
            % containing the estimations of the classes of all the N_test
            % inputs.
            size_test = size(testData);
            size_W = size(obj.W);
            testData = [testData;ones(1,size_test(2))];
            num_of_points = size_test(2);
            num_of_hyperplanes = size_W(2);
            testResults = zeros(num_of_points,1);
            for index = (1:num_of_points)
                counts = zeros(1,10);
                for hyperplane = (1:num_of_hyperplanes)
                    counts(obj.w(hyperplane)) = (testData(:,index))'*obj.W(:,hyperplane);
                end
                [val, max_index] = max(counts);
                testResults(index) = max_index;
            end 
        end
     
    end
end
