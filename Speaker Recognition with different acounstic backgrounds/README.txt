Speaker Recognition with different acounstic backgrounds(with and without babble background)

We propose a support vector machine approach to this task of speaker recognition, incorporating elementary voice characteristics, 
namely pitch and formant frequencies, as well as harmonic amplitude measures and Mel Frequency Cepstrum Coefficients (MFCC). 
Dimensionality reduction was performed using a time-average of these features. The magnitude difference between feature vectors 
and the corresponding binary labels (0 if the same speaker and 1 otherwise) were used for training of a support vector machine. 
Training was performed on both data sets with and without the presence of background babble noise. The model was evaluated on both 
clean and noisy data sets as well as two distance calculations: Euclidean and logarithmic. When trained on the clean data and Euclidean 
distance calculation, the model achieved a (FPR, FNR) of (23.8%, 14.8%) on clean testing data, and (30.8%, 20.7%) on noisy testing data. 
Training the machine learning model on both clean and noisy data achieved (FPR, FNR) of (29.3%, 9.6%) on clean testing data, and 
(36.6%, 16.3%) on noisy testing data.