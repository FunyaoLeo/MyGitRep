function fMatOut = RemoveSilenceFeatures( fMatIn )
%UNTITLED2 Summary of this function goes here
%   input: Feature matrix of a single audio file
%   output: Feature matrix with silent regions removed

    signal = fMatIn(:,7); %Energy Column of feature matrix fMatIn
    
    baselineEnergy = signal(1:100);
    baselineEnergy(baselineEnergy == 0) = [];
    baselineEnergy = mean(baselineEnergy);
    
    if baselineEnergy < 0.01
        baselineEnergy = 0.01;
    end
    soundRegions = (signal > 3 * baselineEnergy);
    idx = find(soundRegions);
    
    fMatOut = fMatIn(idx,:);
    
end

