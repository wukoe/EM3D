% fuse prediction results from augmented stacks
%  prob=de_augment_data(D,opt)
% opt={'max','avg'}
function prob=de_augment_data(D,opt)
% d_size=length(D);
prob1_sum=recoverAUGvariation(D(1:8));
prob1_sum=predfuse(prob1_sum,opt);

prob2_sum=recoverAUGvariation(D(9:16));
%sweep Z dimension
for k=1:length(prob2_sum)
    prob2_sum{k}=flip(prob2_sum{k},3);
end
prob2_sum=predfuse(prob2_sum,opt);

if strcmp(opt,'max')
    prob=max(prob1_sum,prob2_sum);
else
    prob=(prob1_sum+prob2_sum)/2;
end

end

function x=recoverAUGvariation(x)
%    case 1
% pass
%    case 2 
x{2} = flip(x{2},1);
%    case 3
x{3} = flip(x{3},2);
%case 4 rotate 90 in rotational axis, so counter-cloclwise.
x{4} = rot90(x{4},-1);
%case 5
x{5} = rot90(x{5},1);
%case 6
x{6} = flip(rot90(x{6},-1),1);
%case 7
x{7} = flip(rot90(x{7},-1),2);
%case 8
x{8} = rot90(x{8},2);

end

% Avareging data from multiple predictions.
function F=predfuse(D,opt)
F=D{1};
if strcmp(opt,'max')
    for k=2:length(D)
        F = max(F, D{k});
    end
else
    for k=2:length(D)
        F = F + D{k};
    end
    F = F/length(D);
end

end
