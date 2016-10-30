function [D,L]=augment_data(x,y)
[D,L]=create8Variation(x,y);

%swap Z dimension
x=x(:,:,end:-1:1);
y=y(:,:,end:-1:1);
[data2,label2]=create8Variation(x,y);
D=[D; data2];
L=[L; label2];

end


function [D,L]=create8Variation(x,y)
% imgnum=size(x,3);
D=cell(8,1);
L=cell(8,1);
% data=zeros(size(x));
% label=zeros(size(y));

%    case 1
D{1}=x; L{1}=y;
%    case 2 
D{2} = flip(x,1); 	L{2}=flip(y,1);
%    case 3
D{3} = flip(x,2); 	L{3}=flip(y,2);
%case 4 rotate 90 in rotational axis, so counter-cloclwise.
% for k = 1:imgnum
%     data(:,:,k) = rot90(x(:,:,k));
%     label(:,:,k) = rot90(y(:,:,k));
% end
D{4} = rot90(x); 	L{4}=rot90(y);
%case 5
D{5} = rot90(x,-1); 	L{5}=rot90(y,-1);
%case 6
% for k = 1:imgnum
%     data(:,:,k) = rot90(flip(x(:,:,k), 1));
%     label(:,:,k) = rot90(flip(y(:,:,k), 1));
% end
D{6} = rot90(D{2}); 	L{6}=rot90(L{2});
%case 7
D{7} = rot90(D{3}); 	L{7}=rot90(L{3});
%case 8
D{8} = rot90(x,2); 	L{8}=rot90(y,2);

end