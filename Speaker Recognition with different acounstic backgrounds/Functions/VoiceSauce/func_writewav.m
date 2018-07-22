function func_writewav(y, fs, nbits, wavfile)

audiowrite(wavfile, y, fs, 'BitsPerSample', nbits);
end