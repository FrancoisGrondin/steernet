function wave = rir_wave(params)
  
    c = params.speed;
    fs = params.fs;
    r = params.mics;
    L = params.room;
    beta = params.beta * ones(1,6);
    n = 0.5 * fs;
    
    nMics = size(params.mics,1);
    nSrcs = size(params.srcs,1);
    
    hs = zeros(nMics*nSrcs,n);
    
    for iSrc = 1:1:nSrcs
        
        s = params.srcs(iSrc,:);
        h = rir_generator(c, fs, r, s, L, beta, n); 
  
        iStart = (iSrc-1) * nMics + 1;
        iStop = (iSrc-1) * nMics + nMics;

        hs(iStart:1:iStop,:) = h;
        
    end     
  
    wave = hs;
  
end
