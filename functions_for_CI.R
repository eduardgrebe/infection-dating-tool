f_left <- function(t, alpha, delta) {
  return((1 - (1-exp(alpha*t))/(1-exp(-alpha*delta)))/2)
}

f <- function(t, alpha, delta) {
  rv <- 
    ifelse(t < -delta, 
           0, 
           ifelse(t > delta,
                  1,
                  ifelse(t<=0,
                         f_left(t,alpha,delta),
                         1-f_left(-t,alpha,delta)))
           )
     
  return(rv)
}

sigma_tree <- function(alpha, sigma, d) {
  delta <- min(3*sigma,d)
  var <- sigma^2
  (2+(-2-alpha*delta*(2+alpha*delta))*exp(-alpha*delta)) / ( alpha^2 * (1 - exp(-alpha*delta))) - var
}

d <- 15
sigma <- 0.4*d
delta <- min(3*sigma,d)
alpha <- uniroot(f = sigma_tree, lower = 1/(10*sigma), upper = 5*(1/sigma), sigma = sigma, d = d)$root


plot(x = seq(-20,20,0.1),f(seq(-20,20,0.1), alpha, delta), type = "l")


cubature::adaptIntegrate(f = f, lowerLimit = -delta, upperLimit = delta, alpha = alpha, delta = delta)








# forget this
F <- function(t, alpha, delta) {
  if(t<=0 & t>= -delta) {
    A <- delta * (1-1/(1-exp(-alpha*delta))) - (exp(-alpha*delta))/((1-exp(-alpha*delta)*alpha))
    B <- 1-1/(1-exp(-alpha*delta))
    C <- 1/((1-exp(-alpha*delta) * alpha))
    return(A + B*t + C*exp(alpha*t))
  }
}


