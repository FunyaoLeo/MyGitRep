function [p] = PlotImage(f)

p = image(repmat(reshape(f,10,10)*255,1,1,3));
