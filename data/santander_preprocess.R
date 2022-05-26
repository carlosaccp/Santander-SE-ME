# Title:        Some preprocessing on the Santander Bikes data
# Author:       Francesco Sanna Passino
# Affiliation:  Department of Mathematics, Imperial College London
# Email:        f.sannapassino@imperial.ac.uk

## Empty list object
weekly_data = list()
## List all the .csv file names (and sort them in case they are not ordered by number)
file_names = sort(list.files('~/Documents/github/bikes_library/data/santander_summaries/', pattern='.csv'))
## file_names = file_names[which(grepl('256',file_names)):which(grepl('261',file_names))]
file_names = file_names[which(grepl('221', file_names)):which(grepl('236', file_names))]
start_day = as.Date(strsplit(strsplit(file_names[1], '_')[[1]][2], '-')[[1]][1], '%d%b%Y')
## Total number of files
n_weeks = length(file_names)

## Import
weekly_data = list()
for(week in 1:n_weeks){
  weekly_data[[week]] = read.table(paste('~/Documents/github/bikes_library/data/santander_summaries/',
                                         file_names[week],sep=''), sep=',', header=FALSE, 
                                   col.names=c('start_id','end_id','start_time','duration'))
}
library(dplyr)
df = dplyr::bind_rows(weekly_data)
df = transform(df, end_time = start_time + duration)

## Import stations
stations = read.table('~/Documents/github/bikes_library/data/santander_locations.csv', sep=',', header=TRUE)

## Calculate geodesic distance
library(geodist)
distances = geodist(stations[,c('longitude','latitude')], measure='vincenty') / 1000
## Station IDs
xx = numeric(max(stations$Station.Id))
for(i in 1:length(xx)){
  kk = which(stations$Station.Id == i)
  if(length(kk) > 0){
    xx[i] = kk
  }
}
## Distances
vv = apply(df, MARGIN=1, FUN=function(x) distances[xx[x[1]], xx[x[2]]])
df = transform(df, dist=vv)
