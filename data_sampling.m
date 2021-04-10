%Ayana Mussabayeva
%Preprocessing P300 EEG data
%   Loading P300-Speller EEG data and saving every target/non-target as individual csv file


N = 8;  %Number of EEG data

%loop to preprocess every single dataset and save every 
for i=1:1:N
    
    loadName = sprintf('S%d.mat', i);
    load(loadName)                      
    
    starttime = -100;                %in ms after stimuli 
    endtime = 700;                  %in ms after stimuli 
    
    samples = ((endtime-starttime)/4)+1;    %calculating number of samples
    
    t_trig1 = find(trig == 1);              %find targets
    
    p300target(1:150,1:samples) = zeros;    %preparing p300matrix

    for x=1:1:150                          
         %create area around every target(in samples)
        p300target(x,1:samples) = t_trig1(x)+starttime*(fs/1000) : 1 : t_trig1(x)+endtime*(fs/1000);
     
        ytarget(1:samples,1:8) = y(p300target(x,1:samples) , 1:8);    %y-values in target area
     
        saveName = sprintf('S%d_target%d.csv', i, x);
        writematrix(ytarget,saveName)                           %write to csv
        
    end
    
    
    %same for non-targets
    t_trig2 = find(trig == -1);       
    
    p300nontarget(1:210,1:samples) = zeros;
    
    for x=5:5:1050                      
        p300nontarget(x,1:samples) = t_trig2(x)+starttime*(fs/1000) : 1 : t_trig2(x)+endtime*(fs/1000);
     
        ytarget(1:samples,1:8) = y(p300nontarget( x , 1:samples) , 1:8);
     
        saveName = sprintf('S%d_non-target%d.csv', i, x);
        writematrix(ytarget,saveName)
    end
    
end