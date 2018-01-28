function correctFieldMapJson(bids_dir,sub,ses)

if (exist('ses','var'))
sub_prefix=sprintf('%s_%s',sub,ses);
sub_path_prefix=sprintf('%s/%s',sub,ses);
sub_dir=sprintf('%s/%s/%s',bids_dir,sub_path_prefix);

else

sub_prefix=sprintf('%s',sub);
sub_path_prefix=sub_prefix;
sub_dir=sprintf('%s/%s',bids_dir,sub_path_prefix);


end

phasediff_json_file=sprintf('%s/fmap/%s_phasediff.json',sub_dir,sub_prefix);
mag1_json_file=sprintf('%s/fmap/%s_magnitude1.json',sub_dir,sub_prefix);
mag2_json_file=sprintf('%s/fmap/%s_magnitude2.json',sub_dir,sub_prefix);


%disp(phasediff_json_file);
%disp(mag1_json_file);
%disp(mag2_json_file);
%disp(rest_nii);


phasediff_json=loadjson(phasediff_json_file);
mag1_json=loadjson(mag1_json_file);
mag2_json=loadjson(mag2_json_file);

phasediff_json.EchoTime1=mag1_json.EchoTime;
phasediff_json.EchoTime2=mag2_json.EchoTime;
disp(sprintf('%s: EchoTime1=%f',phasediff_json_file,mag1_json.EchoTime));
disp(sprintf('%s: EchoTime2=%f',phasediff_json_file,mag2_json.EchoTime));

%apply to all bold images
all_bold=dir(sprintf('%s/%s/func/%s_*_bold.nii.gz',bids_dir,sub_prefix,sub_prefix));
Nbold=length(all_bold);
if (Nbold==1)
nii=sprintf('%s/func/%s',sub_path_prefix,all_bold(1).name);
disp(sprintf('%s: IntendedFor=%s',phasediff_json_file,nii));
phasediff_json.IntendedFor=nii;
else
% make a cell array
phasediff_json.IntendedFor=cell(1,length(all_bold));
for i=1:length(all_bold)
nii=sprintf('%s/func/%s',sub_path_prefix,all_bold(i).name);
disp(sprintf('%s: IntendedFor[%d]=%s',phasediff_json_file,i,nii));
phasediff_json.IntendedFor{i}=nii;
end

end



%need to add write permission before saving..
system(sprintf('chmod a+w %s',phasediff_json_file));
savejson('',phasediff_json,phasediff_json_file);
system(sprintf('chmod a-w %s',phasediff_json_file));


end