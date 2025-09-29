
# preliminaries:
rm( list = ls() ) # clear workspace
graphics.off()    # close all graphics
library(ggplot2)
fpath <- file.path(  dirname( sys.frame(1)$ofile ) , "effect_size_functions.R")
source( fpath )



# generate random samples and calculate effect size:
set.seed(1)
n      <- 8    # sample size (single group)
Q      <- 101  # number of domain points
nbasis <- 6    # number of basis functions
norder <- 3    # bspline order
y1     <- rnorm.1d(n, Q, nbasis, norder)  # random functions
y2     <- rnorm.1d(n, Q, nbasis, norder)  # random functions
d1     <- abs( cohen.d.two.sample(y1, y2) )      # Cohen's d



# repeat for rougher functions:
set.seed(2)
nbasis <- 26   # number of basis functions
y1     <- rnorm.1d(n, Q, nbasis, norder)  # random functions
y2     <- rnorm.1d(n, Q, nbasis, norder)  # random functions
d2     <- abs(cohen.d.two.sample(y1, y2))      # Cohen's d



# assemble data frames:
x      <- seq(0, 1, length.out = Q)  # domain position
df1    <- data.frame(x, d1)
df2    <- data.frame(x, d2)



# plot:
colors <- c('black', 'blue')
vals   <- c("FWHM=25"=colors[1], "FWHM=5"=colors[2])
ggplot() +
    geom_line( data=df1,   aes(x=x, y=d1, color="FWHM=25" ), linewidth=2 ) +
    geom_line( data=df2,   aes(x=x, y=d2, color="FWHM=5" ), linewidth=2 ) +
    scale_color_manual(values = vals) +
    xlab("Domain position") +
    ylab("Cohen's d-value") +
    ggtitle(  "Absolute effect size"  ) +
    theme(
        legend.position = c(0.8, 0.85),
        legend.title=element_blank(),
        axis.text=element_text(size=10),
        axis.title=element_text(size=16),
        )
