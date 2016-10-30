data_dir='/tempspace/wbian/flyem/validation_sample/';
lb_file =[data_dir filesep  'label3d.h5'];
cutrange=250;

label=h5read(lb_file,'/label');
label=permute(label,[2,1,3]);
lb=label(1:cutrange,1:cutrange,1:cutrange);

%% load predict data
predictdata=[data_dir,'predict_single/predict01_shift_0.h5'];
prob=h5read(predictdata,'/data');
prob=prob(:,:,:,2);
prob=permute(prob,[2,1,3]);
prob=prob(1:cutrange,1:cutrange,1:cutrange);

% prob=h5read(mat_train_file_5fm,'/probability');

%%
fstd=0.2:0.1:0.9;
ths=0.01:0.002:0.04;
fa=length(fstd); tha=length(ths);
res=zeros(tha,fa);
for i=1:fa
%     h=fspecial('Gaussian', [5,5], hs(i)); % create 2D Gaussian filter of size[5,5] and std hs(i).
    ft=Gausfilter3D([5,5,5],fstd(i));
    
    parfor j=1:tha
        L = watershed(imhmin(imfilter(prob, ft), ths(j)),6); %
        L = single(L);
        % imfilter is 2d/3d filter.
        % imhmin is H-minima transform. IMHMIN(I,H) suppresses all minima in I whose depth is less than H.  I is an intensity image.
        % watershed(X,conn) conn is specified connected neighborhood, 6 means the 6 connected in 3D neighbourhood.
%         L=full_fill(L);
        res(j,i)=SNEMI3D_metrics(lb,L);
        display(sprintf('watershed threshold = %d, hs = %d, metric = %d', ths(j),fstd(i), res(j,i)));
    end
end




%L = watershed(imhmin(imfilter(prob, h), 0.086),6);
% lbs=label;
% lbs=permute(lbs,[2 3 1]);
% display(sprintf('watershed threshold = %d, metric = %d', th, SNEMI3D_metrics(lbs,L)));
% %[out_map,out_map_fill,L,ws]=watershed_post_processing(prob,'3d');
% display(sprintf('watershed threshold = %d, metric = %d', th, SNEMI3D_metrics(lbs,L)));
% %display(sprintf('outmap threshold = %d, metric = %d', th, SNEMI3D_metrics(label,out_map)));
