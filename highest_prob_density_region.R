# Example 1 - moving bounds out

t1 <- 0
t2 <- 30
delta <- t2 - t1

t <- seq(t1-30,t2+30, length.out = 90)
pt <- c(rep(0,27),0.1,0.35,0.45,0.55,0.8,0.9,rep(1,24),0.9,0.8,0.55,0.45,0.35,0.1,rep(0,27))

p <- splinefun(x = t, y = pt, method = "monoH.FC")

tt<- seq(t1-30,t2+30,0.01)
plot(x = tt, p(x=tt), type = "l")

plot(x = tt, p(x=tt), type = "l")
ptt <- pmax(0, p(x=tt)) # normalize so prob >0
const <- sum(ptt)
sptt <- sort(ptt, decreasing = TRUE) / const
critp <- sptt[which(cumsum(sptt) >= 1-alpha)[1]] * const
abline(h=critp, col = "red", lty = 3)
abline(v=t1, col= "green")
abline(v=t2, col= "green")

posterior_minus_crit <- function(x, alpha=0.05, f = p2) {
  #browser()
  ptt <- pmax(0, f(tt)) # normalize so prob >0
  const <- sum(ptt)
  sptt <- sort(ptt, decreasing = TRUE) / const
  critp <- sptt[which(cumsum(sptt) >= 1-alpha)[1]] * const
  return(f(x) - critp)
}

CI.LB <- uniroot(posterior_minus_crit, interval = c(t1-delta,t1+delta/2))$root
CI.UB <- uniroot(posterior_minus_crit, interval = c(t2-delta/2,t2+delta))$root

plot(x = tt, p(x=tt), type = "l")
ptt <- pmax(0, p(x=tt)) # normalize so prob >0
const <- sum(ptt)
sptt <- sort(ptt, decreasing = TRUE) / const
critp <- sptt[which(cumsum(sptt) >= 1-alpha)[1]] * const
abline(h=critp, col = "red", lty = 3)
abline(v=t1, col= "green")
abline(v=t2, col= "green")
abline(v=CI.LB, col = "blue", lty = 3)
abline(v=CI.UB, col = "blue", lty = 3)




# Example 2 - moving bounds in
t1 <- 0
t2 <- 150
delta <- t2 - t1

t <- seq(t1-30,t2+30, length.out = 204)
pt <- c(rep(0,20),0.05,0.07,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.85,0.9,rep(1,136),0.9,0.85,0.8,0.7,0.6,0.5,0.4,0.3,0.25,0.2,0.15,0.1,0.07,0.05,rep(0,20))

p <- splinefun(x = t, y = pt, method = "monoH.FC")

tt<- seq(t1-30,t2+30,0.01)
plot(x = tt, p(x=tt), type = "l")


posterior_minus_crit <- function(x, alpha=0.05, f = p) {
  #browser()
  ptt <- pmax(0, f(tt)) # normalize so prob >0
  const <- sum(ptt)
  sptt <- sort(ptt, decreasing = TRUE) / const
  critp <- sptt[which(cumsum(sptt) >= 1-alpha)[1]] * const
  return(f(x) - critp)
}

CI.LB <- uniroot(posterior_minus_crit, interval = c(t1-delta,t1+delta/2))$root
CI.UB <- uniroot(posterior_minus_crit, interval = c(t2-delta/2,t2+delta))$root

plot(x = tt, p(x=tt), type = "l")
ptt <- pmax(0, p(x=tt)) # normalize so prob >0
const <- sum(ptt)
sptt <- sort(ptt, decreasing = TRUE) / const
critp <- sptt[which(cumsum(sptt) >= 1-alpha)[1]] * const
abline(h=critp, col = "red", lty = 3)
abline(v=t1, col= "green")
abline(v=t2, col= "green")
abline(v=CI.LB, col = "blue", lty = 3)
abline(v=CI.UB, col = "blue", lty = 3)
