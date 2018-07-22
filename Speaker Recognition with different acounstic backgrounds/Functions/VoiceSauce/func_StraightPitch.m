function [F0, V] = func_StraightPitch(y, Fs, variables, textgridfile)
% [F0, V] = func_StraightPitch(y, Fs, variables, textgridfile)
% Input:  y, Fs - from wavread
%         variables - settings
%         textgridfile - this is optional
% Output: F0, V - F0 and voicing vectors
% Notes:  This function calls the Straight functions. Using textgrid
% segmentation helps to speed up the processing.
%
% Author: Yen-Liang Shue, Speech Processing and Auditory Perception Laboratory, UCLA
% Copyright UCLA SPAPL 2009-2016

% Note: Straight was updated in version 1.28. There are minor differences
% in the F0 estimations from previous versions.

maxdur = variables.maxstrdur;

params.f0floor = variables.minstrF0;
params.f0ceil = variables.maxstrF0;
params.framePeriod = 1;  % 1ms to maintain consistency with old Straight, this is downsampled later in vs_ParameterEstimation.m

% break up the file if it is too big (i.e. > 15sec)
if (nargin == 3)  % do the whole file, no textgrid data available
    L = floor(length(y)/Fs * 1000) - 1;    
    F0 = zeros(L, 1);

    if (length(y) / Fs > maxdur)
        % find suitable places to chop
        cnt = 1;
        startx = 1;
        endx = startx + floor(maxdur*Fs);

        while(startx < length(y))
            if (startx == 1)
                yseg = y(startx : endx);  % extra millisecond
            else
                yseg = y(startx - floor(F0 / 1000) - 10 : endx);  % extra millisecond
            end
            %fprintf('Processing segment %d to %d\n', startx, endx);
            
            [F0seg, V] = calculateF0(yseg,Fs,params);

            F0(cnt:cnt+length(F0seg)-1) = F0seg;
            cnt = cnt + length(F0seg);
            startx = endx + 1;
            
            remainder = length(y) - endx - 1;
            if (remainder > maxdur*Fs)
                endx = startx + floor(maxdur*Fs);
            else
                endx = length(y);
            end
        end        
    else
        [F0, V] = calculateF0(y,Fs,params);
    end
else  % use textgrid data
    % get the labels to ignore from the settings
    tbuffer = variables.tbuffer;
    ignorelabels = textscan(variables.TextgridIgnoreList, '%s', 'delimiter', ',');
    ignorelabels = ignorelabels{1};
    
    [labels, start, stop] = func_readTextgrid(textgridfile);
    
    labels_tmp = [];
    start_tmp = [];
    stop_tmp = [];
    
    for k=1:length(variables.TextgridTierNumber)
        inx = variables.TextgridTierNumber(k);
        if (inx <= length(labels))
            labels_tmp = [labels_tmp; labels{inx}];
            start_tmp = [start_tmp; start{inx}];
            stop_tmp = [stop_tmp; stop{inx}];
        end
    end
    
    labels = labels_tmp;
    start = start_tmp * 1000; % milliseconds
    stop = stop_tmp * 1000; % milliseconds
    
    L = floor(length(y) / Fs * 1000) - 1;
    
    F0 = zeros(L, 1) * NaN;
    V = zeros(L, 1) * NaN;
    
    for k=1:length(start)
        
        switch(labels{k})
            case ignorelabels
                continue;  % skip anything that is within the ignore list
        end
                
        tstart = start(k) - tbuffer;
        tstop = stop(k) + tbuffer;
        
        sstart = floor(tstart / 1000 * Fs);
        sstop = ceil(tstop / 1000 * Fs);
        
        sstart(sstart <= 0) = 1;
        sstop(sstop > length(y)) = length(y);
        
        yseg = y(sstart:sstop);

        [F0seg, Vseg] = calculateF0(yseg,Fs,params);
        
        tstart = floor(tstart);
        tstart(tstart <= 0) = 1;
        F0(tstart:tstart+length(F0seg)-1) = F0seg;
        V(tstart:tstart+length(Vseg)-1) = Vseg;
        
        if (length(F0) > L)
            F0 = F0(1:L);
        end
        
    end
    
end

% sometimes Straight outputs 0s for F0
F0(F0 == 0) = NaN;


function [F0, V] = calculateF0(y,fs,params)
r = exF0candidatesTSTRAIGHTGB(y,fs,params);
rc = autoF0Tracking(r, y);
F0 = rc.f0;
if (~isfield(rc, 'vuv'))
    % assume everything is voiced
    rc.vuv = ones(size(F0));
end
V = refineVoicingDecision(y,rc);

% do some simple filtering to make results comparable with v1.27 and below
if (length(F0) > 14)
    F0_smooth = filter(ones(9,1)/9, 1, [ones(9, 1) * F0(1); F0; ones(4, 1) * F0(end)]);
    F0 = F0_smooth(14:end);
end
