% WB ver
% if a region has less than certain number of pixels,mark it as background.
function slice=fill_small_region(slice,thres)
u=unique(slice);
% remove bg: pixels marked 0
idx=u==0;
u(idx)=[];

for i=1:length(u)
    idx=slice==u(i);
    if sum(idx(:))<thres
        slice(idx)=0;
    end
end

end