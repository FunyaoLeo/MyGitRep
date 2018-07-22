function [y, fs, nbits] = func_readwav(wavfile)

if (nargout == 3)
    info = audioinfo(wavfile);
    nbits = info.BitsPerSample;
end

[y,fs] = audioread(wavfile);
end