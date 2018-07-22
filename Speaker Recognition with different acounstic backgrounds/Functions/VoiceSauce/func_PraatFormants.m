function [F1, F2, F3, F4, F5, F6, F7, B1, B2, B3, B4, B5, B6, B7, err] = func_PraatFormants(wavfile, ...
                                                  windowlength, frameshift, frameprecision, datalen, num_formants, max_formant_freq)
% [F1, F2, F3, F4, F5, F6, F7, B1, B2, B3, B4, B5, B6, B7, err] = func_PraatFormants(wavfile, windowlength, frameshift, frameprecision, datalen)
% KY Time-stamp: <2010-10-16 21:47:24 amoebe>  
% Input:  wavfile - input wav file
%         windowlength - windowlength in seconds
%         frameshift - in seconds
%         frameprecision - unitless
%         datalen - output data length
%         num_formants - number of formants to estimate (min 4, max 7)
% Output: Fx, Bx - formant and bandwidth vectors
%         err - error flag
%
% Author: Yen-Liang Shue, Speech Processing and Auditory Perception Laboratory, UCLA
% Modified by Kristine Yu, 2010-10-16 to allow for variable precision in
% matching up time alignment between data vectors.
%
% Copyright UCLA SPAPL 2010-2014

% settings 
maxFormant = max_formant_freq;
iwantfilecleanup = 1;  %delete pfmt files when done

% check if we need to put double quotes around wavfile
if (wavfile(1) ~= '"')
    pwavfile = ['"' wavfile '"'];
else
    pwavfile = wavfile;
end

if (ispc)  % pc can run praatcon.exe
    cmd = sprintf('Praat\\Praat.exe --run Praat\\praatformants.praat %s %.3f %.3f %.1f %d', pwavfile, frameshift, windowlength, num_formants, maxFormant);

elseif (ismac) % mac osx can run Praat using terminal, call Praat from
                % Nix/ folder
  curr_wav = wavfile;
  
  cmd = sprintf(['Praat/Praat.app/Contents/MacOS/Praat Praat/praatformants.praat ' ...
  '%s %.3f %.3f %.1f %d'], curr_wav, frameshift, windowlength, num_formants, maxFormant);
    
else
    F1 = NaN; F2 = NaN; F3 = NaN; F4 = NaN; F5 = NaN; F6 = NaN; F7 = NaN;
    B1 = NaN; B2 = NaN; B3 = NaN; B4 = NaN; B5 = NaN; B6 = NaN; B7 = NaN;
    err = -1;
    return;
end

% Set name of formant track file
fmtfile = [wavfile '.pfmt'];

F5 = []; F6 = []; F7 = [];
B5 = []; B6 = []; B7 = [];

%call up praat

% for pc
if (ispc)
  err = system(cmd);
  
  if (err ~= 0)  % oops, error, exit now
    F1 = NaN; F2 = NaN; F3 = NaN; F4 = NaN; F5 = NaN; F6 = NaN; F7 = NaN;
    B1 = NaN; B2 = NaN; B3 = NaN; B4 = NaN; B5 = NaN; B6 = NaN; B7 = NaN;
    if (iwantfilecleanup)
      if (exist(fmtfile, 'file') ~= 0)
        delete(fmtfile);
      end        
    end
    return;
  end
end


% for mac
if (ismac)
  err = unix(cmd);

  if (err ~= 0)  % oops, error, exit now
    F1 = NaN; F2 = NaN; F3 = NaN; F4 = NaN; F5 = NaN; F6 = NaN; F7 = NaN;
    B1 = NaN; B2 = NaN; B3 = NaN; B4 = NaN; B5 = NaN; B6 = NaN; B7 = NaN;
    if (iwantfilecleanup)
      if (exist(fmtfile, 'file') ~= 0)
        delete(fmtfile);
      end        
    end
    return;
  end
end

% praat call was successful, return fmt values
F1 = zeros(datalen, 1) * NaN;  B1 = zeros(datalen, 1) * NaN;
F2 = zeros(datalen, 1) * NaN;  B2 = zeros(datalen, 1) * NaN;
F3 = zeros(datalen, 1) * NaN;  B3 = zeros(datalen, 1) * NaN;
F4 = zeros(datalen, 1) * NaN;  B4 = zeros(datalen, 1) * NaN;

num_formants = round(num_formants);

if (num_formants >= 5)
    F5 = zeros(datalen, 1) * NaN;  B5 = zeros(datalen, 1) * NaN;
end
if (num_formants >= 6)
    F6 = zeros(datalen, 1) * NaN;  B6 = zeros(datalen, 1) * NaN;
end
if (num_formants == 7)
    F7 = zeros(datalen, 1) * NaN;  B7 = zeros(datalen, 1) * NaN;
end

% Get formant file

fid = fopen(fmtfile, 'rt');

% read and discard the header
C = textscan(fid, '%s', 1, 'delimiter', '\n');

% read the rest
switch(num_formants)
    case 4
        C = textscan(fid, '%f %f %f %f %f %f %f %f %f %f', 'delimiter', '\n', 'TreatAsEmpty', '--undefined--');
    case 5
        C = textscan(fid, '%f %f %f %f %f %f %f %f %f %f %f %f', 'delimiter', '\n', 'TreatAsEmpty', '--undefined--');
    case 6
        C = textscan(fid, '%f %f %f %f %f %f %f %f %f %f %f %f %f %f', 'delimiter', '\n', 'TreatAsEmpty', '--undefined--');
    case 7
        C = textscan(fid, '%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f', 'delimiter', '\n', 'TreatAsEmpty', '--undefined--');
    otherwise
        C = textscan(fid, '%f %f %f %f %f %f %f %f %f %f', 'delimiter', '\n', 'TreatAsEmpty', '--undefined--');
end
fclose(fid);
t = round(C{1} * 1000);  % time locations

start = 0; % KY changed since Praat doesn't necessarily have data start
           % at time = 0
finish = t(end);
increment = frameshift * 1000;

for k=start:increment:finish
    [val, inx] = min(abs(t - k)); % try to find the closest value
    if (abs(t(inx) - k) > frameprecision * frameshift * 1000)  % no valid value found
        continue;
    end
   
    n = round(k / (frameshift * 1000)) + 1; % KY I added 1 since Matlab
                                            % index starts at 1, not 0
    if (n < 1 || n > datalen)
        continue;
    end
    
    F1(n) = C{3}(inx);
    B1(n) = C{4}(inx);
    F2(n) = C{5}(inx);
    B2(n) = C{6}(inx);
    F3(n) = C{7}(inx);
    B3(n) = C{8}(inx);
    F4(n) = C{9}(inx);
    B4(n) = C{10}(inx);
    
    if (num_formants >= 5)
        F5(n) = C{11}(inx);
        B5(n) = C{12}(inx);
    end
    if (num_formants >= 6)
        F6(n) = C{13}(inx);
        B6(n) = C{14}(inx);
    end
    if (num_formants == 7)
        F7(n) = C{15}(inx);
        B7(n) = C{16}(inx);
    end
end

if (iwantfilecleanup)
    if (exist(fmtfile, 'file') ~= 0)
        delete(fmtfile);
    end    
end
