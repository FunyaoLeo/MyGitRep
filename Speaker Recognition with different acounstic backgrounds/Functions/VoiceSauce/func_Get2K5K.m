function [H2KH5K] = func_Get2K5K(H2K, F2K, H5K, Fs, F0, F1, F2, F3, B1, B2, B3)
% [H2KH5K] = func_Get2K5K(H2K, F2K, H5K, Fs, F0, F1, F2, F3, B1, B2, B3)
% Input:  H2K, F2K, H5K vectors
%         Fs - sampling frequency
%         F0 - vector of fundamental frequencies
%         Fx, Bx - vectors of formant frequencies and bandwidths
% Output: H2KH5K (2K*-5K) vectors
% Notes:  Function produces the corrected versions of the parameters. They
% are stored as H2KH5K for compatibility reasons. Use func_buildMData.m to
% recreate the mat data with the proper variable names.
% Also note that the bandwidths from the formant trackers are not currently
% used due to the variability of those measurements.
%
% Author: Yen-Liang Shue, Speech Processing and Auditory Perception Laboratory, UCLA
% Copyright UCLA SPAPL 2014


if (nargin == 8)
  B1 = func_getBWfromFMT(F1, F0, 'hm');
  B2 = func_getBWfromFMT(F2, F0, 'hm');
  B3 = func_getBWfromFMT(F3, F0, 'hm');
end

H2K_corr = H2K - func_correct_iseli_z(F2K, F1, B1, Fs);
H2K_corr = H2K_corr - func_correct_iseli_z(F2K, F2, B2, Fs);
H2K_corr = H2K_corr - func_correct_iseli_z(F2K, F3, B3, Fs);

H2KH5K = H2K_corr - H5K;
