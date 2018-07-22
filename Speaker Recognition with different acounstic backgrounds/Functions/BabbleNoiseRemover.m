function newSignal = BabbleNoiseRemover(signal,fs)
    windowL = 100e-3; % in Sec
    threshold = 5;
    IS = FindFirstNoisePeriod(signal,fs,windowL,threshold);
    [newSignal,~]=WienerNoiseReduction(signal,fs,IS);
end

function y = FindFirstNoisePeriod(signal,fs,windowL,threshold)
    
    segmentCount = floor( length(signal)/(fs*windowL) );
    windowSampleCount = fs*windowL;
    previousE = norm(signal( 1 : windowSampleCount))^2;
    ratio = zeros(1,segmentCount-1);
    for i = 2 : segmentCount
        if windowSampleCount*(i+1)> length(signal)
           break;
        end
        segment = signal(i*windowSampleCount+1 : windowSampleCount*(i+1));
        ratio(i-1)= (norm(segment)^2)/previousE;
        if (norm(segment)^2)/previousE > threshold         
            y = i * windowSampleCount;
           return;
        end
        previousE = norm(segment)^2;
    end
y =  windowSampleCount;
end