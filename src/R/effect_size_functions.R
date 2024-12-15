


# ----- EFFECT SIZE (Cohen's d) FUNCTIONS ----- 

# Convert Cohen's d-values to t-values (two-sample case)
# 
# Inputs:
#   d: d-value(s)
#   n1: sample size (group 1)
#   n2: sample size (group 2)
#
d2t.two.sample <- function(d, n1, n2){
    t  <- d / sqrt(1/n1 + 1/n2)
    return( t )
}



# Convert t-values to Cohen's d-values (two-sample case)
# 
# Inputs:
#   t: t-value(s)
#   n1: sample size (group 1)
#   n2: sample size (group 2)
t2d.two.sample <- function(t, n1, n2){
    d  <- t * sqrt(1/n1 + 1/n2)
    return( d )
}



# Effect size (Cohen's d) for a two-sample test
# 
# Inputs:
#   y1: group 1 sample
#   y2: group 2 sample 
# 
# Outputs:
#   d: Cohen's d-value
# 
# Examples:
#   y1 <- rnorm(8)
#   y2 <- rnorm(8)
#   d  <- cohen.d.two.sample(y1, y2)
#   
#   y1 <- rnorm.1d(8, 101, 10, 3) # random functional data
#   y2 <- rnorm.1d(8, 101, 10, 3)
#   d  <- cohen.d.two.sample(y1, y2)
#
cohen.d.two.sample <- function(y1, y2){
    if( is.null( nrow(y1) ) ){
        y1 <- matrix(y1)
        y2 <- matrix(y2)
    }
    n1 <- nrow(y1);           n2 <- nrow(y2)
    m1 <- colMeans(y1);       m2 <- colMeans(y2)
    v1 <- apply(y1, 2, var);  v2 <- apply(y2, 2, var)
    sp <- sqrt(  (  (n1-1)*v1 + (n2-1)*v2  )  / (n1+n2-2)  )
    d  <- (m1 - m2) / sp
    return( d )
}



# Test statistic (t-value) for a two-sample test
# 
# Inputs:
#   y1: group 1 sample
#   y2: group 2 sample
# 
# Outputs:
#   t: test statistic value (t-value)
# 
# Examples:
#   y1 <- rnorm(8)
#   y2 <- rnorm(8)
#   d  <- t.two.sample(y1, y2)
#   
#   y1 <- rnorm.1d(8, 101, 10, 3) # random functional data
#   y2 <- rnorm.1d(8, 101, 10, 3)
#   d  <- t.two.sample(y1, y2)
#
t.two.sample <- function(y1, y2){
    if( is.null( nrow(y1) ) ){
        y1 <- matrix(y1)
        y2 <- matrix(y2)
    }
    n1 <- nrow(y1)
    n2 <- nrow(y2)
    d  <- cohen.d.two.sample(y1, y2)
    t  <- d / sqrt(1/n1 + 1/n2)
    return( t )
}




# Constrain corrected p-values to range [0, 1]
p.constrain <- function(p){
    return( max(0, min(1,p) ) )
}



# Probability (survival function) for maximum Cohen's d-value across m independent two-sample tests
# 
# Inputs:
#   d = maximum Cohen's d value across m independent tests
#   n = group size (total number of observations = 2*n)
#   m = (optional) number of independent tests (default: m=1)
# 
# OUTPUTS:
#   p-value
#
p.d.two.sample <- function(d, n, m){
    if( missing(m) ){
        m <- 1
    }
    v   <- 2*n - 2                 # degrees of freedom
    t   <- d / sqrt(1/n + 1/n)     # t-value
    pu  <- pt( t, v, lower=FALSE ) # uncorrected p-value
    p   <- 1 - (1 - pu)^m          # corrected p-value (Bonferroni)
    p   <- sapply(p, p.constrain)  # constrain to the range [0,1]
    return( p )
}









# ----- CONVENIENCE FUNCTIONS ----- 

# Flatten a 2D array of observations into a data frame
# 
# Inputs:
#   a: a (J,Q) array;  J = num. observations, Q = num. domain points
#
matrix2dataframe <- function(a){
    m <- nrow(a)
    n <- ncol(a)
    i <- replicate( n, seq(m) )
    x <- t( replicate( m, seq(0, 1, length.out = n) ) )
    # assemble data frame:
    x <- as.vector( x )
    y <- as.vector( a )
    i <- as.vector( i )
    return( data.frame(x, y, i) )
}




