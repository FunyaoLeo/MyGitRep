function [featureCell ,columnTitle]= ReadFeatures( inputFile, outputDirectory,savefile)
% inputFile : path to .xlsx spreadsheet
% outputDirectory : path to output folder
    featureCell = containers.Map;
    disp(['Reading ', inputFile,' ...']);
    [~,~,raw] = xlsread( inputFile );
    columnTitle = {};
    for i = 5:size(raw,2)
        columnTitle = [columnTitle raw{1,i}];
    end
    mkdir( [outputDirectory,'/MAT']);
    outputDirectory = [outputDirectory,'/MAT'];
    display('Parsing Data...');
    
    fileList = cell(1,1);
    fileList{1,1} = '';
    fileListIdx = 1;
        
    for i=2:length(raw)
        f = strfind( fileList, raw{i,1} );
        g = find(not(cellfun('isempty', f)));
        
        if numel(g) == 0
            
            fileList{fileListIdx,1} = raw{i,1};
            fileListIdx = fileListIdx + 1;
            
            
            findOFname = strfind( raw(:,1), raw{i,1} );
            idxList = find(not(cellfun('isempty', findOFname )));
            
            fileMatrix = cell2mat(raw(idxList, 5:end));
            
            featureMatrix = fileMatrix;
            
            if savefile == true
                save( [ outputDirectory '/' raw{i,1} ], 'featureMatrix' );
                display([ 'Saving ' raw{i,1} ] );
            else
                display([ 'Processing ' raw{i,1} ] );
            end
            
            key = raw{i,1};
            key = [key(1:end-3),'wav'];
            featureCell(key) = featureMatrix; % Save to a cell
        end
    end
end