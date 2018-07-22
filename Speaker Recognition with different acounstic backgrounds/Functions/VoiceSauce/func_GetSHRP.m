function [SHR,F0]=func_GetSHRP(y,Fs, variables, datalen)
%function [f0_time,f0_value,SHR,f0_candidates]=func_GetSHRP(y,Fs,F0MinMax,timestep,SHR_Threshold)
% Input:  y, Fs - from wavread
%         variables - settings from initialization/setting
%         datalen - output data length
% Output: F0 - F0 values
%         SHR - Subharmonic-harmonic ratio values
%         (and eventually, F0 candidates?)
% Author: Kristine Yu, Department of Linguistics, UCLA, based off code
% by Yen-Liang Shue for func_PraatPitch.m
% Modified on 5/4/2015 to process in 10s chunks to reduce memory use


%%%%%%%%%%% Get/set arguments to shrp.m

% TESTING
% [y,Fs]=wavread('work/beijing_f3_50_a.wav'); % for testing
% F0MinMax = [vars.SHRmin, vars.SHRmax]; % For testing
% windowsize = vars.windowsize; % Set frame_length to 25ms, the VS default, for testing
% frameshift = vars.frameshift; % Set 10 ms frameshift, for testing
% SHR_Threshold = 0.4; %
% frame_precision = 1; % fudge factor for time alignment
% ceiling = 1250;
% med_smooth = 0; CHECK_VOICING = 0; % Leave default: no smoothing, no voice detection

%%% Get settings

F0MinMax = [variables.SHRmin, variables.SHRmax]; % Set lower and
                                                       % upper bounds for
                                                       % f0 estimation
  
frameshift = variables.frameshift; % this is in ms
windowsize = variables.windowsize; % also in ms

SHR_Threshold = variables.SHRThreshold; % Set subharmonic-to-harmonic ratio

ceiling = 1250; % Leave default 1250 Hz

med_smooth = 0; CHECK_VOICING = 0; % Leave default: no smoothing, no voice detection

frame_precision = variables.frame_precision; % how many frames can
                                            % time-alignment be off by,
                                            % when outputting data vectors?

chunk_size = 10;  % in secs                                
search_range = 1.5;  % search +/- this range in sec
smooth_win = 0.2 * Fs; 

y_smoothed_energy = filter(ones(smooth_win,1)/smooth_win, 1, y .^ 2);

y_sec = length(y) / Fs;
if (y_sec > chunk_size)
    init_split_idx = 0:chunk_size:y_sec;  % initial split times
    
    adjusted_split_idx = zeros(length(init_split_idx), 1);
    adjusted_split_idx(1) = 1;
    
    for i=2:length(init_split_idx)
        start_search = (init_split_idx(i) - search_range) * Fs;
        end_search = (init_split_idx(i) + search_range) * Fs;
        if (end_search > length(y))
            end_search = length(y);
        end
        
        [val, inx] = min(y_smoothed_energy(start_search:end_search));
        
        adjusted_split_idx(i) = start_search + inx;
    end
    
    % now call shrp
    f0_time = [];
    f0_value = [];
    SHR_value = [];
    f0_candidates = [];
    for i=1:length(adjusted_split_idx);
        startx = adjusted_split_idx(i);
        if (i ~= length(adjusted_split_idx))
            endx = adjusted_split_idx(i+1) - 1;
        else
            endx = length(y);
        end
        
        yseg = y(startx:endx);
        
        [f0_t,f0_v,SHR_v,f0_c]=shrp(yseg,Fs,F0MinMax,windowsize,frameshift,SHR_Threshold,ceiling,med_smooth,CHECK_VOICING);

        f0_time = [f0_time; (f0_t + (startx-1)/Fs * 1000)];
        f0_value = [f0_value; f0_v];
        SHR_value = [SHR_value; SHR_v];
        f0_candidates = [f0_candidates; f0_c];
    end
    
else

    %%%%%%%%%%% Calculate subharmonic-harmonic ratios and f0 tracks
    % Call Xuejing Sun's subharmonic-harmonic ratio based pitch detection
    % algorithm shrp.m
    % Available for download here
    %http://www.mathworks.com/matlabcentral/fileexchange/1230-pitch-determination-algorithm
    %http://www.speakingx.com/blog/2008/01/02/pitch-determination

    [f0_time,f0_value,SHR_value,f0_candidates]=shrp(y,Fs,F0MinMax,windowsize,frameshift,SHR_Threshold,ceiling,med_smooth,CHECK_VOICING);
end                                         


%%%%%%%%%%% Postprocess subharmonic-harmonic ratios and f0 tracks 

% Initialize F0 and subharmonic-harmonic ratio values  
F0 = zeros(datalen, 1) * NaN; 
SHR = zeros(datalen, 1) * NaN; 
  
t = round(f0_time);  % time locations rounded to nearest ms

start = 0; % Like timecoures from Praat, we might have missing values so pad with NaNs at
           % beginning and end if necessary.
finish = t(end);
increment = frameshift;

for k=start:increment:finish
    [val, inx] = min(abs(t - k)); % try to find the closest value
    if (abs(t(inx) - k) > frame_precision * frameshift)  % no valid value found
        continue;
    end
    
    n = round(k / frameshift) + 1; % KY I added a 1 because Matlab index starts at 1, not 0
    if (n < 1 || n > datalen)
        continue;
    end
    
    F0(n+1) = f0_value(inx); % f0 values
    SHR(n+1) = SHR_value(inx); % SHR values
    % I eventually would like to get candidates as well
end
