f_left <- function(t, scale, delta) {
  return((1 - (1-exp(scale*t))/(1-exp(-scale*delta)))/2)
}

f <- function(t, t_centre=0, scale, delta) {
  t <- t-t_centre
  rv <- 
    ifelse(t < -delta, 
           0, 
           ifelse(t > delta,
                  1,
                  ifelse(t<=0,
                         f_left(t,scale,delta),
                         1-f_left(-t,scale,delta)))
           )
     
  return(rv)
}

g <-function(t, t_centre, scale, delta) {
  f(t_centre-t, scale = scale, delta = delta)
}

sigma_tree <- function(scale, sigma, d) {
  delta <- min(3*sigma,d)
  var <- sigma^2
  (2+(-2-scale*delta*(2+scale*delta))*exp(-scale*delta)) / ( scale^2 * (1 - exp(-scale*delta))) - var
}

likelihood <- function(t, t1 = 0, t2, scale1, delta1, scale2, delta2) {
  f(t = t, t_centre = t1, scale = scale1, delta = delta1) * g(t = t, t_centre = t2, scale = scale2, delta = delta2)
}

find_scale_delta <- function(d, sigma) {
  if ((delta <- 3*sigma) < d) {
    #delta <- 3*sigma
    scale <- 1.195554/sigma  
  } else {
    delta <- d
    scale <- uniroot(f = sigma_tree, lower = 1/(10*sigma), upper = 10*(1/sigma), sigma = sigma, d = d)$root
  }
  return(c(delta = delta, scale = scale))
}


t1 <- 0
d1 <- 15
sigma1 <- 0.2*d1
delta1 <- find_scale_delta(d = d1, sigma = sigma1)[[1]]
scale1 <- find_scale_delta(d = d1, sigma = sigma1)[[2]]

t2 <- 25
d2 <- 13
sigma2 <- 0.2*d2
delta2 <- find_scale_delta(d = d2, sigma = sigma2)[[1]]
scale2 <- find_scale_delta(d = d2, sigma = sigma2)[[2]]

plot(x = seq(-20,50,0.1), 
     y = likelihood(t = seq(-20,50,0.1), t1 = t1, t2 = t2, 
                    scale1 = scale1, delta1 = delta1, 
                    scale2 = scale2, delta2 = delta2), type = "l")




const <- cubature::adaptIntegrate(f = likelihood,
                                  lowerLimit = t1-2*delta1,
                                  upperLimit = t2+2*delta2,
                                  t1 = t1,
                                  t2 = t2,
                                  scale1 = scale1,
                                  delta1 = delta1,
                                  scale2 = scale2,
                                  delta2 = delta2)$integral

posterior_density_prop <- function(t, t1, t2, scale1, delta1, scale2, delta2, const = NULL) {
  prop <- cubature::adaptIntegrate(f = likelihood,
                                   lowerLimit = t1-delta1,
                                   upperLimit = t,
                                   t1 = t1,
                                   t2 = t2,
                                   scale1 = scale1,
                                   delta1 = delta1,
                                   scale2 = scale2,
                                   delta2 = delta2)$integral/const
  return(prop)
}

posterior_tree <- function(t, t1, t2, scale1, delta1, scale2, delta2, const = NULL, p = 0.025) {
  prop <- posterior_density_prop(t = t,
                                   t1 = t1,
                                   t2 = t2,
                                   scale1 = scale1,
                                   delta1 = delta1,
                                   scale2 = scale2,
                                   delta2 = delta2,
                                 const = const)
  return(prop - p)
}

find_ci_limits <- function(t1, t2, scale1, delta1, scale2, delta2, const = const, alpha = 0.05) {
  ci.lb <- uniroot(f = posterior_tree, lower = t1- 2 * delta1, upper = t2 + 2 * delta2, t1 = t1, t2 = t2, scale1 = scale1, delta1 = delta1, scale2 = scale2, delta2 = delta2, const = const, p = alpha/2)$root
  ci.ub <- uniroot(f = posterior_tree, lower = t1- 2 * delta1, upper = t2 + 2 * delta2, t1 = t1, t2 = t2, scale1 = scale1, delta1 = delta1, scale2 = scale2, delta2 = delta2, const = const, p = 1 - alpha/2)$root
  return(list(CI.LB = ci.lb, CI.UB = ci.ub))
}


find_ci_limits(t1, t2, scale1, delta1, scale2, delta2, const = const, alpha = 0.05)





# Testing stuff - ignore
posterior_density_prop(t = 47, t1 = 0, t2 = 30, 
                       scale1 = scale1, delta1 = delta1, 
                       scale2 = scale2, delta2 = delta2, const = const)


posterior_tree(t = 47, t1 = 0, t2 = 30, 
               scale1 = scale1, delta1 = delta1, 
               scale2 = scale2, delta2 = delta2,
               const = const, p = 0.025)


t1 <- 0
d1 <- 15
sigma1 <- 2
delta1 <- min(3*sigma1,d1)
scale1 <- uniroot(f = sigma_tree, lower = 1/(10*sigma1), upper = 5*(1/sigma1), sigma = sigma1, d = d1)$root
print(scale1)
test <- cubature::adaptIntegrate(f = likelihood,
                                 lowerLimit = t1-delta1,
                                 upperLimit = t1+delta1,
                                 t1 = t1,
                                 t2 = t2,
                                 scale1 = scale1,
                                 delta1 = delta1,
                                 scale2 = scale2,
                                 delta2 = delta2)$integral
print(test)
sigma1 <- 5
delta1 <- min(3*sigma1,d1)
scale1 <- uniroot(f = sigma_tree, lower = 1/(10*sigma1), upper = 5*(1/sigma1), sigma = sigma1, d = d1)$root
print(scale1)
test <- cubature::adaptIntegrate(f = likelihood,
                                 lowerLimit = t1-delta1,
                                 upperLimit = t1+delta1,
                                 t1 = t1,
                                 t2 = t2,
                                 scale1 = scale1,
                                 delta1 = delta1,
                                 scale2 = scale2,
                                 delta2 = delta2)$integral
print(test)
