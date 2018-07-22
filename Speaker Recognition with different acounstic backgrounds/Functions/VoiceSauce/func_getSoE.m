% ---------------------------------------------
% epoch detection and strength of excitation
% ---------------------------------------------
%
% [1] Murty, K., and B. Yegnanarayana. 
% "Epoch extraction from speech signals." 
% Audio, Speech, and Language Processing, IEEE Transactions on, 2008.
%
% [2] Yegnanarayana, B., and K. Murty. 
% "Event-based instantaneous fundamental frequency estimation from speech signals." 
% Audio, Speech, and Language Processing, IEEE Transactions on, 2009.
%
%
% implemented by Soo Jin Park (sj.park@ucla.edu)
% last modified 2015-06-17
% ---------------------------------------------


function [epoch, soe, z]=func_getSoE(snd,data_len,origSndFs, METHOD, F0, vars)

% ---------------------------------------------
% input ---------------------------------------
%
%   snd         | a vector with the sound signal to analyze
%   data_len    | the desired output length
%   origSndFs   | the sampling frequency of the sound (will be down-sampled)
%   METHOD
%       'whole' : process the whole signal at once
%       'block' : block processing (preferrable if the F0 varies in a large range)
%   F0          | pre-estimated fundamental frequency
% 
% output --------------------------------------
%
%   epoch       | detected epoches (binary)
%       1 : epoch
%       0 : not epoch
%   soe         | the strenght of excitation at each epoch
%                 NaNs if the frame does not correspond to an epoch
%   z           | zero-frequency-filtered signal
% ---------------------------------------------

if vars.frameshift<10
    warning('the frame resolution is too low for pitch period less than 10ms')
end


Fs = 10000; % new sampling frequency
snd = resample(snd, Fs, origSndFs);


%%
if strcmp(METHOD, 'whole')
    F0_nonans = F0(~isnan(F0));
    
    meanN0 = mean(Fs./F0_nonans);   % calculate average pitch period in samples
    
    % ----- get zero-freq filtered signal
    z = zff(snd, meanN0);

    
elseif strcmp(METHOD, 'block')
    
    
    winSec  = vars.windowsize /1000;
    stepSec = vars.frameshift /1000;

    WINDOW  = winSec*Fs;
    STEP    = stepSec*Fs;
    
    
    Nfrm = floor((length(snd)+WINDOW) / Fs / stepSec);    


    z = zeros(size(snd));
    for nf=1:Nfrm
            ks = round((nf-1) * STEP);
            if (ks <= 0 || ks > length(snd))
                continue;
            end
            
            currF0 = F0(nf);
            
            if isnan(currF0)
                F0_nonans = F0(~isnan(F0));
                currF0 = mean(F0_nonans);
            end
            
            currN0 = Fs/currF0;


            
            winStart = round(ks - WINDOW/2);
            if winStart<=0 || winStart+WINDOW-1 > length(snd)
                continue;
            else
                winSnd = snd(winStart:winStart+WINDOW-1);

            end
            


            % ----- take one segment to process
            x= winSnd.*hamming(length(winSnd),'periodic');
            
            % ----- get zero-freq filtered signal
            currZ = zff(x, currN0);
            z(winStart:winStart+WINDOW-1) = z(winStart:winStart+WINDOW-1)+currZ;


    end
    


    
else
    error('invalid method');
end

% ----- normalize
z    = 0.95*z/max(abs(z));


% ----- epoch detection
z1 = [NaN; z(1:end-1)]; % 1-sample delay
tf = z1>0 & z<=0;       % find zero-crossing points

