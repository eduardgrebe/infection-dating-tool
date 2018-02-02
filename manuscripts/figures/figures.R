library(tidyverse)

ind_test_sensitivity <- function(t,scale,shape, position) {
  return(
    ifelse(t - position < 0, 0,
           1 - exp(-((t - position) / scale)^shape))
  )
}




plotdata <- data_frame(t = seq(0,25,0.1), 
                       p1 = ind_test_sensitivity(t = seq(0,25,0.1), scale = 3, shape = 4, position = 5),
                       p2 = ind_test_sensitivity(t = seq(0,25,0.1), scale = 3, shape = 4, position = 6),
                       p3 = ind_test_sensitivity(t = seq(0,25,0.1), scale = 3, shape = 4, position = 7))

plotdata %>%
  ggplot(data = .) + 
  geom_line(aes(x = t, y = p1), colour = "blue") + 
  geom_line(aes(x = t, y = p2), colour = "red") + 
  geom_line(aes(x = t, y = p3), colour = "green")



ind_likelihood_negative <- function(t,scale,shape, position) {
  return(
    ifelse(t - position < 0, 0,
           1 - exp(-((t - position) / scale)^shape))
  )
}

is.even <- function(x) x %% 2 == 0

generate_likelihoods_negative <- function(t, scale, shape, mean_position, sd_position, n) {
  #positions <- rnorm(n = n, mean = mean_position, sd = sd_position)
  positions[1] <- mean_position
  if (is.even(n)) {
    for (i in 2:n/2) {
      position[i] <- positions[i-1] + 1/pnorm(q = positions[i-1], mean = mean_position, sd = sd_position)
    }
  } else {stop("n must be even")}
  
  
  likelihoods <- matrix(nrow = length(t), ncol = n+1)
  likelihoods[,1] <- t
  for(i in 1:n) {
    likelihoods[,i+1] <- ind_likelihood_negative(t = t, scale = scale, shape = shape, position = positions[i])
  }
  likelihoods <- as_data_frame(likelihoods)
  colnames(likelihoods) <- c("t", paste("N",1:n, sep = ""))
  return(likelihoods)
}

df <- generate_likelihoods_negative(t = seq(0,25,0.1), scale = 7, shape = 4, mean_position = 6, sd_position = 4, n = 10)
  
plot_likelihoods_neg <- function(t, scale, shape, mean_position, sd_position, n) {
  likelihoods <- generate_likelihoods_negative(t = t, scale = scale, shape = shape, mean_position = mean_position, sd_position = sd_position, n = n)
  plot <- ggplot(data = likelihoods)
  cnames <- colnames(likelihoods)
  for (i in 2:n+1) {
    plot <- plot + geom_line(aes_string(x = "t", y = cnames[i]))
  }
  return(plot)
  }