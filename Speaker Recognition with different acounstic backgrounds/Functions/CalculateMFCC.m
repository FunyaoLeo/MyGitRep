function [MFCCMap,columnName]= CalculateMFCC(inputDirName,Tw,Ts,alpha,R,M,C,L,savefile)
%Tw = 25;            % analysis frame duration (ms)
%Ts = 1;             % analysis frame shift (ms)
%alpha = 0.97;       % preemphasis coefficient
%R = [0 1000];       % frequency range to consider
%M = 20;             % number of filterbank channels 
%C = 13;             % number of cepstral coefficients
%L = 22;             % cepstral sine lifter parameter
       
% hamming window (see Eq. (5.2) on p.73 of [1])
hamming = @(N)(0.54-0.46*cos(2*pi*[0:N-1].'/(N-1)));
       
folderInfo = dir(inputDirName); 
mfcc_cell = {}; %initialize result cell

disp(['Using files in ',inputDirName]);
MFCCMap = containers.Map;
addpath(genpath(inputDirName));
for i = 1:length(folderInfo)
    if folderInfo(i).isdir == true
        continue;
    end
    [speech,fs] = audioread(folderInfo(i).name);
    
    col_length = floor(size(speech,1)/8);
    zeroPadLength = 1E-3*fs*Tw + (1E-3*fs*Ts)*(col_length-1) - size(speech,1);       
    speech = [speech; zeros(zeroPadLength,1)];
    
    mfcc1 = (mfcc(speech, fs, Tw, Ts, alpha, hamming, R, M, C, L)).';

    temp_mfcc_cell = num2cell(mfcc1);
    file_id = folderInfo(i).name;
    for k = 1:col_length
       temp_mfcc_cell{k,C+1} = file_id;
    end
    mfcc_cell = [mfcc_cell; temp_mfcc_cell];
    MFCCMap(file_id) = mfcc1;
    if(mod(i,10)==0)
        disp(['Calculating MFCC: Completed ',num2str(i),' of ',num2str(length(folderInfo)),' files.']);
    end
end

columnName = {};
for i = 1:C
    columnName{i} = ['MFCC_',num2str(i)];
end
columnName{C+1}='file_id';

if savefile == true
    mkdir([inputDirName,'/EXCEL'])
    filename = [inputDirName,'/EXCEL/MFCCs.xlsx'];
    fprintf("Writing to Excel file...\n")
    T = cell2table(mfcc_cell,'VariableNames',columnName);
    writetable(T,filename);
end