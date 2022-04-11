clear all
close all
clc


td_data = load_atis_data('triangle_2_50_all_td.dat',0, 0);

% the camera has 480x360 pixels (x,y). td_data.x goes from 0 to 359
% td_data.ts contains the time stamp of the events (in us)
% td_data.p contains the polarity of the events (+/- 1)

pc1=pointCloud([td_data.ts/1e3 td_data.x td_data.y ],'Intensity',td_data.p);

figure
pcshow(pc1)
%% Zoom-in to see the events of interest

tM=max(td_data.ts);
nb_bins=1e3;
time_vec=linspace(0,tM,nb_bins)';
H=hist(td_data.ts,time_vec);

figure
plot(time_vec,H)
xlabel('Time (us)')
ylabel('Events')
%%
fp=fopen('triangle_all.txt','w');
for i=1:length(td_data.ts)
    fprintf(fp,'%d,',td_data.ts(i));
    fprintf(fp,'%d,',td_data.x(i));
    fprintf(fp,'%d,',td_data.y(i));
    fprintf(fp,'%d\n',td_data.p(i));
    
end
fclose(fp);



