function mdata = func_buildMData(matfile, smoothwin)
% mdata = func_buildMData(matfile, smoothwin)
% Input:  mat filename
%         smoothing window size (0 denotes no smoothing)
% Output: mat data structure
% Notes:  Function tries to construct as many parameters as possible based
% on the parameters currently in the mat file. Some parameters will have a
% different variable name to what is originally stored in the mat file:
% e.g. H1 is actually the uncorrected harmonic (H1u), it is stored this way
% for compatability reasons.
%
% Author: Yen-Liang Shue, Speech Processing and Auditory Perception Laboratory, UCLA
% Copyright UCLA SPAPL 2009-2015

mdata = load(matfile);

% these are for compatibility with VS0 matfiles
if (~isfield(mdata, 'HF0algorithm'))
    mdata.HF0algorithm = 'F0 (Straight)';
end

if (~isfield(mdata, 'AFMTalgorithm'))
    mdata.AFMTalgorithm = 'Formants (Snack)';
end

if (~isfield(mdata, 'Fs'))
    mdata.Fs = 16000;
end

% make sure output to text has something to print if these fields don't
% exist
if (~isfield(mdata, 'H2KFMTalgorithm'))
    mdata.H2KFMTalgorithm = '';
end

if (~isfield(mdata, 'BandwidthMethod'))
    mdata.BandwidthMethod = '';
end

if (~isfield(mdata, 'frameshift'))
    mdata.frameshift = 0;
end

if (~isfield(mdata, 'preemphasis'))
    mdata.preemphasis = 0;
end

if (~isfield(mdata, 'windowsize'))
    mdata.windowsize = 0;
end

% get the right F0
F0 = func_parseF0(mdata, mdata.HF0algorithm);
[F1, F2, F3] = func_parseFMT(mdata, mdata.AFMTalgorithm);

% can't do much without F0 or FMTs
if (isempty(F0) || isempty(F1))
    return;
end

% get bandwidth mapping
B1 = func_getBWfromFMT(F1, F0, 'hm');
B2 = func_getBWfromFMT(F2, F0, 'hm');
B3 = func_getBWfromFMT(F3, F0, 'hm');

% Hx
if (isfield(mdata, 'H1'))
    mdata.H1u = mdata.H1;  % H1 is actually the uncorrected harmonic
    mdata.H1c = mdata.H1u - func_correct_iseli_z(F0, F1, B1, mdata.Fs);  % correct for F1
    mdata.H1c = mdata.H1c - func_correct_iseli_z(F0, F2, B2, mdata.Fs);  % correct for F2    
    if (smoothwin~=0)
        mdata.H1u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1u);
        mdata.H1c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1c);
    end    
    %mdata = rmfield(mdata, 'H1');  % remove H1 to remove confusion
end

if (isfield(mdata, 'H2'))
    mdata.H2u = mdata.H2;  % H2 is actually the uncorrected harmonic
    mdata.H2c = mdata.H2u - func_correct_iseli_z(2*F0, F1, B1, mdata.Fs);
    mdata.H2c = mdata.H2c - func_correct_iseli_z(2*F0, F2, B2, mdata.Fs);
    if (smoothwin~=0)
        mdata.H2u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H2u);
        mdata.H2c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H2c);
    end
    %mdata = rmfield(mdata, 'H2');
end

if (isfield(mdata, 'H4'))
    mdata.H4u = mdata.H4;  % H4 is actually the uncorrected harmonic
    mdata.H4c = mdata.H4u - func_correct_iseli_z(4*F0, F1, B1, mdata.Fs);
    mdata.H4c = mdata.H4c - func_correct_iseli_z(4*F0, F2, B2, mdata.Fs);
    if (smoothwin~=0)
        mdata.H4u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H4u);
        mdata.H4c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H4c);
    end
    %mdata = rmfield(mdata, 'H4');
end
    
% Ax
if (isfield(mdata, 'A1'))
    mdata.A1u = mdata.A1; % A1 is actually the uncorrected amplitude
    mdata.A1c = mdata.A1u - func_correct_iseli_z(F1, F1, B1, mdata.Fs);
    mdata.A1c = mdata.A1c - func_correct_iseli_z(F1, F2, B2, mdata.Fs);
    if (smoothwin~=0)
        mdata.A1u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.A1u);
        mdata.A1c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.A1c);
    end    
    %mdata = rmfield(mdata, 'A1');
end

if (isfield(mdata, 'A2'))
    mdata.A2u = mdata.A2; % A2 is acutally the uncorrected amplitude
    mdata.A2c = mdata.A2u - func_correct_iseli_z(F2, F1, B1, mdata.Fs);
    mdata.A2c = mdata.A2c - func_correct_iseli_z(F2, F2, B2, mdata.Fs);
    if (smoothwin~=0)
        mdata.A2u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.A2u);
        mdata.A2c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.A2c);
    end
    %mdata = rmfield(mdata, 'A2');
end

if (isfield(mdata, 'A3'))
    mdata.A3u = mdata.A3; % A3 is actually the uncorrected amplitude
    mdata.A3c = mdata.A3u - func_correct_iseli_z(F3, F1, B1, mdata.Fs);
    mdata.A3c = mdata.A3c - func_correct_iseli_z(F3, F2, B2, mdata.Fs);
    mdata.A3c = mdata.A3c - func_correct_iseli_z(F3, F3, B3, mdata.Fs);
    if (smoothwin~=0)
        mdata.A3u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.A3u);
        mdata.A3c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.A3c);
    end
    %mdata = rmfield(mdata, 'A3');
