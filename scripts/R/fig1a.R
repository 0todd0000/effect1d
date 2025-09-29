

# preliminaries:
rm( list = ls() ) # clear workspace
graphics.off()    # close all graphics
library(ggplot2)
fpath <- file.path(  dirname( sys.frame(1)$ofile ) , "effect_size_functions.R")
source( fpath )



# specify constants
### published Cohen's d interpretations (Sawilowsky, 2009)
d.labels.i <- c("Very small", "Small", "Medium", "Large", "Very large", "Huge")
d.values.i <- c(0.01, 0.2, 0.5, 0.8, 1.2, 2.0)
### d ranges for theoretical "t" and simulation "s" cases 
d.values.t <- seq(0.01, 2, length.out=51)
# d.values.s <- seq(0.01, 1.9, length.out=15)
### sample sizes (group size)
nn         <- c(10, 30, 100)

# calculate theoretical probabilities for interpretation values
p1         <- p.d.two.sample(d.values.i, nn[1])
p2         <- p.d.two.sample(d.values.i, nn[2])
p3         <- p.d.two.sample(d.values.i, nn[3])

# calculate theoretical probabilities (finer d scale)
p1t        <- p.d.two.sample(d.values.t, nn[1])
p2t        <- p.d.two.sample(d.values.t, nn[2])
p3t        <- p.d.two.sample(d.values.t, nn[3])



# simulations
rng1 <- function(){
    return( rnorm(nn[1]) )
}
rng2 <- function(){
    return( rnorm(nn[2]) )
}
rng3 <- function(){
    return( rnorm(nn[3]) )
}
# run simulation:
set.seed(3)
nsim       <- 500
u.sim      <- seq(0.01, 2, length.out=15)
d1.sim     <- sim.two.sample(rng1, cohen.d.two.sample, nsim)
d2.sim     <- sim.two.sample(rng2, cohen.d.two.sample, nsim)
d3.sim     <- sim.two.sample(rng3, cohen.d.two.sample, nsim)
# calculate survival functions:
sf1.sim    <- sim.sf(d1.sim, u.sim)
sf2.sim    <- sim.sf(d2.sim, u.sim)
sf3.sim    <- sim.sf(d3.sim, u.sim)



# build data frames for plotting:
d          <- d.values.i
df         <- data.frame(d, p1, p2, p3)
d          <- d.values.t
dft        <- data.frame(d, p1t, p2t, p3t)
df.sim     <- data.frame(u.sim, sf1.sim, sf2.sim, sf3.sim)



# plot
colors <- c('#348ABD', '#A60628', '#7A68A6')
vals   <- c("Theoretical (N= 10)"=colors[1], "Theoretical (N= 30)"=colors[2], "Theoretical (N=100)"=colors[3])
ggplot() +
    geom_line(data=dft,  aes(x=d, y=p1t, color="Theoretical (N= 10)"), linewidth=2 ) +
    geom_line(data=dft,  aes(x=d, y=p2t, color="Theoretical (N= 30)"), linewidth=2 ) +
    geom_line(data=dft,  aes(x=d, y=p3t, color="Theoretical (N=100)"), linewidth=2 ) +
    geom_point(data=df,  aes(x=d, y=p1), color=colors[1], size=4 ) +
    geom_point(data=df,  aes(x=d, y=p2), color=colors[2], size=4 ) +
    geom_point(data=df,  aes(x=d, y=p3), color=colors[3], size=4 ) +
    geom_point(data=df.sim, aes(x=u.sim, y=sf1.sim), color=colors[1], size=2, shape=21, fill="white" ) +
    geom_point(data=df.sim, aes(x=u.sim, y=sf2.sim), color=colors[2], size=2, shape=21, fill="white" ) +
    geom_point(data=df.sim, aes(x=u.sim, y=sf3.sim), color=colors[3], size=2, shape=21, fill="white" ) +
    scale_color_manual(values = vals) +
    xlab("Cohen's d") +
    ylab("Probability") +
    ylim(0, 1) +
    ggtitle(  "Sample size (N) dependence;  M=1"  ) +
    annotate("label", x=df$d[1]+0.05, y=df$p1[1]+0.00, label=d.labels.i[1], hjust=0) +
    annotate("label", x=df$d[2]+0.05, y=df$p1[2]+0.00, label=d.labels.i[2], hjust=0) +
    annotate("label", x=df$d[3]+0.05, y=df$p1[3]+0.00, label=d.labels.i[3], hjust=0) +
    annotate("label", x=df$d[4]+0.05, y=df$p1[4]+0.00, label=d.labels.i[4], hjust=0) +
    annotate("label", x=df$d[5]+0.05, y=df$p1[5]+0.00, label=d.labels.i[5], hjust=0) +
    annotate("label", x=df$d[6]+0.05, y=df$p1[6]+0.00, label=d.labels.i[6], hjust=0) +
    theme(
        legend.position = c(0.8, 0.4),
        legend.title=element_blank(),
        axis.text=element_text(size=10),
        axis.title=element_text(size=16),
        )



