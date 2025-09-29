
# preliminaries:
rm( list = ls() ) # clear workspace
graphics.off()    # close all graphics
library(ggplot2)
fpath <- file.path(  dirname( sys.frame(1)$ofile ) , "effect_size_functions.R")
source( fpath )



# generate random samples and calculate means:
set.seed(1)
n      <- 8    # sample size (single group)
Q      <- 101  # number of domain points
nbasis <- 6    # number of basis functions
norder <- 3    # bspline order
y1     <- rnorm.1d(n, Q, nbasis, norder)  # random functions
y2     <- rnorm.1d(n, Q, nbasis, norder)  # random functions
m1     <- colMeans( y1 )  # sample mean
m2     <- colMeans( y2 )  # sample mean



# estimate FWHM:
#  THIS IS A HACK because I don't know how to control FWHM (or LKC)
#  with random function generators in R. This hack estimates FWHM
#  from a relatively large sample. The estimated FWHM is expected
#  to converge to the true population FWHM as the sample size grows,
#  similar to sample mean and variance estimates.
y     <- rnorm.1d(1000, Q, nbasis, norder)  # large sample
efwhm <- fwhm.estimate(y)  # estimated FWHM


# assemble data frames:
x      <- seq(0, 1, length.out = Q)  # domain position
df1    <- matrix2dataframe(y1)
df2    <- matrix2dataframe(y2)
df.m1  <- data.frame(x, m1)
df.m2  <- data.frame(x, m2)



# plot:
colors <- c('black', 'blue')
vals   <- c("Group 1 sample mean"=colors[1], "Group 2 sample mean"=colors[2])
ggplot() +
    geom_line( data=df1,   aes(x=x, y=y, group=i ), color=colors[1], linewidth=0.1 ) +
    geom_line( data=df2,   aes(x=x, y=y, group=i ), color=colors[2], linewidth=0.1 ) +
    geom_line( data=df.m1, aes(x=x, y=m1, color="Group 1 sample mean"), linewidth=2 ) +
    geom_line( data=df.m2, aes(x=x, y=m2, color="Group 2 sample mean"), linewidth=2 ) +
    # geom_line( data=df1, aes( x = q, y = y, group = variable ), colour = 'blue' )
    scale_color_manual(values = vals) +
    xlab("Domain position") +
    ylab("Dependent variable value") +
    ggtitle(  sprintf("Random functional dataset (FWHM=%.1f)", efwhm)  ) +
    theme(
        legend.position = c(0.7, 0.85),
        legend.title=element_blank(),
        axis.text=element_text(size=10),
        axis.title=element_text(size=16),
        )
    