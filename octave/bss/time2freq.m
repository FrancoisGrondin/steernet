function f = time2freq(x,hopSize,frameSize)

    nSamples = length(x);
    nFrames = floor((nSamples - frameSize + hopSize)/hopSize);
    R = 1;
    
    halfFrameSize = R*frameSize / 2 + 1;
    f = zeros(nFrames,halfFrameSize);
    
    window = sqrt(hann(frameSize))';
    frameW2 = zeros(1, R*frameSize);
    
    for iFrame = 1:1:nFrames
       
        iStart = (iFrame-1) * hopSize + 1;
        iStop = iStart + frameSize - 1;
        
        frameT = x(iStart:1:iStop);
        frameW = frameT .* window;
        frameW2(1:1:frameSize) = frameW;
        frameF = fft(frameW2);
        
        f(iFrame,:) = frameF(1:1:halfFrameSize);
        
    end

return