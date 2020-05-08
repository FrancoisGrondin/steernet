function params = rir_setup(rooms, betas, speeds, mics, scales, fs, margin, dists, counts, noises, dtdoa)

    % Select room configuration

    room_size = randi([1,size(rooms,1)]);
    room_X = uniform(rooms(room_size,1), rooms(room_size,2));
    room_Y = uniform(rooms(room_size,3), rooms(room_size,4));
    room_Z = uniform(rooms(room_size,5), rooms(room_size,6));
    room = [ room_X room_Y room_Z ];

    % Select reflection coefficient

    beta = uniform(betas(1), betas(2));

    % Define speed of sound

    speed = uniform(speeds(1), speeds(2));

    % Define microphone array position in the room

    mic0_X = uniform(margin, room_X - margin);
    mic0_Y = uniform(margin, room_Y - margin);
    mic0_Z = uniform(margin, room_Z - margin);
    mic0 = [ mic0_X mic0_Y mic0_Z ];

    % Define microphone rotation

    yaw = uniform(0, 360);
    pitch = uniform(0, 360);
    roll = uniform(0, 360);
    mics_rotation = rotate(yaw, pitch, roll);

    % Define microphones positions
    
    scale = uniform(scales(1), scales(2));
    mics = transpose(mics_rotation * scale * mics' + mic0' * ones(1, size(mics,1)));

    % Define sources positions

    count = randi([counts(1) counts(2)]);
    
    while true
      
        srcs = zeros(count,3);
        for iSrc = 1:1:count
            while true
                src = [ uniform(margin, room_X - margin) uniform(margin, room_Y - margin) uniform(margin, room_Z - margin) ];
                r = norm(src-mic0);
                if (r >= dists(1)) && (r <= dists(2))
                    break
                end
            end
            srcs(iSrc,:) = src;
        end

        srcsNorm = srcs - ones(size(srcs,1),1) * mic0;
        micsNorm = mics - ones(size(mics,1),1) * mic0;
        srcsNorm = srcsNorm ./ (sqrt(sum(srcsNorm.^2,2)) * ones(1,3));    
        taus = (fs/speed) * (micsNorm * srcsNorm');

        dtaus = max(max(abs(taus - taus(:,1) * ones(1,size(taus,2)))));
        
        if dtaus >= dtdoa
            break
        end
    
    end
    
    % Define noise level
    
    noise = uniform(noises(1), noises(2));
    
    params = {};
    params.room = room;
    params.beta = beta;
    params.speed = speed;
    params.fs = fs;
    params.mics = mics;
    params.srcs = srcs;
    params.noise = noise;
  
end

function value = uniform(minValue, maxValue)
  
    value = rand(1) * (maxValue - minValue) + minValue;
  
end

function R = rotate(yaw, pitch, roll)
  
    alpha = 2 * pi * yaw / 360;
    beta = 2 * pi * pitch / 360;
    gamma = 2 * pi * roll / 360;

    Rx = [ 1 0 0 ; 0 cos(gamma) -sin(gamma) ; 0 sin(gamma) cos(gamma) ];
    Ry = [ cos(beta) 0 sin(beta) ; 0 1 0 ; -sin(beta) 0 cos(beta) ];
    Rz = [ cos(alpha) -sin(alpha) 0 ; sin(alpha) cos(alpha) 0 ; 0 0 1 ];

    R = Rz * Ry * Rx;

end
