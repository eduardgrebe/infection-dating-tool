f_left <- function(t, shape, delta) {
  return((1 - (1-exp(shape*t))/(1-exp(-shape*delta)))/2)
}

f <- function(t, t_centre=0, shape, delta) {
  t <- t-t_centre
  rv <- 
    ifelse(t < -delta, 
           0, 
           ifelse(t > delta,
                  1,
                  ifelse(t<=0,
                         f_left(t,shape,delta),
                         1-f_left(-t,shape,delta)))
           )
     
  return(rv)
}

g <-function(t, t_centre, shape, delta) {
  f(t_centre-t, shape = shape, delta = delta)
}

sigma_tree <- function(shape, sigma, d) {
  delta <- min(3*sigma,d)
  var <- sigma^2
  (2+(-2-shape*delta*(2+shape*delta))*exp(-shape*delta)) / ( shape^2 * (1 - exp(-shape*delta))) - var
}

likelihood <- function(t, t1 = 0, t2, shape1, delta1, shape2, delta2) {
  f(t = t, t_centre = t1, shape = shape1, delta = delta1) * g(t = t, t_centre = t2, shape = shape2, delta = delta2)
}


t1 <- 0
d1 <- 15
sigma1 <- 0.2*d1
delta1 <- min(3*sigma1,d1)
shape1 <- uniroot(f = sigma_tree, lower = 1/(10*sigma), upper = 5*(1/sigma), sigma = sigma1, d = d1)$root

t2 <- 30
d2 <- 10
sigma2 <- 0.3*d2
delta2 <- min(3*sigma2,d2)
shape2 <- uniroot(f = sigma_tree, lower = 1/(10*sigma), upper = 5*(1/sigma), sigma = sigma2, d = d2)$root

plot(x = seq(-15,45,0.1), 
     y = likelihood(t = seq(-15,45,0.1), t1 = 0, t2 = 30, 
                    shape1 = shape1, delta1 = delta1, 
                    shape2 = shape2, delta2 = delta2), type = "l")

posterior_density_prop <- function(t, t1, t2, shape1, delta1, shape2, delta2, debug = F) {
  if (debug) {browser()}
  const <- cubature::adaptIntegrate(f = likelihood,
                                    lowerLimit = t1-delta1,
                                    upperLimit = t2+delta2,
                                    t1 = t1,
                                    t2 = t2,
                                    shape1 = shape1,
                                    delta1 = delta1,
                                    shape2 = shape2,
                                    delta2 = delta2)$integral
  #like <- likelihood(t = t, t1=t1, t2=t2, shape1=shape1, delta1=delta1, shape2 = shape2, delta2=delta2)
  prop <- cubature::adaptIntegrate(f = likelihood,
                                   lowerLimit = t1-delta1,
                                   upperLimit = t,
                                   t1 = t1,
                                   t2 = t2,
                                   shape1 = shape1,
                                   delta1 = delta1,
                                   shape2 = shape2,
                                   delta2 = delta2)$integral/const
  return(prop)
}

posterior_tree <- function(t, t1, t2, shape1, delta1, shape2, delta2, p = 0.025) {
  prop <- posterior_density_prop(t = t,
                                   t1 = t1,
                                   t2 = t2,
                                   shape1 = shape1,
                                   delta1 = delta1,
                                   shape2 = shape2,
                                   delta2 = delta2)
  return(prop - p)
}

posterior_density_prop(t = 47, t1 = 0, t2 = 30, 
               shape1 = shape1, delta1 = delta1, 
               shape2 = shape2, delta2 = delta2)


posterior_tree(t = 47, t1 = 0, t2 = 30, 
                           shape1 = shape1, delta1 = delta1, 
                           shape2 = shape2, delta2 = delta2,
               p = 0.025)


find_ci_limits <- function(t1, t2, shape1, delta1, shape2, delta2, alpha = 0.05) {
  ci.lb <- uniroot(f = posterior_tree, lower = t1- 2 * delta1, upper = t2 + 2 * delta2, t1 = t1, t2 = t2, shape1 = shape1, delta1 = delta1, shape2 = shape2, delta2 = delta2, p = alpha/2)$root
  ci.ub <- uniroot(f = posterior_tree, lower = t1- 2 * delta1, upper = t2 + 2 * delta2, t1 = t1, t2 = t2, shape1 = shape1, delta1 = delta1, shape2 = shape2, delta2 = delta2, p = 1 - alpha/2)$root
  return(list(CI.LB = ci.lb, CI.UB = ci.ub))
}


find_ci_limits(t1, t2, shape1, delta1, shape2, delta2, alpha = 0.05)

