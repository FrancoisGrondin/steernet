function halfFrame = full2half(fullFrame)
 
    frameSize = length(fullFrame);
    halfFrameSize = frameSize / 2 + 1;
 
    halfFrame = fullFrame(1:1:halfFrameSize);
 
return