diff = -get_delta(z.',2); % get derivative
diff = diff.';



% xx = (1:length(snd)).';
% epoch =  xx(tf)/Fs; % epoch in [sec]
% soe = diff(tf);


% ------ fit into frames
epoch = zeros(data_len,1);
soe = NaN*ones(data_len,1);
for smpIdx = 1:length(z)
   
    if tf(smpIdx) 
        frm_idx = round(smpIdx/Fs/(vars.frameshift/1000));
        
        if frm_idx <1 || frm_idx>data_len
            continue;
        end
        
        epoch(frm_idx) = 1;
        soe(frm_idx) = diff(smpIdx);
    end
end
epoch = logical(epoch);

% soe = 0.95*soe/max(abs(soe));   % normalize if needed


if ~nargout
    
    xx = (1:length(snd)).';
    tt = xx/Fs;
    t_frm = (1:data_len).' * vars.frameshift/1000;
    
    figure('Name','epoch and SoE');
    ax = zeros(2,1);
    
    
    ax(1)=subplot(3,1,1);
    hold all
    plot(tt, zeros(length(tt),1),'k:');
    plot(tt, snd);
    axis tight;
    
    ax(2)=subplot(3,1,2);
    hold all
    plot(tt, zeros(length(tt),1),'k:');
    plot(tt, z);
    plot(tt(tf), z(tf),'rx');
    axis tight;
    ylabel('zff signal')
    
    ax(3)=subplot(3,1,3);
    stem(t_frm(epoch), soe(epoch));
    axis tight;
    ylabel('SoE')
    
    set(ax(1:end-1), 'xtick',[]);
    xlabel(ax(end), '[sec]')
    linkaxes(ax,'x');
    

end




end



function z = zff(x, n0)


alpha = .999;



% --- differenced signal s
x = x-x(1);
s = filter([1 -1],1, x);

% --- 1st ZFR
u = filter(1,[1 -2*alpha alpha^2],s);
% --- trend-removal operation
v = RemoveTrend(u, round(n0/1.5)); 

% --- 2nd ZFR
y = filter(1,[1 -2*alpha alpha^2],v);
% --- trend-removal operation
z = RemoveTrend(y, round(n0/1.5)); 




if ~nargout
    figure('Name','zero-frequency filtering');
    h = zeros(5,1);
    
    h(1) = subplot(5,1,1);
    plot(x);
    title('input signal');
    axis tight;
    
    h(2) = subplot(5,1,2);
    plot(s);
    title('differenced signal');
    axis tight;
    
    h(3) = subplot(5,1,3);
    hold all;
    plot(u);
    plot(u-v);
    title('1st-filtered signal and its trend');
    axis tight;
    
    h(4) = subplot(5,1,4);
    hold all;
    plot(y);
    plot(y-z);
    title('2nd-filtered signal and its trend');
    axis tight;
    
    h(5) = subplot(5,1,5);
    hold all
    plot(1:length(z),zeros(length(z),1),'k:');
    plot(z);
    title('trend removed signal');
    axis tight;
%     ylim([-500 500])
    
    linkaxes(h, 'x');
end

end


function y=RemoveTrend(x, N)

if round(N)~= N
    warning('N must be an integer: rounding it...')
    N = round(N);
end

width = 2*N+1;
L = length(x);

% ----- find smoothed curve
c = filter(ones(width,1)/width,1,x);
cbegin = cumsum(x(1:width-2));
cbegin = cbegin(1:2:end)./(1:2:(width-2))';
cend = cumsum(x(L:-1:L-width+3));
cend = cend(end:-2:1)./(width-2:-2:1)';
c = [cbegin;c(width:end);cend];

% ----- subtract the smoothed curve from the original
y = x-c;

end


function dx=get_delta(x,D)

% the derivative is obtained
% as described in the HTK book (for HTK 3.4)

% inputs
%   x : [ FEATURE_DIMENSION   FRM ] input matrix
%   D : delta window, 2*D+1 frames are involved


%----- initializing -----%
dx = NaN*ones(size(x));

%----- processing -----%
for nf = 1:size(x,2)
    try
        %----- calculate delta coefficients -----%
        numer = zeros(size(x,1),1);
        denom = 0;
        for theta = 1:D
            numer = numer + theta*(x(:, nf+theta)-x(:, nf-theta));
            denom = denom + 2*theta^2;
        end
        dx(:,nf) = numer/denom;
    catch
        %----- solve end-effect problem -----%
        if nf<=D
            dx(:,nf) = x(:,nf+1)-x(:,nf);
        elseif nf>=size(x,2)-D
            dx(:,nf) = x(:,nf)-x(:,nf-1);
        end
    end

end
end