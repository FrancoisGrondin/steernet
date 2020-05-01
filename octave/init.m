root = argv(){1};
azs = 'a':'z';

for letter1 = azs  
    for letter2 = azs
        directory = [root letter1 "/" letter2 "/"];
        if ~exist(directory, 'dir')
            mkdir(directory);
        end    
    end
end

