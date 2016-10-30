% wb ver
data_dir ='/tempspace/wbian/flyem/validation_sample';
data_file=[data_dir filesep 'imgdata_ds.h5'];
label_file=[data_dir filesep 'label3d_ds_boundary.h5'];

% saving dataset name
d_loc = '/data';
l_loc = '/label';

% read raw data.
raw_data=h5read(data_file,'/data');
raw_data=permute(raw_data,[2 1 3]);
raw_label=h5read(label_file,'/label');
raw_label=permute(raw_label,[2 1 3]);

% dr=255; % data range.
% raw_data=raw_data/dr;
% disp(['assuming the data range is:',num2str(dr)]);

%%  ---------------next 100 stacks for training set ------------------------
data =single(raw_data(:,:,:));
labels =single(raw_label(:,:,:));

[data,labels]=augment_data(data,labels);
disp('data augmentation done.');
for i=1:length(data)
  d_tr=data{i};  l_tr=labels{i};
  d_tr=permute(d_tr,[2,1,3]); l_tr=permute(l_tr,[2,1,3]); % make the rotation so in python each figure is in right rotation.
  disp(['writing V' num2str(i) ' train file ...'])
  fname=[data_dir filesep 'val_ds' num2str(i) '.h5'];
  hdf5write(fname,d_loc,d_tr,l_loc,l_tr);
end


%% validation stacks -------------------------------------------------------
% 
% d_tr =single(raw_data(:,:,201:250));
% l_tr =single(label(:,:,201:250));
% %d_tr=permute(d_tr,[3 2 1]);
% %l_tr=permute(l_tr,[3 2 1]);
% 
% [data,labels]=augment_data(d_tr,l_tr);
% for i=1:length(data)
%   d_tr=data{i};  l_tr=labels{i};
%   d_tr=permute(d_tr,[3,1,2]); l_tr=permute(l_tr,[3,1,2]);
%   disp(['writing V' num2str(i) ' valid file ...'])
%   fname=[data_dir filesep 'train2_val' num2str(i) '.h5'];
% %   h5create(fname,d_loc,size(d_tr));
% %   h5write(fname,d_loc,d_tr);
% %   h5create(fname,l_loc,size(d_tr));
% %   h5write(fname,l_loc,l_tr);
%   hdf5write(fname,d_loc,d_tr,l_loc,l_tr);
% %   hdf5write(fname,l_loc,l_tr);
% end


%% ----------------- full test stack  ------------------------------------
% %test_data_file=[data_dir filesep 'sample_B+_20160601.hdf'];
% %raw_data=h5read(test_data_file,'volumes/raw');
% %label=raw_data;
% %d_te =single(raw_data);
% %l_te =single(label);
% 
% d_te = single(raw_data(:,:,151:200));
% l_te = single(label(:,:,151:200));
% %d_te=permute(d_te,[3 2 1]);
% %l_te=permute(l_te,[3 2 1]);
% 
% 
% [data,labels]=augment_data(d_te,l_te);
% for i=1:length(data)
%   d_te=data{i};
%   l_te=labels{i};
%   disp(['writing V' num2str(i) ' test file ...'])
%   fname=[data_dir filesep 'train2_test' num2str(i) '.h5'];
% %   h5create(fname,d_loc,size(d_te));
% %   h5write(fname,d_loc,d_te);
% %   h5create(fname,l_loc,size(d_te));
% %   h5write(fname,l_loc,l_te);
%   hdf5write(fname,d_loc,d_te,l_loc,l_te);
% %   hdf5write(fname,l_loc,l_tr);
% end

% savefile=[save_dir filesep 'snemi3d_test_v8.mat'];
% save(savefile,'data','-v7.3');
% h5write([save_dir filesep 'snemi3d_test_last10slice.h5'],d_details,d_te);
