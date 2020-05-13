function fullFrame = half2full(halfFrame)
 
    halfFrameSize = size(halfFrame,2);
    frameSize = (halfFrameSize - 1) * 2;
 
    fullFrame = [ halfFrame conj(fliplr(halfFrame(:,2:1:(halfFrameSize-1)))) ];
 
return