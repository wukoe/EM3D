% WB ver.
% 
function prob=combinePredictionVolume(folder_name, save_h5_mat)%, threshold)
if ~exist(folder_name,'dir')
	disp(['Can''t find folder:  ' folder_name]);
	return
end
a = dir([folder_name filesep '*.h5']);
names={a.name};
f_idx=cellfun(@(x) x(end)=='5',names,'UniformOutput',false); % give list of boolean whether each file is h5 file.

f_idx=[f_idx{:}];
name_temp=names{f_idx};
name_temp = name_temp(1:end-4);

% tiff_file_save = strcat(folder_name, filesep,'prediction_result.tif');
% delete(tiff_file_save); wb

% Get data set information (value range, size)
mx=0; % max of data range.
for k = 1:length(f_idx)
    filename = strcat(folder_name, filesep, name_temp, num2str(k-1),'.h5');
    temp1 = hdf5info(filename);
    b = hdf5read(temp1.GroupHierarchy.Datasets); % b is reading the data
	mx_s=length(size(b)); % data dimension

    if mx_s==4 
        b = b(:,:,:,2); % old:b(1,:,:,2)
        mx_c=max(max(max(b)));
	elseif mx_s==3
        b = b(:,:,2);
        mx_c=max(max(b));
    end    
    
	if mx<mx_c
		mx=mx_c;
	end
end
% width=size(b,1);
% height=size(b,2);
% znum=size(b,3);

% probability map of each file
% prob=zeros(width,height,length(f_idx)); %for 2D
for k =  0: length(f_idx)-1
	filename = strcat(folder_name, filesep, name_temp, num2str(k),'.h5');
    temp1 = hdf5info(filename);
    b = hdf5read(temp1.GroupHierarchy.Datasets);
	mx_s=length(size(b));

	if mx_s==4
        b = squeeze(b(:,:,:,2));
	elseif mx_s==3
        b = b(:,:,2);
	end
% 	prob(:,:,k+1)=b;
    prob=b;
% 	im=255-uint8(b*(255/mx));
% 	imwrite(im,tiff_file_save,'WriteMode','append');
% 	disp(['write #' num2str(k) '  image ... ' tiff_file_save]);
end

if nargin>1 && save_h5_mat==true
    mat_file=[folder_name filesep 'prob.mat'];
    h5_file=[folder_name filesep 'prob.h5'];
    save(mat_file,'prob')

    p_details.location = '/';
    p_details.Name = 'probabilities';
    hdf5write(h5_file,p_details,prob);
end

end