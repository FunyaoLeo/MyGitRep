function silenceRemovedSound = RemoveSilence( signal )
%SEPARATEWORDS Summary of this function goes here
%   Detailed explanation goes here
   %[signal,~] = audioread(inputFile);
    
    windowLength = 100;
    signalEnergy = zeros(length(signal)-windowLength, 1);
    
    for j=1:length(signal)-windowLength
        signalWindow = signal(j:j+windowLength);
        signalEnergy(j) = sum( signalWindow.^2 );
    end
    
    baselineEnergy = signalEnergy(1);
    
    if baselineEnergy <= 1e-4
        baselineEnergy = 0.01;
    end
    
    soundRegions = (signalEnergy > 10 * baselineEnergy);
    idx = find(soundRegions);
    silenceRemovedSound = signal(idx);
    
    %close all;plot(signal);figure;plot(silenceRemovedSound);
end


