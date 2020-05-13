function figfull(img, cRange)

    c = [ 252 251 189 ; ...
          254 195 135 ; ...
          251 135  97 ; ...
          228  79 100 ; ...
          183  55 121 ; ...
          131  38 129 ; ...
           81  18 124 ; ...
           29  17  71 ; ...
            0   0   0 ];

    c = flipud(c) / 255;
    i = linspace(0,1,size(c,1));
    n = linspace(0,1,64);
    
    cR = interp1(i,c(:,1),n);
    cG = interp1(i,c(:,2),n);
    cB = interp1(i,c(:,3),n);
    
    c2 = [ cR' cG' cB' ];
    
    imagesc(img, cRange);
    colormap(c2);
    set(gcf,'Position',[100 100 500 100]);
    set(gca,'Position',[0 0 1 1]);
    set(gca,'xtick',[]);
    set(gca,'ytick',[]);
    
return    