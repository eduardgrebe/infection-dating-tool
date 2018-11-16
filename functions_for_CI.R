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


sigma_tree <- function(alpha, sigma) {
  delta <- 2*sigma
  var <- sigma^2
  (2+(-2-alpha*delta*(2+alpha*delta))*exp(-alpha*delta)) / ( alpha^2 * (1 - exp(-alpha*delta))) - var
}

sigma <- 5
delta <- 2 * sigma
alpha <- uniroot(f = sigma_tree, lower = 1/(10*sigma), upper = 5*(1/sigma), sigma = sigma)$root


plot(x = seq(-15,15,0.1),f(seq(-15,15,0.1), alpha, delta), type = "l")


F <- function(t, alpha, delta) {
  if(t<=0 & t>= -delta) {
    A <- delta * (1-1/(1-exp(-alpha*delta))) - (exp(-alpha*delta))/((1-exp(-alpha*delta)*alpha))
    B <- 1-1/(1-exp(-alpha*delta))
    C <- 1/((1-exp(-alpha*delta) * alpha))
    return(A + B*t + C*exp(alpha*t))
  }
}


