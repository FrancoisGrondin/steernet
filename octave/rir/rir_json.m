function json = rir_json(params)

    txt_room = sprintf('"room": [ %1.2f, %1.2f, %1.2f ]', params.room(1), params.room(2), params.room(3));
    txt_beta = sprintf('"beta": %1.2f', params.beta);
    txt_speed = sprintf('"speed": %1.1f', params.speed);
    txt_fs = sprintf('"fs": %u', params.fs);
    
    txt_mics = sprintf('"mics": [ ');
    nMics = size(params.mics,1);
    for iMic = 1:1:nMics
        txt_mic = sprintf('[ %1.3f, %1.3f, %1.3f ]', params.mics(iMic,1), params.mics(iMic,2), params.mics(iMic,3));
        txt_mics = [ txt_mics txt_mic ];
        if (iMic ~= nMics)
            txt_mics = [ txt_mics ', ' ];
        end
    end
    txt_mics = [ txt_mics ' ]' ];
    
    txt_srcs = '"srcs": [ ';
    nSrcs = size(params.srcs,1);
    for iSrc = 1:1:nSrcs
        txt_src = sprintf('[ %1.3f, %1.3f, %1.3f ]', params.srcs(iSrc,1), params.srcs(iSrc,2), params.srcs(iSrc,3));
        txt_srcs = [ txt_srcs txt_src ];
        if (iSrc ~= nSrcs)
            txt_srcs = [ txt_srcs ', ' ];
        end
    end
    txt_srcs = [ txt_srcs ' ]' ];
    
    txt_noise = sprintf('"noise": %1.5f', params.noise);    
    
    json = sprintf('{\n\t%s,\n\t%s,\n\t%s,\n\t%s,\n\t%s,\n\t%s,\n\t%s\n}', txt_room, txt_beta, txt_speed, txt_fs, txt_mics, txt_srcs, txt_noise);

return