# ----- RANDOM FIELD THEORY FUNCTIONS ----- 

# Smoothness estimates (following Kiebel et al. 1999)
#
# Kiebel, S. J., Poline, J. B., Friston, K. J., Holmes, A. P.,
#    & Worsley, K. J. (1999). Robust smoothness estimation in
#     statistical parametric maps using standardized residuals
#     from the general linear model. Neuroimage, 10(6), 756-766.
#
fwhm.estimate <- function(r){
    ssq  <-  apply(r^2, 2, sum)
    grad <- pracma::gradient(r)
    v    <-  apply( grad$X^2, 2, sum)
    v    <- v / ssq
    reselsPerNode <- sqrt( v / (4*log(2)) )
    efwhm <- 1 / mean( reselsPerNode )  # estimated FHWM
}



# Random field theory (RFT) survival function for the maximum t-value
# 
# Inputs:
#   u: threshold
#   v: degrees of freedom
#   Q: number of domain points
#   fwhm: field smoothness
#
# From Worsley et al. (2004);  see Table 2 (page S191)
#
#    Worsley, K. J., Taylor, J. E., Tomaiuolo, F., & Lerch, J. (2004).
#    Unified univariate and multivariate random field theory.
#    Neuroimage, 23, S189-S195.
#
# A simplified version of the Worsley et al. (2004) equations
#    for a continuous (i.e., unbroken) one-dimensional domain
#    --- and the version that appears in the function below ---
#    is given in Eqn.3 from Pataky et al. (2016).
# 
#    Pataky, T. C., Vanrenterghem, J., & Robinson, M. A. (2016).
#    The probability of false positives in zero-dimensional analyses
#    of one-dimensional kinematic, force and EMG trajectories.
#    Journal of Biomechanics, 49(9), 1468-1476.
rft.tmax.sf <- function(u, v, Q, fwhm){
    sw <- (Q-1) / fwhm
    p  <- 1 - exp(   -(1-pt(u, v))  -sw * sqrt(4*log(2))/(2*pi)  * (1+u^2/v)^( -(v-1) / 2 )   )
    return( p )
}


# Random field theory (RFT) survival function for maximum Cohen's d-value
# 
# This is a simple sample size-based transformation of rmax.tmax.sf (above)
rft.dmax.sf.two.sample <- function(u, n1, n2, Q, fwhm){
    v <- n1 + n2 - 2
    t <- u / sqrt(1/n1 + 1/n2)
    p <- rft.tmax.sf(t, v, Q, fwhm)
    return( p )
}






# ----- SIMULATION FUNCTIONS ----- 

# random functional data (Gaussian)
rnorm.1d <- function( J=8, Q=101, nbasis=10, norder=4 ){
    library(fda)
    x       <- seq(0,1,length.out=Q)
    basis   <- create.bspline.basis(rangeval = c(0,1), nbasis=nbasis, norder=norder)
    coef    <- matrix( rnorm(J*nbasis), nbasis, J)
    fdobj   <- fd(coef, basis)
    y       <- eval.fd(x, fdobj)
    return( t(y) )
}


# Simulate random datasets
#
# Inputs:
#   rng: a random number generator function;  must be callable without inputs as "rng()"
#   statfn: a function that calculates a statistic from two samples
#   nsim: number of simulation iterations (i.e., random datasets)
#   
# Outputs:
#   z: statistic values (one for each simulation iteration)
#
sim.two.sample <- function(rng, statfn, nsim){
    z      <- matrix(nrow=nsim)  # calculated stat distribution across simulations
    for (i in 1:nsim){
        y1   <- rng()
        y2   <- rng()
        z[i] <- statfn(y1, y2)
    }
    return( z )
}



# Survival function (SF) for simulations
#
# Inputs:
#   z:  statistic values (calculated using sim.two.sample, for example)
#   u:  points (thresholds) at which to calculate the SF
#   
# Outputs:
#   p: survival function probabilities;  P(z>u)
#
sim.sf <- function(z, u){
    p <- matrix( nrow=length(u) )
    for (i in 1:length(u)){
        p[i] <- mean( z > u[i] )
    }
    return( p )
}





