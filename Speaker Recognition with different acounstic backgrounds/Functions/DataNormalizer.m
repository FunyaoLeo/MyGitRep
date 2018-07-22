function [feature_map] = DataNormalizer(feature_map, num_features,norm_para)
    % Normalize the data by y = a x + b
    fileNames = feature_map.keys;
    
    for index = (1:length(fileNames))
        X = feature_map(fileNames{index});
        X(isnan(X)) = 0;
        for column =(1:num_features)
            X(:, column) = X(:, column)*norm_para(1,column)+norm_para(2, column);
        end
        feature_map(fileNames{index}) = X;
    end
end