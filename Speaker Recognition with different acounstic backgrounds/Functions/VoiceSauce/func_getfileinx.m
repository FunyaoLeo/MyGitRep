function fileinx = func_getfileinx(param)
% fileinx = func_getfileinx(param)
% Input:  param
% Output: file index
% Notes:  Function is a helper function for outputting to text. 
%
% Author: Yen-Liang Shue, Speech Processing and Auditory Perception Laboratory, UCLA
% Copyright UCLA SPAPL 2009-2014

switch (param)
    case {'F0 - Straight (strF0)', 'F0 - Snack (sF0)', 'F0 - Praat (pF0)', 'F0 - Other (oF0)', 'F0 - SHR (shrF0)', 'CPP (CPP)', 'Energy (Energy)', 'HNR05 (HNR05)', 'HNR15 (HNR15)', 'HNR25 (HNR25)', 'HNR35 (HNR35)'}
        fileinx = 1;
    case {'F1 - Snack (sF1)', 'F2 - Snack (sF2)', 'F3 - Snack (sF3)', 'F4 - Snack (sF4)', 'F1 - Praat (pF1)', 'F2 - Praat (pF2)', 'F3 - Praat (pF3)', 'F4 - Praat (pF4)', 'F1 - Other (oF1)', 'F2 - Other (oF2)', 'F3 - Other (oF3)', 'F4 - Other (oF4)', 'B1 - Snack (sB1)', 'B2 - Snack (sB2)', 'B3 - Snack (sB3)', 'B4 - Snack (sB4)', 'B1 - Praat (pB1)', 'B2 - Praat (pB2)', 'B3 - Praat (pB3)', 'B4 - Praat (pB4)', 'B5 - Praat (pB5)', 'B6 - Praat (pB6)', 'B7 - Praat (pB7)', 'B1 - Other (oB1)', 'B2 - Other (oB2)', 'B3 - Other (oB3)', 'B4 - Other (oB4)'}
        fileinx = 2;
    case {'F5 - Snack (sF5)', 'F6 - Snack (sF6)', 'F7 - Snack (sF7)', 'F5 - Praat (pF5)', 'F6 - Praat (pF6)', 'F7 - Praat (pF7)', 'F5 - Other (oF5)', 'F6 - Other (oF6)', 'F7 - Other (oF7)', 'B5 - Snack (sB5)', 'B6 - Snack (sB6)', 'B7 - Snack (sB7)', 'B5 - Other (oB5)', 'B6 - Other (oB6)', 'B7 - Other (oB7)'}
        fileinx = 2;
    case {'H1* (H1c)', 'H2* (H2c)', 'H4* (H4c)', 'A1* (A1c)', 'A2* (A2c)', 'A3* (A3c)', '2K* (H2Kc)', 'H1 (H1u)', 'H2 (H2u)', 'H4 (H4u)', 'A1 (A1u)', 'A2 (A2u)', 'A3 (A3u)', '2K (H2Ku)', '5K (H5Ku)'}
        fileinx = 3;
    case {'H1*-H2* (H1H2c)', 'H2*-H4* (H2H4c)', 'H1-H2 (H1H2u)', 'H2-H4 (H2H4u)', 'SHR (SHR)'}
        fileinx = 4;
    case {'H1*-A1* (H1A1c)', 'H1*-A2* (H1A2c)', 'H1*-A3* (H1A3c)', 'H4*-2K* (H42Kc)', '2K*-5K (H2KH5Kc)', 'H1-A1 (H1A1u)', 'H1-A2 (H1A2u)', 'H1-A3 (H1A3u)', 'H4-2K (H42Ku)', '2K-5K (H2KH5Ku)'}
        fileinx = 5;
    case {'epoch (epoch)', 'SoE (soe)'}
        fileinx = 6;
    otherwise
        fileinx = -1;
end
