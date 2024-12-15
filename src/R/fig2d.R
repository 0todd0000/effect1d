
# preliminaries:
rm( list = ls() ) # clear workspace
graphics.off()    # close all graphics
library(ggplot2)
library(latex2exp)
fpath <- file.path(  dirname( sys.frame(1)$ofile ) , "effect_size_functions.R")
source( fpath )


# set main parameters
n       <- 10  # sample size (single group)
Q       <- 101 # number of domain points
fwhm0   <- 25  # smoothness (case 0)
fwhm1   <- 5   # smoothness (case 1)
nbasis0 <- 6   # approximately fwhm=25
nbasis1 <- 26  # approximately fwhm=5
norder  <- 3   # bspline order



# theoretical probabilities (d_max survival functions)
u       <- seq(0, 2.5, length.out=51)
sf0     <- rft.dmax.sf.two.sample(u, n, n, Q, fwhm0)
sf1     <- rft.dmax.sf.two.sample(u, n, n, Q, fwhm1)



# simulations
rng0 <- function(){
    return( rnorm.1d(n, Q, nbasis0, norder) )
}
rng1 <- function(){
    return( rnorm.1d(n, Q, nbasis1, norder) )
}
statfn.dmax <- function(y1, y2){
    return(   max( cohen.d.two.sample(y1, y2) )    )
}
# run simulation:
set.seed(3)
nsim     <- 500
u.sim    <- seq(0, 2.5, length.out=11)
dmax0    <- sim.two.sample(rng0, statfn.dmax, nsim)
dmax1    <- sim.two.sample(rng1, statfn.dmax, nsim)
sf0.sim  <- sim.sf(dmax0, u.sim)
sf1.sim  <- sim.sf(dmax1, u.sim)



# assemble data frames:
df0      <- data.frame(u, sf0)
df1      <- data.frame(u, sf1)
df0.sim  <- data.frame(u.sim, sf0.sim)
df1.sim  <- data.frame(u.sim, sf1.sim)



# plot:
colors <- c('black', 'blue')
vals   <- c("FWHM=25"=colors[1], "FWHM=5"=colors[2])
ggplot() +
    geom_line( data=df0,     aes(x=u, y=sf0, color="FWHM=25" ), linewidth=2 ) +
    geom_line( data=df1,     aes(x=u, y=sf1, color="FWHM=5" ), linewidth=2 ) +
    geom_point(data=df0.sim, aes(x=u.sim, y=sf0.sim), color=colors[1], size=3 ) +
    geom_point(data=df1.sim, aes(x=u.sim, y=sf1.sim), color=colors[2], size=3 ) +
    scale_color_manual(values = vals) +
    xlab("Threshold  [ u ] ") +
    ylab( TeX( r'($P(d_{max}>u)$)' )  ) +
    ggtitle(  "Effect size probabilities"  ) +
    theme(
        legend.position = c(0.8, 0.85),
        legend.title=element_blank(),
        axis.text=element_text(size=10),
        axis.title=element_text(size=16),
        )
