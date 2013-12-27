source("radar.R")

roll_call <- build_rollcall('sen2005-2006.csv', 'Brazilian Senate 2005-2006')
radar_pca <- radarpca(roll_call, lop = -1, minvotes = 0)
plot_radar_black_and_white(radar_pca)
plot_radar(radar_pca)


