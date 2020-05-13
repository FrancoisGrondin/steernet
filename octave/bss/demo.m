
warning('off','all');
folder = '';

nFiles = 1000;
sdrs = zeros(nFiles,2);

for index = 0:1:(nFiles-1)

    xs = audioread(sprintf('%s%08u.wav',folder,index));

    xRef = xs(:,1)';
    xMix = xs(:,2)';
    xGev = xs(:,3)';

    SDRmix = bss_eval_sources(xMix,xRef);
    SDRgev = bss_eval_sources(xGev,xRef);

    sdrs(index+1,1) = SDRmix;
    sdrs(index+1,2) = SDRgev;
    
    disp(index);

end