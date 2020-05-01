root = argv(){1};
geometry = argv(){2};
N = str2num(argv(){3});

rooms = [ 5 10 5 10 2 5 ];
betas = [ 0.2 0.8 ];
speeds = [ 340.0 355.0 ];
fs = 16000;
margin = 0.5;
dists = [ 1.0 5.0 ];
counts = [ 2 2 ];

if strcmp(geometry, 'pair')
    mics = [ -0.5 0.0 0.0 ; 0.5 0.0 0.0 ];
    scales = [ 0.04 0.20 ];
end

if strcmp(geometry, 'circular')
    mics = [ +0.0 +0.00 0.0 ; ...
             +1.0 +0.00 0.0 ; ...
             +0.5 +0.87 0.0 ; ...
             -0.5 +0.87 0.0 ; ...
             -1.0 +0.00 0.0 ; ...
             -0.5 -0.87 0.0 ; ...
             +0.5 -0.87 0.0 ];
    scales = [ 0.05 0.05 ];
end

for n = 1:1:N

    disp(n);

    params = rir_setup(rooms, betas, speeds, mics, scales, fs, margin, dists, counts);
    json = rir_json(params);
    wave = rir_wave(params);

    id = ('a':'z')(randi([1 26],1,10));
    path = [ root id(1) '/' id(2) '/' id ];

    fid = fopen([path '.json'], 'w');
    fprintf(fid, json);
    fclose(fid);

    audiowrite([path '.wav'], wave', fs);
    
end