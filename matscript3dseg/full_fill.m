% WB ver
% Fill the zero pixels in the image
% x must not be uint type, in which the nan and 0 is the same.
function x=full_fill(x)
x=single(x);
sumz=sum(x(:)==0);
while(sumz > 0)
	x = ReplacePixelsWithMode(x, x==0);
    sumz=sum(x(:)==0);
%     disp(sumz);
end

end