end

% 2K
if (isfield(mdata, 'H2K') && isfield(mdata, 'F2K'))
    mdata.H2Ku = mdata.H2K;
    mdata.H2Kc = mdata.H2Ku - func_correct_iseli_z(mdata.F2K, F1, B1, mdata.Fs);
    mdata.H2Kc = mdata.H2Kc - func_correct_iseli_z(mdata.F2K, F2, B2, mdata.Fs);
    mdata.H2Kc = mdata.H2Kc - func_correct_iseli_z(mdata.F2K, F3, B3, mdata.Fs);
    if (smoothwin~=0)
        mdata.H2Ku = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H2Ku);
        mdata.H2Kc = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H2Kc);
    end    
end

% 5K
if (isfield(mdata, 'H5K'))
    mdata.H5Ku = mdata.H5K;
    if (smoothwin~=0)
        mdata.H5Ku = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H5Ku);
    end    
end

% the uncorrected combo parameters
if (isfield(mdata, 'H1') && isfield(mdata, 'H2'))
    mdata.H1H2u = mdata.H1 - mdata.H2;
    if (smoothwin ~= 0)
        mdata.H1H2u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1H2u);
    end
end

if (isfield(mdata, 'H2') && isfield(mdata, 'H4'))
    mdata.H2H4u = mdata.H2 - mdata.H4;
    if (smoothwin ~= 0)
        mdata.H2H4u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H2H4u);
    end
end

if (isfield(mdata, 'H1') && isfield(mdata, 'A1'))
    mdata.H1A1u = mdata.H1 - mdata.A1;
    if (smoothwin ~= 0)
        mdata.H1A1u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1A1u);
    end
end

if (isfield(mdata, 'H1') && isfield(mdata, 'A2'))
    mdata.H1A2u = mdata.H1 - mdata.A2;
    if (smoothwin ~= 0)
        mdata.H1A2u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1A2u);
    end
end

if (isfield(mdata, 'H1') && isfield(mdata, 'A3'))
    mdata.H1A3u = mdata.H1 - mdata.A3;
    if (smoothwin ~= 0)
        mdata.H1A3u = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1A3u);
    end
end

if (isfield(mdata, 'H4') && isfield(mdata, 'H2K'))
    mdata.H42Ku = mdata.H4 - mdata.H2K;
    if (smoothwin ~= 0)
        mdata.H42Ku = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H42Ku);
    end
end
    
if (isfield(mdata, 'H2K') && isfield(mdata, 'H5K'))
    mdata.H2KH5Ku = mdata.H2Ku - mdata.H5Ku;
    if (smoothwin ~= 0)
        mdata.H2KH5Ku = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H2KH5Ku);
    end
end


% this section is included for old VS compatibility, previously, the
% corrected versions of HxHx and HxAx were stored as HxHx and HxAx (i.e.
% without the "c"
if (isfield(mdata, 'H1H2'))
    mdata.H1H2c = mdata.H1H2;
end

if (isfield(mdata, 'H2H4'))
    mdata.H2H4c = mdata.H2H4;
end

if (isfield(mdata, 'H1A1'))
    mdata.H1A1c = mdata.H1A1;
end

if (isfield(mdata, 'H1A2'))
    mdata.H1A2c = mdata.H1A2;
end

if (isfield(mdata, 'H1A3'))
    mdata.H1A3c = mdata.H1A3;
end


% check if the others require smoothing
if (smoothwin ~= 0)
    if (isfield(mdata, 'H1H2c'))
        mdata.H1H2c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1H2c);
    end
    
    if (isfield(mdata, 'H2H4c'))
        mdata.H2H4c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H2H4c);
    end
    
    if (isfield(mdata, 'H1A1c'))
        mdata.H1A1c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1A1c);
    end
    
    if (isfield(mdata, 'H1A2c'))
        mdata.H1A2c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1A2c);
    end
    
    if (isfield(mdata, 'H1A3c'))
        mdata.H1A3c = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H1A3c);
    end
    
    if (isfield(mdata, 'H42Kc'))
        mdata.H42Kc = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H42Kc);
    end
    
    if (isfield(mdata, 'H2KH5Kc'))
        mdata.H2KH5Kc = filter(ones(smoothwin,1)/smoothwin, 1, mdata.H2KH5Kc);
    end
    
    if (isfield(mdata, 'CPP'))
        mdata.CPP = filter(ones(smoothwin,1)/smoothwin, 1, mdata.CPP);
    end
       
    if (isfield(mdata, 'HNR05'))
        mdata.HNR05 = filter(ones(smoothwin,1)/smoothwin, 1, mdata.HNR05);
    end

    if (isfield(mdata, 'HNR15'))
        mdata.HNR15 = filter(ones(smoothwin,1)/smoothwin, 1, mdata.HNR15);
    end

    if (isfield(mdata, 'HNR25'))
        mdata.HNR25 = filter(ones(smoothwin,1)/smoothwin, 1, mdata.HNR25);
    end

    if (isfield(mdata, 'HNR35'))
        mdata.HNR35 = filter(ones(smoothwin,1)/smoothwin, 1, mdata.HNR35);
    end
    
end