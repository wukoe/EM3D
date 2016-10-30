
% hd_dir='../../hd5'
% data_dir='../../data'
% 
% 
% raw_file =[data_dir filesep  'sample_A+_20160601.hdf']; %'snems3d_train_old.mat';
% raw_data =h5read(raw_file,'/volumes/raw');
% %raw_data =permute(raw_data,[2 3 1]);
% 
% mat_test_file ='predict/ave_probs_test_A_iter_36000.mat';
% mat_test_deconv_1x3='../A_DeconvNet_3fm_1x3/predict/ave_probs_test_A_iter_36000.mat';
% %mat_test_deconv_3x3='../A_DeconvNet_3fm_1x3/predict/ave_probs_test_A_iter_36000.mat';
% %to add the above one
% mat_test_file_5fm_3x3='../A_InceptionSegNet_5fm_3x3/predict/ave_probs_test_A_iter_18000.mat';
% %mat_test_file_5fm_3x3='../A_InceptionSegNet_5fm_3x3/predict/ave_probs_test_A_iter_28000.mat';
% mat_test_file_1fm_1x3='../A_InceptionSegNet_1fm_1x3/predict/ave_probs_test_iter_20000.mat';
% %mat_test_file_1fm_1x3='../A_InceptionSegNet_1fm_1x3/predict/ave_probs_test_iter_36000.mat';
% mat_test_file_1fm_3x3='../A_InceptionSegNet_1fm_3x3/predict/ave_probs_test_iter_18000.mat';
% %mat_test_file_1fm_3x3='../A_InceptionSegNet_1fm_3x3/predict/ave_probs_test_iter_28000.mat';
% mat_test_file_3fm_1x3='../A_InceptionSegNet_3fm_1x3/predict/ave_probs_test_iter_20000.mat';
% mat_test_file_3fm_3x3='../A_InceptionSegNet_3fm_3x3/predict/ave_probs_test_iter_14000.mat';
% %mat_test_file_3fm_3x3='../A_InceptionSegNet_3fm_3x3/predict/ave_probs_test_iter_24000.mat';
% 
% 
% 
% 
% prob_mask_th=0.8;
% 
% load(mat_test_file);
% prob_test=1-average;
% 
% load(mat_test_deconv_1x3);
% prob_deconv_test=1-average;
% 
% load(mat_test_file_5fm_3x3);
% prob_test_5fm_3x3=1-average;
% 
% load(mat_test_file_1fm_1x3);
% prob_test_1fm_1x3=1-average;
% 
% 
% load(mat_test_file_1fm_3x3);
% prob_test_1fm_3x3=1-average;
% 
% 
% load(mat_test_file_3fm_1x3);
% prob_test_3fm_1x3=1-average;
% 
% load(mat_test_file_3fm_3x3);
% prob_test_3fm_3x3=1-average;
% 
% %fused_prob=max(max(prob_test,prob_deconv_test),prob_test_5fm_3x3);
% fused_prob1=max(max(max(prob_test,prob_deconv_test),prob_test_5fm_3x3),prob_test_1fm_1x3);
% fused_prob2=max(max(prob_test_1fm_3x3,prob_test_3fm_1x3),prob_test_3fm_3x3);
% fused_prob = max(fused_prob1,fused_prob2);
% 
% 
% 
% % h_fill = fspecial('Gaussian', [6 6], 1);
% % imhm_th_3d=0.01
% % disp('3D watershed ...')
% % L = watershed(imhmin(imfilter(fused_prob, h_fill), imhm_th_3d),6);

% above sealed by  WB

%% ------------- 3d filtering & 3d watershed ------------------------------
fused_prob=prob;

imhm_th_3d=0.048;
Gfilter = Gausfilter3D([5,5,5],0.7); %fspecial('Gaussian', [5,5], 0.5);
proc_prob = imhmin(imfilter(fused_prob, Gfilter), imhm_th_3d); %
disp('filter done');
seg_raw = watershed(proc_prob,6);
disp('watershed done');

% % ---watershed 1:80 and 81:end separetely as  80 and 81 slices do not align well--------------------
% % TODO: ---need a way to connect 80 and 81 slices
% BW_L = watershed(imhmin(imfilter(fused_prob(:,:,1:80), h_fill), imhm_th_3d),6);
% BW_L_2 =watershed(imhmin(imfilter(fused_prob(:,:,81:end), h_fill), 0.035),6);
% L_Seg=cat(3,BW_L,BW_L_2);
% %figure,imshow(label2rgb(BW_L(:,:,100),'jet','w','shuffle'))
% L_Seg(1249,:,:)=L_Seg(1248,:,:);
% L_Seg(1250,:,:)=L_Seg(1248,:,:);
% 
% L_Seg(:,1249,:)=L_Seg(:,1248,:);
% L_Seg(:,1250,:)=L_Seg(:,1248,:);


% % ------------------2d watershed -----------------------------------------------------
% imhm_th_2d=0.30;
% L_2d = watershed(imhmin(imfilter(fused_prob, h_fill), imhm_th_2d),8);
% figure,imshow(label2rgb(L(:,:,10),'jet','w','shuffle'))
% figure,imshow(label2rgb(L_2d(:,:,10),'jet','w','shuffle'))

%% %======================fill_small region with 0 for 2d =================
% sz=size(seg_raw);
% seg_raw=double(seg_raw);
% seg_sm_fill=zeros(sz);
% disp('smfill: ');
% for i=1:sz(3)
% 	 fprintf('|');
% 	 seg_sm_fill(:,:,i)=fill_small_region(seg_raw(:,:,i),10);
% end
% fprintf('\n');
% %
% 
% % %%================ remove background and fill =================================================
% 
% % L_fill=double(L);
%  % parfor i=1:size(L_fill,3)
% 	 % disp(['disp ' num2str(i)])
% 	 % f = full_fill(L_fill(:,:,i));
% 	 % out_map_fill(:,:,i)=f;
% % end

%% ================ remove background on final segmentation =================================================
% This section is to remove the white lines boarder between segments and leave pure
% segmentations.

% L_fill=double(seg_raw);
% seg_final=zeros(sz);
% disp('fullfill ')
% for i=1:sz(3)
%      fprintf('|');
% 	 seg_final(:,:,i) = full_fill(L_fill(:,:,i));
% end
% fprintf('\n');

seg_final=full_fill(seg_raw);
disp('filling done');

% if exist('raw_fuse_seg.tiff','file')
%    delete('raw_fuse_seg.tiff');
% end
% write_label2rgb_image(uint32(final_seg),raw_data,'raw_fuse_seg_018_prob');
% final_seg=uint64(final_seg);
% d_details.location = '/volumes/labels/';
% d_details.Name = 'neuron_ids';
% hdf5write('segmentation/seg_test_a_018_prob.h5',d_details, final_seg);
