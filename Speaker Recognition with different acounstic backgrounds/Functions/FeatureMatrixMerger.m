function featureMatrix = FeatureMatrixMerger(featureCellClean,featureCellBabble,myFiles)
    featureMatrix = containers.Map;
    for i = 1 : length(myFiles)
        S = regexp(myFiles{i},'\','split');
        
        fileName = S{3};
        fileName = [fileName(1:end-3),'wav'];
        
        if isempty(strfind(myFiles{i},'Clean')) == false
            featureMatrix(myFiles{i}) = featureCellClean(fileName);
        
        elseif isempty(strfind(myFiles{i},'Babble')) == false
            featureMatrix(myFiles{i}) = featureCellBabble(fileName);
            
        else
            error('FeatureMatrixMerger Error !!\n')
        end
        
    end
    save('featureMatrix.mat','featureMatrix')

end
