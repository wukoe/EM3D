% WB ver
% replace pixels with mode (most frequent element) in its vicinity (3x3
% neighborhood in case of 2D image, 3x3x3 in case of 3D volume)
function im=ReplacePixelsWithMode(im, index)
sz=size(im);
if length(sz)==2 % For 2D image
    pad = padarray(im, [1 1]); % adding zero padding around im.
    pad(pad==0) = NaN;
    c = im2col(pad, [3 3], 'sliding');%convert block(size 3x3) to column of c.
    pc = reshape(index,[1,prod(sz)]);
    c = c(:,pc);
else % For 3D volumn
    pad = padarray(im, [1,1,1]);
    pad(pad==0) = NaN;
    c = vol2col(pad,[3,3,3],index);
end

md = mode(c); %md= most frequent element in each block
md(isnan(md)) = 0;
im(index) = md; % put these most frequent element back to original array

end