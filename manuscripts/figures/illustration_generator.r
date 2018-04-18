if(Sys.info()['login']=='eduardgrebe') {
  setwd("~/dev/infection-dating-tool/manuscripts/figures/")
} else if(Sys.info()['login']=='JumpCo Vostro3700') {
  setwd("C:/Users/JumpCo Vostro3700/desktop/infection-dating-tool/manuscripts/figures")
} else {
  setwd(".") #what does this do?
}
library("DescTools")
#Tool for generating plots that illustrate the value of the knowing the details of individual HIV detectability
#Initiated February 2018
#Code by Jeremy Bingham with Eduard Grebe and Alex Welte

#Definitions
# All test functions [unless specified otherwise] are sensitivity functions ie probability of testing positive as a function of time since exposure

# The next section of code defines functions that are used to:
# choose a set of values for one parameter (usually position), with spacing defined using an inverse cumulative normal distribution.
# define and generate individual curves - a sensitivity curve for each type of test, and a description of how to include the population variability to generate a set of curves
# Generate families of n curves for sensitivity   
# Generate families of n curves for likelihood of a certain test result. These functions take a 'test' object which specifies the parameter values
#   (including the set of values for the varying parameter(s) that represent the population-level variability) and the test result ('negative' or 'positive')
#   and a set of times. They return a matrix, each column of which contains the likelihood values for one of the `individual` curves; each curve specifies 
#   the likelihood of the test result given for each hypothetical date of first detectable infection.
# Note: generate_family functions don't return the range, granularity etc of thetime axis - this should be defined somewhere more central in the script.



generate_positions_for_individual_curves = function(n,scale,shape,mean_center_position,sd_size){
  shift_to_half_likelihood = scale*(-1*log(1/2))^(1/shape)
  myseq <- seq(1/(2*n),1-1/(2*n),1/n)
  positions <- qnorm(myseq,mean=mean_center_position-shift_to_half_likelihood,sd=sd_size)
  return(positions)
}

generate_positions_cumulative_normal = function(n,mean_center_position,sd_size){
  myseq <- seq(1/(2*n),1-1/(2*n),1/n)
  positions<-qnorm( myseq,mean=mean_center_position,sd=sd_size )
  return(positions)
}

#a sensitivity is a probability of correctly detecting an infection as a function of time after infection (or fddi doesn't matter here)
#a sensitivity is a probability of a positive result as a function of time since infection
#in our graphs (of likelihood functions) the time since infection is the difference between the time we observe and the test-time. This increases as we move left, which is 
# why we need to reverse the ``direction of time" when we convert from a sensitivity function to a likelihood. We should call the sensitivity function, reversed (comment this clearly so people aren't confused or angry), 
#the probability of testing negative is just 1 -probability of testing positive. no indeterminate results here
 



# Hello and Welcome

# These comments will guide you gently and clearly throught this code

# if you have any questions don't hesistate to email us at jeremyb@sun.ac.za

#questions I'm wondering about: legends instead of long y-axis labels?

# SECTION ONE: THE SENSITIVITY CURVES

# We begin by defining any and all sensitivity functions we will use. make sure to include an adjustable position parameter
# Each function you define here will have a function of its own in each of the following sections


shift_to_half_likelihood_weibul <- function(scale,shape){
  return(scale*(-1*log(1/2))^(1/shape))
}

sensitivity_weibul <- function(x,scale,shape,position){
  return(ifelse(x-position<0,0,1-exp(-((x-position)/scale)^shape))) #Note that the zero in the ifelse implies that pre-infection test results are never positive. 
  #adjust to incorporate imperfect specificity JEREMY CHECK THIS
}

#SECTION TWO: THE LIKELIHOOD CURVES

# we now write functions to represent each sensitivity function as a likelihood of testing positive/negative, given an infection/detectability time.

# the functional-form name at the end of each function name (eg "weibul") refers to the shape of the SENSITIVITY function for a particular test
# position is determined by the delay and the time of the test (0 for sensitivity) otherwise test_time

individual_sensitivity_weibul <- function(times,scale,shape,delay){
  return(sensitivity_weibul(x=times,scale=scale,shape=shape,position=delay-shift_to_half_likelihood_weibul(shape=shape,scale=scale)))
}

individual_negative_likelihood_weibul  <- function(times, scale, shape, delay, test_time){ #times is a vector of all the times we consider
  return(1-sensitivity_weibul(x=test_time-times,scale=scale,shape=shape,position=delay-shift_to_half_likelihood_weibul(scale=scale,shape=shape)))
}

individual_positive_likelihood_weibul <- function(times, scale, shape, delay, test_time){
  return (sensitivity_weibul(x=test_time-times,scale=scale,shape=shape,position=delay-shift_to_half_likelihood_weibul(scale=scale,shape=shape)))
}

# We now have code  generate the likelihood curves for our chosen tests

#SECTION THREE: THE FAMILIES

#note that the factor which varies within the family can be any of the parameters or even a combination of parameters
 # currently the family-generating functions have variability driven by one input

family_sensitivity_weibul <- function(times, scale, shape, mean_delay, sd_size, n){ #could also list all parameters (with default values) and use if else to select particular sensitivity shape
  list_of_positions <- generate_positions_cumulative_normal(n=n, mean_center_position=mean_delay, sd_size=sd_size)
  set_of_sensitivity_curves <- matrix(nrow=length(times),ncol=n)
  for(i in seq(1,n)){
    set_of_sensitivity_curves[,i] <- individual_sensitivity_weibul(times,scale,shape,list_of_positions[i])
  }
  return(set_of_sensitivity_curves)
}

family_negative_likelihood_weibul <- function(times, scale, shape, mean_delay, sd_size, n, test_time){ #could also list all parameters (with default values) and use if else to select particular sensitivity shape
  list_of_positions <- generate_positions_cumulative_normal(n=n, mean_center_position=mean_delay, sd_size=sd_size)
  set_of_negative_curves <- matrix(nrow=length(times),ncol=n)
  for(i in seq(1,n)){
    set_of_negative_curves[,i] <- individual_negative_likelihood_weibul(times=times,scale=scale,shape=shape,delay = list_of_positions[i],test_time=test_time)
  }
  return(set_of_negative_curves)
}

family_positive_likelihood_weibul <- function(times, scale, shape, mean_delay, sd_size, n, test_time){
  list_of_positions = generate_positions_cumulative_normal(n=n, mean_center_position=mean_delay, sd_size=sd_size)
  set_of_positive_curves <- matrix(nrow=length(times),ncol=n)
  for(i in seq(1,n)){
    set_of_positive_curves[,i] <- individual_positive_likelihood_weibul(times=times,scale=scale,shape=shape,delay = list_of_positions[i],test_time=test_time)
  }
  return(set_of_positive_curves)
}

#calculate the mean of a generic family of curves over a specified set of t-values
generate_mean_of_family = function(family_of_curves){ #input should be a matrix
  return(rowMeans(family_of_curves))
}

#calculate the product of two curves
generate_product_curve = function(curve1,curve2){ #this obviously doesn't need to be its own function I'm just renaming it 
  return(curve1*curve2)
}

#given a curve and find the likelihood for all times the combined test results.
likelihood_by_DDI = function(set_of_positive_curves,set_of_negative_curves,times){
  if(ncol(set_of_negative_curves) != ncol(set_of_positive_curves)) {stop ("Huh?? Why are there different numbers of curves?")}
  if(nrow(set_of_negative_curves) != nrow(set_of_positive_curves)) {stop ("Huh?? Why are there different numbers of time steps?")}
  likelihoods_per_time = rep(0,length(times))
  for (tpos in seq(1:length(times))){
    cumu_likely <- 0
    for (curvenumber in seq(1:ncol(set_of_negative_curves))){ #chronological order makes a trivial difference - there is 
                                                          #just a product per person
      likelihood_forward <- set_of_positive_curves[tpos,curvenumber]*set_of_negative_curves[tpos,curvenumber]
      likelihood_backward <- "The same thing unless I don't actually understand this task"
      cumu_likely <- cumu_likely + likelihood_forward
    }
    likelihoods_per_time[tpos] <- cumu_likely / ncol(set_of_negative_curves)
  }
  return(likelihoods_per_time)
}

#ALSO
#nice plotting function showing likelihood for an individual time point (including dashed lines for unlikely people)

# let's try the same functiont again but generating the curves from scratch each time, or at least input the delay and test_time - is this a good idea or should I just calculate which lines should be dotted based on the actual value (> or < 1/2 at considered time). using the actual value is MUCH less efficient...
# instead, I'll calculate a cutoff curve-number. Ie plot dotted from the cuttoff-th curve
# Okay, I think that may just make it moree difficult than it needs to be....

simple_plot_individual_time_likelihood <- function(n,times,set_of_positive_curves,set_of_negative_curves,set_of_positive_curves_background,set_of_negative_curves_background,time,test_of_interest,col_negative,col_positive,col_likelihood,lwd_ind,lwd_means,lwd_likelihood,curve_level_cutoff_probability){
  positive_mean_naive = rowMeans(set_of_positive_curves_background)
  negative_mean_naive = rowMeans(set_of_negative_curves_background)
  likelihood_naive <- negative_mean_naive*positive_mean_naive
  #position in timeaxis
  time_position <- which(times==time)
  #calculate_likelihood
  cumu_likely=0
  for (person in seq(1:ncol(set_of_negative_curves_background))){ #chronological order makes a trivial difference - there is 
    #just a product per person
    likelihood_forward = set_of_positive_curves_background[time_position,person]*set_of_negative_curves_background[time_position,person]
    likelihood_backward = "The same thing unless I don't actually understand this task"
    cumu_likely <- cumu_likely + likelihood_forward
  }
  likelihood_DDI_at_time_given_both_test_results = 1/ncol(set_of_negative_curves_background) *cumu_likely
  #plot the curves
  plot(times,plotdata_negative[,1],type='c',xlim=c(times[1],times[length(times)]),ylim=c(0,1),xlab='',ylab="",col='green',xaxt='n',yaxt='n',xaxs='i',yaxs='i',bty='l')
 
  # Time of Hypothetical DDI
  # Likelihood of observed test results
  #points(plotdata[,1],plotdata[,3])
  
  # normalising factor
  normalise_negative_test <- 0
  normalise_positive_test <- 0
  for (curve_number in seq(1:ncol(set_of_negative_curves))){
    normalise_negative_test <- normalise_negative_test + set_of_negative_curves[time_position,curve_number]
    normalise_positive_test <- normalise_positive_test + set_of_positive_curves[time_position,curve_number]
  }
  # normalise_negative_test <- normalise_negative_test/n
  # normalise_positive_test <- normalise_positive_test/n
  # print(normalise_negative_test)
  # print(normalise_positive_test)
  
  if(test_of_interest=="negative"){
    for (curve in seq(1:ncol(set_of_negative_curves))){
      if(!(set_of_negative_curves[time_position,curve]==0)&&!(set_of_positive_curves[time_position,curve]==0)&&(is.nan(set_of_negative_curves[time_position,curve]/normalise_negative_test) | is.nan(set_of_positive_curves[time_position,curve]/normalise_positive_test))){print("NaN Error! at",time,curve)}
      # print(set_of_negative_curves[time_position,curve]/normalise_negative_test)
      if (!(set_of_negative_curves[time_position,curve]==0) && set_of_negative_curves[time_position,curve]/normalise_negative_test>curve_level_cutoff_probability){
        lines(times,set_of_positive_curves[,curve],col=col_positive, lwd=lwd_ind) #what color should the positive curves be 
        lines(times,set_of_negative_curves[,curve],col=col_negative, lwd=lwd_ind) 
      }else{
        lines(times,set_of_positive_curves[,curve],col=col_positive,lty=2,lwd=lwd_ind) #what color should the positive curves be 
        lines(times,set_of_negative_curves[,curve],col=col_negative,lty=2,lwd=lwd_ind)
      }
    }}
  else if(test_of_interest=="positive"){
    for (curve in seq(1:ncol(set_of_negative_curves))){
      if (!(set_of_positive_curves[time_position,curve]==0) &&set_of_positive_curves[time_position,curve]/normalise_positive_test>curve_level_cutoff_probability){
        lines(times,set_of_positive_curves[,curve],col=col_positive,lwd=lwd_ind) #what color should the positive curves be 
        lines(times,set_of_negative_curves[,curve],col=col_negative,lwd=lwd_ind) 
      }else{
        lines(times,set_of_positive_curves[,curve],col=col_positive,lty=2,lwd=lwd_ind) #what color should the positive curves be 
        lines(times,set_of_negative_curves[,curve],col=col_negative,lty=2,lwd=lwd_ind)
      }
    }
  }
  lines(timeaxis,positive_mean_naive,col=col_positive,lwd=lwd_means)
  lines(timeaxis,negative_mean_naive,col=col_negative,lwd=lwd_means)
  points(pch=19,times[time_position],likelihood_by_DDI(set_of_positive_curves = set_of_positive_curves_background ,set_of_negative_curves = set_of_negative_curves_background,times=times)[time_position])#,lwd=lwd_likelihood,col=col_likelihood)

  
  
  # prettify_plot this is messy I know. it makes the gif-generation a bit easier
  
  lwd_means <- 4
  lwd_ind <- 1.37
  lwd_likelihood <- lwd_means - 3
  
  col_negative <- rgb(27/255,158/255,119/255)
  col_positive <- rgb(217/255,95/255,2/255)
  col_mean <- rgb(231/255,41/255,138/255)
  col_likelihood <- rgb(117/255,112/255,179/255)
  col_dotted <- rgb(3/7,3/7,3/7) #color for dotted lines
  
  # col_negative <- 'green'
  # col_positive <- 'red'
  # col_likelihood <- 'purple'
  
  #goto_do
  ## frame the dottedness as posteriors
  ## OR frame is as a direct probability statment
  
  scale_t1 = 5    #High scale causes slower swap
  shape_t1 = 5    #high shape causes quicker and steeper swap
  
  mean_delay_t1 = 12
  sd_size_t1 = 3
  #   Time of negative test (relative to arbitrary t=0)
  
  test_time_1 = 28
  
  ##                      TEST 2 (positive)
  
  scale_t2 = scale_t1
  shape_t2 = shape_t1
  
  mean_delay_t2 = mean_delay_t1
  sd_size_t2 = sd_size_t1
  
  #   Time of positive test
  test_time_2 = timeaxis[length(timeaxis)]-10
  
  
  ## Generate the individual likelihood curves for the first (negative) and second (positive) test
  #Test 1
  plotdata_negative = family_negative_likelihood_weibul(n=n, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
  #for generating mean curve
  plotdata_negative_background <- family_negative_likelihood_weibul(n=n+50, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
  #Test 2
  plotdata_positive = family_positive_likelihood_weibul(n=n, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)
  #for generating mean curve
  plotdata_positive_background <- family_positive_likelihood_weibul(n=n+50, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)
  
  
  
  
  title(xlab="Time", line=1.5, cex.lab=1.2)
  title(ylab=expression('Probability of test result'), line=2, cex.lab=1.05)
  
  
  yaxis_pos <- c(0,0.5,1)
  yaxis_names <- c('0',"0.5",'1')
  
  xaxis_pos <- c(focus_2b,test_time_1,test_time_2)
  xaxis_names <- c(expression('t'['i']),expression('t'['1']),expression('t'['2']))
  
  zero_pos <- c(0)
  zero_name <- c(expression('0'['']))
  
  axis(side=2, at=yaxis_pos, labels= yaxis_names,tck=-0.037, padj=.17)
  axis(side=1, at=xaxis_pos, labels= xaxis_names,padj=-.35,hadj=-.037)
  # axis(side=1, at=zero_pos, labels=zero_name,padj=-0.45,hadj=0.37)
  
  
  #positive_mean_background <- rowMeans(plotdata_positive_background)
  #negative_mean_background <- rowMeans(plotdata_negative_background)
  
  #lines(timeaxis,negative_mean_background, lwd=lwd_means, col=col_negative)      ##taking these out cause I included them in the "simple plot" function
  #lines(timeaxis,positive_mean_background, lwd=lwd_means, col=col_positive)
  segments(x0=test_time_1,y0=0,x1=test_time_1,y1=1,lty=4)
  segments(x0=test_time_2,y0=0,x1=test_time_2,y1=1,lty=4)
  
  segments(x0=focus_2b, y0=0, x1=focus_2b,y1=1,lty=3,col=col_dotted) 
  
  }


plot_individual_time_likelihood = function(n,times,set_of_positive_curves,set_of_negative_curves,time, test_of_interest){ #times is all times, ie timeaxis, time is particular time of interest
  #calculate means
  positive_mean_naive = rowMeans(set_of_positive_curves)
  negative_mean_naive = rowMeans(set_of_negative_curves)
  likelihood_naive <- negative_mean_naive*positive_mean_naive
  #position in timeaxis
  time_position <- which(times==time)
  #calculate_likelihood
  cumu_likely=0
  for (person in seq(1:ncol(set_of_negative_curves))){ #chronological order makes a trivial difference - there is 
    #just a product per person
    likelihood_forward = set_of_positive_curves[time_position,person]*set_of_negative_curves[time_position,person]
    likelihood_backward = "The same thing unless I don't actually understand this task"
    cumu_likely <- cumu_likely + likelihood_forward
  }
  likelihood_DDI_at_time_given_both_test_results = 1/ncol(set_of_negative_curves) *cumu_likely
  #plot the curves
  plot(times,plotdata_negative[,1],type='c',xlim=c(times[1],times[length(times)]),ylim=c(0,1),xlab="Hypothetical DDI (days)",ylab="Likelihood of observed test results",col='green')
  #points(plotdata[,1],plotdata[,3])
  if(test_of_interest=="negative"){
  for (curve in seq(1:ncol(set_of_negative_curves))){
    if (!(set_of_negative_curves[time_position,curve]==0) && set_of_negative_curves[time_position,curve]>0.5){
      lines(times,set_of_positive_curves[,curve],col='red', lwd=1.2) #what color should the positive curves be 
      lines(times,set_of_negative_curves[,curve],col='green', lwd=1.2) 
    }else{
      lines(times,set_of_positive_curves[,curve],col='red',lty=2,lwd=1.2) #what color should the positive curves be 
      lines(times,set_of_negative_curves[,curve],col='green',lty=2,lwd=1.2)
    }
  }}
  else if(test_of_interest=="positive"){
    for (curve in seq(1:ncol(set_of_negative_curves))){
      if (!(set_of_negative_curves[time_position,curve]==0) && set_of_positive_curves[time_position,curve]>0.5){
        lines(times,set_of_positive_curves[,curve],col='red',lwd=1.2) #what color should the positive curves be 
        lines(times,set_of_negative_curves[,curve],col='green',lwd=1.2) 
      }else{
        lines(times,set_of_positive_curves[,curve],col='red',lty=2,lwd=1.2) #what color should the positive curves be 
        lines(times,set_of_negative_curves[,curve],col='green',lty=2,lwd=1.2)
      }
    }
  }
  
  lines(times,positive_mean_naive,lwd=2,col='red')
  lines(times,negative_mean_naive,lwd=2,col='green')
  lines(times,likelihood_naive, lwd=4,col='grey') ### todo: transparency? or thin/thick lines? some way to clarify
  points(time,likelihood_DDI_at_time_given_both_test_results)
}



#
# 
# calculate_cuttoff_from_negative_curves <- function(time,timeaxis,set_of_negative_curves){
#  # given a hypothetical DDI returns the index of the first curve in the set  
#   # for which the likelihood of a negative test is smaller than 1/2
#    step <- which.min(abs(timeaxis-time))
#   nearest_curve <- which.min(abs(set_of_negative_curves[step,]-0.5))
#   if(set_of_negative_curves[step,nearest_curve]<0.5){
#     return(nearest_curve+1)}
#   else{return (nearest_curve)
#   }
# } 

# gotoscript

###     Some notes on parameters

#Scale defines interval from the last time where sample almost definitely tests negative to the first time when sample almost definitely tests positive testing positive. 
#Shape #defines the shape of the sensitivity curve as it increases from around 0 to around 1. Also affects the amount of time this takes, though not as much as scale.


##                    SCRIPT


n=3

mean_delay_positive_test=25
mean_delay_positive_test=15
sd_size_positive = 5
sd_size_negative = sd_size_positive
detail = 10
timeaxis = seq(0,100,1/detail)

scale = 5
shape = 5

illustration_timestep_size = 5
illustration_timestart = 30
illustration_number_timesteps = 10

#  Figure 1
################
# : produce a family of sensitivity curves and their average
#goto_1


n=7

# test_details
mean_delay_t1=25
mean_delay_t2=35       #we have a second test listed so that we can easily swap between them when generating the sensitivity curves

sd_size_t1 = 5
sd_size_t2 = sd_size_t1
detail = 10 # 1/Step size
timeaxis = seq(0,100,1/detail)

scale_t1= 5
shape_t1 = 5


#visuals
col_negative <- rgb(27/255,158/255,119/255)
col_positive <- rgb(217/255,95/255,2/255)
col_mean <- rgb(231/255,41/255,138/255)
col_truth <- rgb(117/255,112/255,179/255)


sensitivity_family_1 <-  family_sensitivity_weibul(n=n, scale=scale,shape=shape,mean_delay = mean_delay_t1 , sd_size=sd_size_t1,times=timeaxis)
sensitivity_family_background <- family_sensitivity_weibul(n=n+150,scale=scale_t1,shape=shape_t1,mean_delay=mean_delay_t1,sd_size=sd_size_t1,times=timeaxis)


sensitivity_average <- generate_mean_of_family(sensitivity_family_background) 

plot(timeaxis,sensitivity_family_1[,1],type='l',xaxt='n',xaxs='i',yaxs='i',xlim=c(mean_delay_t1-4*sd_size_t1,mean_delay_t1+shift_to_half_likelihood_weibul(shape=shape_t1,scale=scale_t1)+2*sd_size_t1),ylim=c(-.001,1),xlab="",ylab="",col='green',yaxt='n',bty='L')
# todo:   title
        # label sizes
        # colors
        # line widths
        # scale

title(xlab="Time since infection", line=1.5, cex.lab=1.2)
title(ylab=expression('Probability of positive test result'), line=1.7, cex.lab=1.05)

## goto_fix
# axis ticks, remove box, bring lower axis up to zero or thereabout
yaxis_pos <- c(0,.5,1)
yaxis_names <- c('0','0.5','1')


zero_pos <- c(0)
zero_name <- c(expression('0'['']))

axis(side=2, at=yaxis_pos, labels= yaxis_names,tck=-0.037, padj=.237)
#axis(side=1, at=xaxis_pos, labels= xaxis_names,padj=-.35,hadj=-.137)
axis(side=1, at=zero_pos, labels=zero_name,padj=-0.45,hadj=0.37)




for (i in seq(1:n)){
  lines(timeaxis,sensitivity_family_1[,i],col=col_negative,lwd=1.5)
}
lines(timeaxis,sensitivity_average,col=col_truth,lwd=2.5)


#######

# Figure 2: Likelihood of observed discordant test results, t1 negative t2 positive - different times
#goto_2a

n=10
detail=10
timeaxis=seq(0,70,1/detail)

#                       TEST 1 (negative)

#     Describe individual (person) test sensitivity form with population mean-delay and standard deviation of delay
      # delay is the variable we distribute across the population - it could in principle be anything else of course
#so each individual has the same SHAPE of sensitivity, but different delays

## Visuals

lwd_means <- 2.8
lwd_ind <- 1.95
col_negative <- 'green'
col_positive <- 'red'


scale_t1 = 5    #High scale causes slower swap
shape_t1 = 5    #high shape causes quicker and steeper swap

mean_delay_t1 = 12
sd_size_t1 = 3
#   Time of negative test (relative to arbitrary t=0)

test_time_1 = 28

##                      TEST 2 (positive)

scale_t2 = scale_t1
shape_t2 = shape_t1

mean_delay_t2 = mean_delay_t1
sd_size_t2 = sd_size_t1

#   Time of positive test
test_time_2 = timeaxis[length(timeaxis)]-10


## Generate the individual likelihood curves for the first (negative) and second (positive) test
#Test 1
plotdata_negative = family_negative_likelihood_weibul(n=n, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#for generating mean curve
plotdata_negative_background <- family_negative_likelihood_weibul(n=n+50, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#Test 2
plotdata_positive = family_positive_likelihood_weibul(n=n, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)
#for generating mean curve
plotdata_positive_background <- family_positive_likelihood_weibul(n=n+50, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)


##        COMMUNICATE

plot(timeaxis,plotdata_negative[,1],type='l',xlim=c(timeaxis[1],timeaxis[length(timeaxis)]),ylim=c(-.001,1),xaxt='n',yaxt='n',xaxs='i',yaxs='i',bty='l',xlab='',ylab='',col='green') #clarify label in comment
title(xlab="Time", line=1.5, cex.lab=1.2)
title(ylab=expression('Likelihood'), line=1.4, cex.lab=1.05)


yaxis_pos <- c(0,0.5,1)
yaxis_names <- c('0',"0.5",'1')

xaxis_pos <- c(test_time_1,test_time_2)
xaxis_names <- c(expression('t'['1']),expression('t'['2']))

zero_pos <- c(0)
zero_name <- c(expression('0'['']))
 #shift axes
axis(side=2, at=yaxis_pos, labels= yaxis_names,tck=-0.037, padj=.437)
axis(side=1, at=xaxis_pos, labels= xaxis_names,padj=-.35,hadj=-.137)
#axis(side=1, at=zero_pos, labels=zero_name,padj=-0.45,hadj=0.37)

# goto_do

#points(plotdata[,1],plotdata[,3])
for (i in seq(1:n)){
  lines(timeaxis,plotdata_negative[,i],col=col_negative,lwd=lwd_ind)
}
#points(plotdata[,1],plotdata[,3])
for (i in seq(1:n)){
  lines(timeaxis,plotdata_positive[,i],col=col_positive,lwd=lwd_ind)
}

positive_mean_background <- rowMeans(plotdata_positive_background)
negative_mean_background <- rowMeans(plotdata_negative_background)

lines(timeaxis,negative_mean_background, lwd=lwd_means, col=col_negative)
lines(timeaxis,positive_mean_background, lwd=lwd_means, col=col_positive)
segments(x0=test_time_1,y0=0,x1=test_time_1,y1=1,lty=4)
segments(x0=test_time_2,y0=0,x1=test_time_2,y1=1,lty=4)

# segments(x0=0,y0=1.0004,x1=timeaxis[length(timeaxis)],y1=1.0004,lty=8,lwd=1.2)

#arrows(x0=test_time_1-mean_delay_t1,y0=0.5,x1=test_time_1,y1=0.5,lty=1,code=3,length=.1,angle=10)

#TO DO: REMOVE AXIS LABELS FOR x-axis && give title && write comment
    ### IDEA: I could calculate the mean using a large number of individual curves, but plot just a few of the individual curves. I did choose to do this to ensure the mean curve looks 
      ## Question: Why and precicely how is it valid to use the cumulative normal distribution to approximate the population-level distribution of delays? (even if the population-level delays are normally distributed, which I think we just thumbsuck like a linear fit. Initially I thought the normal distribution was natural since the disease progression is random on each day and for a particular test the total delay is a sum of the daily (or whichver discrete timestep) delays. However this means an individual's actual delay is drawn from a normal distribution, but we only ever see one data point from that exact distribution. Different population members may have delays drawn from different normal distributions - there's no particular reason to believe that the means (nevermind the standard deviations) of individual normal distributions will be normally distributed across the population. There could for example be a particular genetic marker which just protects 20% of people really well, leading to a two-spike distribution of means for the individual normal distributions, and a two-peak less-spiked distribution of realised delays.)
      ## another IDEA: make the mean lines slightly transparent - needs rgb color specification: good excuse to choose better colors
      ## another question: axes need labels?
        ##another QUESTION: in figure 3a (more/less sensitive tests on same day w/ discordant results)
      ## Figure 3b ?
## remove frames


#########

# Figure 2b
# goto_do gif this don't we cant to gif 2c rather?
# We now illuminate the conditional probabilities by portraying the "less-likely individuals [section of the population]" using
# individual dashed instead of solid lines
# We copy the same situation and use the code from the individual_time_likelihood function to get dotted lines
#   goto_2b

n<-10

detail<-10
timeaxis<-seq(0,70,1/detail)

focus_2b <- 20  #the focal hypothetical 'DDI' for this figure

#                       TEST 1 (negative)

#     Describe individual (person) test sensitivity form with population mean-delay and standard deviation of delay
# delay is the variable we distribute across the population - it could in principle be anything else of course
#so each individual has the same SHAPE of sensitivity, but different delays
 

# goto_do spell our correlation
# we are completely ignorant of which curve 'you' are on -> Prior
# The hypothetical assumption that tDDI is the tDDI

# q1 hypothetical DDI, probablity of test result (A: mean curve)
# q2 given ddi and test(-), what is the probability attached to each individual likelihood curve. i.e.
# what is the probability that a subject is on a particular curve?
# to get this, we should probably
# Well a particular curve represents the probability that a particular subject will test positive => P(test result | subject)
# we want P(subject|test result) for the same set of DDI's. of course the Sum_{subjects} P(subject|test result) = 1, so we can
# just normalise according to the cutoff

## Visuals

lwd_means <- 4
lwd_ind <- 1.37
lwd_likelihood <- lwd_means - 3

col_negative <- rgb(27/255,158/255,119/255)
col_positive <- rgb(217/255,95/255,2/255)
col_mean <- rgb(231/255,41/255,138/255)
col_likelihood <- rgb(117/255,112/255,179/255)
col_dotted <- rgb(3/7,3/7,3/7) #color for dotted lines

# col_negative <- 'green'
# col_positive <- 'red'
# col_likelihood <- 'purple'

#goto_do
## frame the dottedness as posteriors
## OR frame is as a direct probability statment

scale_t1 = 5    #High scale causes slower swap
shape_t1 = 5    #high shape causes quicker and steeper swap

mean_delay_t1 = 12
sd_size_t1 = 3
#   Time of negative test (relative to arbitrary t=0)

test_time_1 = 28

##                      TEST 2 (positive)

scale_t2 = scale_t1
shape_t2 = shape_t1

mean_delay_t2 = mean_delay_t1
sd_size_t2 = sd_size_t1

#   Time of positive test
test_time_2 = timeaxis[length(timeaxis)]-10


## Generate the individual likelihood curves for the first (negative) and second (positive) test
#Test 1
plotdata_negative = family_negative_likelihood_weibul(n=n, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#for generating mean curve
plotdata_negative_background <- family_negative_likelihood_weibul(n=n+50, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#Test 2
plotdata_positive = family_positive_likelihood_weibul(n=n, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)
#for generating mean curve
plotdata_positive_background <- family_positive_likelihood_weibul(n=n+50, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)


##        COMMUNICATE
for (infection_time in seq(1:timeaxis[length(timeaxis)])){
  simple_plot_individual_time_likelihood(n=n, times=timeaxis, test_of_interest = 'negative',set_of_positive_curves_background = plotdata_positive_background,set_of_negative_curves_background = plotdata_negative_background, set_of_positive_curves = plotdata_positive,set_of_negative_curves = plotdata_negative,time = infection_time, col_negative=col_negative ,col_positive=col_positive, col_likelihood = col_likelihood, lwd_means=lwd_means,lwd_likelihood = lwd_likelihood, lwd_ind = lwd_ind,curve_level_cutoff_probability = .05)
}
focus_2b <-15
simple_plot_individual_time_likelihood(n=n, times=timeaxis, test_of_interest = 'negative',set_of_positive_curves_background = plotdata_positive_background,set_of_negative_curves_background = plotdata_negative_background, set_of_positive_curves = plotdata_positive,set_of_negative_curves = plotdata_negative,time = focus_2b, col_negative=col_negative ,col_positive=col_positive, col_likelihood = col_likelihood, lwd_means=lwd_means,lwd_likelihood = lwd_likelihood, lwd_ind = lwd_ind,curve_level_cutoff_probability = .05)

for(infection_time in seq(to=timeaxis[length(timeaxis)],from=1)){
  simple_plot_individual_time_likelihood(n=n, times=timeaxis, test_of_interest = 'positive',set_of_positive_curves_background = plotdata_positive_background,set_of_negative_curves_background = plotdata_negative_background, set_of_positive_curves = plotdata_positive,set_of_negative_curves = plotdata_negative,time = infection_time, col_negative=col_negative ,col_positive=col_positive, col_likelihood = col_likelihood, lwd_means=lwd_means,lwd_likelihood = lwd_likelihood, lwd_ind = lwd_ind,curve_level_cutoff_probability = .05)
}


#GIF_IT

setwd( "H:\\infection-dating-tool\\manuscripts\\figures\\")

for(infection_time in seq(to=timeaxis[length(timeaxis)],from=1)){
  
  pdf(file=paste0("gif_",infection_time,".pdf"))
  
  par(mfrow=c(1,2))
  
  simple_plot_individual_time_likelihood(n=n, times=timeaxis, test_of_interest = 'negative',set_of_positive_curves_background = plotdata_positive_background,set_of_negative_curves_background = plotdata_negative_background, set_of_positive_curves = plotdata_positive,set_of_negative_curves = plotdata_negative,time = infection_time, col_negative=col_negative ,col_positive=col_positive, col_likelihood = col_likelihood, lwd_means=lwd_means,lwd_likelihood = lwd_likelihood, lwd_ind = lwd_ind,curve_level_cutoff_probability = .05)
  simple_plot_individual_time_likelihood(n=n, times=timeaxis, test_of_interest = 'positive',set_of_positive_curves_background = plotdata_positive_background,set_of_negative_curves_background = plotdata_negative_background, set_of_positive_curves = plotdata_positive,set_of_negative_curves = plotdata_negative,time = infection_time, col_negative=col_negative ,col_positive=col_positive, col_likelihood = col_likelihood, lwd_means=lwd_means,lwd_likelihood = lwd_likelihood, lwd_ind = lwd_ind,curve_level_cutoff_probability = .05)
  
  dev.off()
}
# dev.off()

# # supposed example (not really working though)
# dir.create("examples")
# setwd("examples")
# 
# # example 1: simple animated countdown from 10 to "GO!".
# png(file="example%02d.png", width=200, height=200)
# for (i in c(10:1, "G0!")){
#   plot.new()
#   text(.5, .5, i, cex = 6)
# }
# dev.off()
# 
# # convert the .png files to one .gif file using ImageMagick.
# # The system() function executes the command as if it was done
# # in the terminal. the -delay flag sets the time between showing
# # the frames, i.e. the speed of the animation.
# system("convert -delay 80 *.png example_1.gif")
# 
# # to not leave the directory with the single jpeg files
# # I remove them.
# file.remove(list.files(pattern=".png"))

##how to use imagemagick for gifs
# https://cran.r-project.org/web/packages/animation/animation.pdf

# now put all the graphical niceties into the main function.
# then finish it off 

# question: once we normalise the likelihoods into "probabilities that a randomly selected population member is on this curve given the results"
# .. in the limiting case of n identical curves we never have this probability be larger than 1/n. so it's not exactly clear 
# how we should present this... I guess it doesn't matter but people might wonder why we choose a particular value. ?? 
# we could fail to specify the value /// mention that it doesn't matter > I'd stick with the first ("Solid lines indicate the more likely {footnote with precise statement} sensitivity profiles.)

# ref
# somePDFPath = "C:\\temp\\some.pdf"
# pdf(file=somePDFPath)  
# 
# for (i in seq(5,10))   
# {   
#   par(mfrow = c(2,1))
#   VAR1=rnorm(i)  
#   VAR2=rnorm(i)  
#   plot(VAR1,VAR2)   
# } 
# dev.off() 
# more ref

#goto_do dot at real likelihood I think this is more appropriate for the next figure (figure 2c)

# plot(timeaxis,plotdata_negative[,1],type='l',xlim=c(timeaxis[1],timeaxis[length(timeaxis)]),ylim=c(0,1),xaxt='n',yaxt='n',xlab='',ylab='',col='green') #clarify label in comment
title(xlab="Time", line=1.5, cex.lab=1.2)
title(ylab=expression('Probability of test result'), line=2, cex.lab=1.05)


yaxis_pos <- c(0,0.5,1)
yaxis_names <- c('0',"0.5",'1')

xaxis_pos <- c(focus_2b,test_time_1,test_time_2)
xaxis_names <- c(expression('t'['i']),expression('t'['1']),expression('t'['2']))

zero_pos <- c(0)
zero_name <- c(expression('0'['']))

axis(side=2, at=yaxis_pos, labels= yaxis_names,tck=-0.037, padj=.17)
axis(side=1, at=xaxis_pos, labels= xaxis_names,padj=-.35,hadj=-.037)
# axis(side=1, at=zero_pos, labels=zero_name,padj=-0.45,hadj=0.37)


#positive_mean_background <- rowMeans(plotdata_positive_background)
#negative_mean_background <- rowMeans(plotdata_negative_background)

#lines(timeaxis,negative_mean_background, lwd=lwd_means, col=col_negative)      ##taking these out cause I included them in the "simple plot" function
#lines(timeaxis,positive_mean_background, lwd=lwd_means, col=col_positive)
segments(x0=test_time_1,y0=0,x1=test_time_1,y1=1,lty=4)
segments(x0=test_time_2,y0=0,x1=test_time_2,y1=1,lty=4)

segments(x0=focus_2b, y0=0, x1=focus_2b,y1=1,lty=3,col=col_dotted)

# segments(x0=0,y0=1.004,x1=timeaxis[length(timeaxis)],y1=1.004,lty=8,lwd=1.2)

# Arrows(x0=focus_2b+.25,y0=0.5,x1=test_time_1-.3,y1=0.5,code=3,arr.length=.2, arr.width = .1,arr.adj=0.5,arr.type='triangle',segment=TRUE,col=1,lty=2,lwd=1.1,arr.lwd=1.1)


#####


###          Figure 2c
# Let's see what the more-careful likelihood function looks like. Let's illustrate how we could define a cuttoff window for quite "sure the infection happened hereabouts"

#   goto_2c
# goto_do dot at real likelihood

n<-10

detail<-10
timeaxis<-seq(0,70,1/detail)

cutoff_likelihood <- 0.2

#                       TEST 1 (negative)

#     Describe individual (person) test sensitivity form with population mean-delay and standard deviation of delay
# delay is the variable we distribute across the population - it could in principle be anything else of course
#so each individual has the same SHAPE of sensitivity, but different delays

## Visuals

lwd_means <- 2
lwd_ind <- 1.37
col_negative <- 'green'
col_positive <- 'red'


scale_t1 = 5    #High scale causes slower swap
shape_t1 = 5    #high shape causes quicker and steeper swap

mean_delay_t1 = 12
sd_size_t1 = 3
#   Time of negative test (relative to arbitrary t=0)

test_time_1 = 28

##                      TEST 2 (positive)

scale_t2 = scale_t1
shape_t2 = shape_t1

mean_delay_t2 = mean_delay_t1
sd_size_t2 = sd_size_t1

#   Time of positive test
test_time_2 = timeaxis[length(timeaxis)]-10


## Generate the individual likelihood curves for the first (negative) and second (positive) test
#Test 1
plotdata_negative = family_negative_likelihood_weibul(n=n, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#for generating mean curve
plotdata_negative_background <- family_negative_likelihood_weibul(n=n+50, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#Test 2
plotdata_positive = family_positive_likelihood_weibul(n=n, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)
#for generating mean curve
plotdata_positive_background <- family_positive_likelihood_weibul(n=n+50, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)

##

find_L_or_E_PDDI <- function(likelihood,times,cutoff){ 
  # get true cutoff not naive threshold. normalise this joint curve (integrate or can I just divide somehow?)
  # 'cutoff' probablity doesn't belong on the y-axis (not based on height based on area under normalised-likelihood pdf)
  total_area <- AUC(times,likelihood,method="spline")
  likelihood_as_probability <- likelihood / total_area
  print(AUC(times,likelihood_as_probability,method="spline"))
  #returns the indices of the EPToi and LPToi
  infection_window <- c(0,times[length(times)])
  found<-0
  for (time in  seq(1,length(times))){
    if(AUC(times[1:time],likelihood_as_probability[1:time],method="spline")>cutoff && found==0){
      infection_window[1] <- time #need to avoid this check once it's been found
      found <- 1
    }
    else if(AUC(times[1:time],likelihood_as_probability[1:time],method="spline")>1-cutoff && found==1){
      infection_window[2] <- time
      found <- 2
    }
  }
  return(infection_window)
}


likelihood_discordant_results_2c <- likelihood_by_DDI(plotdata_negative,plotdata_positive,timeaxis)
window_infection_time <- find_L_or_E_PDDI(likelihood=likelihood_discordant_results_2c, times=timeaxis, cutoff = cutoff_likelihood)
EPToi <- timeaxis[window_infection_time[1]]
LPToi <- timeaxis[window_infection_time[2]]


plot(timeaxis,likelihood_by_DDI(plotdata_negative,plotdata_positive,timeaxis),type='l',lwd='3.7',xlim=c(timeaxis[1],timeaxis[length(timeaxis)]),ylim=c(0,1),xaxs='i',yaxs='i',xaxt='n',yaxt='n',xlab='',ylab='',col='green',bty="L") #clarify label in comment

title(xlab="Time", line=2, cex.lab=1.2)
title(ylab=expression('Likelihood'), line=2, cex.lab=1.05)



yaxis_pos <- c(0,0.5,1)
yaxis_names <- c('0','0.5','1')

polygon(c(timeaxis[timeaxis<=EPToi],EPToi), c(likelihood_discordant_results_2c[timeaxis<=EPToi],0), col=rgb(.2,.2,.2,1/4),border=NA)
polygon(c(timeaxis[timeaxis>=LPToi],LPToi), c(likelihood_discordant_results_2c[timeaxis>=LPToi],0), col=rgb(.2,.2,.2,1/4),border=NA)

xaxis_pos <- c(test_time_1,test_time_2)
xaxis_names <- c(expression('Test'['1(-)']),expression('Test'['2(+)']))

p_pos <- c(EPToi,LPToi)
p_labels <- c(expression('EPt'[" i"]),expression('LPt'[" i"]))

zero_pos <- c(0)
zero_name <- c(expression('0'['']))

axis(side=2, at=yaxis_pos, labels= yaxis_names,tck=-0.0237, padj=-.017)
axis(side=1, at=xaxis_pos, labels= xaxis_names,padj=-.037,hadj=0)
axis(side=1, at=p_pos, labels = p_labels, padj = -.35, hadj=.37)
# axis(side=1, at=zero_pos, labels=zero_name,padj=-0.45,hadj=0.37)

segments(x0=test_time_1,y0=0,x1=test_time_1,y1=1,lty=4)
segments(x0=test_time_2,y0=0,x1=test_time_2,y1=1,lty=4)

segments(x0=EPToi, y0=0, x1=EPToi,y1=1,lty=3,col=4)
segments(x0=LPToi, y0=0, x1=LPToi,y1=1,lty=3,col=4)

segments(x0=0,y0=1.004,x1=timeaxis[length(timeaxis)],y1=1.004,lty=8,lwd=1.2)

####

# Figure 3a

# goto_3a
# Here we have two tests, on the same day, where the less sensitive test yields a negative result while the more sensitive test yields 
# a positive result.
n=10
detail=10
timeaxis=seq(0,70,1/detail)

#                       TEST 1 (negative)

#     Describe individual (person) test sensitivity form with population mean-delay and standard deviation of delay
# delay is the variable we distribute across the population - it could in principle be anything else of course
#so each individual has the same SHAPE of sensitivity, but different delays

## Visuals

lwd_means <- 4
lwd_likelihoods <- 2.7
lwd_ind <- 2
col_negative <- rgb(27/255,158/255,119/255)
col_positive <- rgb(217/255,95/255,2/255)
col_mean <- rgb(231/255,41/255,138/255)
col_truth <- rgb(117/255,112/255,179/255)


scale_t1 = 5    #High scale causes slower swap
shape_t1 = 5    #high shape causes quicker and steeper swap

mean_delay_t1 = 24
sd_size_t1 = 5
#   Time of negative test (relative to arbitrary t=0)

test_time_1 =45

##                      TEST 2 (positive)

scale_t2 = scale_t1
shape_t2 = shape_t1

mean_delay_t2 = mean_delay_t1/2
sd_size_t2 = sd_size_t1*.7

#   Time of positive test
test_time_2 = test_time_1


## Generate the individual likelihood curves for the first (negative) and second (positive) test
#Test 1
plotdata_negative = family_negative_likelihood_weibul(n=n, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#for generating mean curve
plotdata_negative_background <- family_negative_likelihood_weibul(n=n+50, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#Test 2
plotdata_positive = family_positive_likelihood_weibul(n=n, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)
#for generating mean curve
plotdata_positive_background <- family_positive_likelihood_weibul(n=n+50, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)

likelihood_discordant_3a <- likelihood_by_DDI(plotdata_negative,plotdata_positive,timeaxis)


plot(timeaxis,plotdata_negative[,1],type='l',xlim=c(timeaxis[1],timeaxis[length(timeaxis)]),ylim=c(-0.001,1),xaxt='n',yaxt='n',xlab='',ylab='',bty='l',yaxs='i',xaxs='i',col='green') #clarify label in comment
title(xlab="Time", line=1.5, cex.lab=1.2)
title(ylab=expression('Likelihood'), line=1.7, cex.lab=1.05)


yaxis_pos <- c(0,0.5,1)
yaxis_names <- c('0','0.5','1')

xaxis_pos <- c(test_time_1)
xaxis_names <- c(expression('t'['+/-']))


axis(side=2, at=yaxis_pos, labels= yaxis_names,tck=-0.027, padj=.437)
axis(side=1, at=xaxis_pos, labels= xaxis_names,padj=-.35,hadj=-.137)

#points(plotdata[,1],plotdata[,3])
for (i in seq(1:n)){
  lines(timeaxis,plotdata_negative[,i],col=col_negative,lwd=lwd_ind)
}
#points(plotdata[,1],plotdata[,3])
for (i in seq(1:n)){
  lines(timeaxis,plotdata_positive[,i],col=col_positive,lwd=lwd_ind)
}



positive_mean_naive <- rowMeans(plotdata_positive)                              #not _naive
negative_mean_naive <- rowMeans(plotdata_negative)
positive_mean_background <- rowMeans(plotdata_positive_background)
negative_mean_background <- rowMeans(plotdata_negative_background)
product_of_means_naive <- positive_mean_background*negative_mean_background # naive product of individual likelihoods


real_likelihood <- likelihood_by_DDI(times = timeaxis, set_of_positive_curves = plotdata_positive_background, set_of_negative_curves = plotdata_negative_background)
difference <- product_of_means_naive - real_likelihood


lines(timeaxis,negative_mean_background, lwd=lwd_means, col=col_negative)
lines(timeaxis,positive_mean_background, lwd=lwd_means, col=col_positive)
segments(x0=test_time_1,y0=0,x1=test_time_1,y1=1,lty=4)
segments(x0=test_time_2,y0=0,x1=test_time_2,y1=1,lty=4)

segments(x0=0,y0=1.004,x1=timeaxis[length(timeaxis)],y1=1.004,lty=8,lwd=1.2)


print("The maximum difference for this scenario between the true likelihood and the totally naive approximation is on the next line:")
print(max(difference))
#lines(timeaxis,difference,lwd=1,col="blue")
# lines(timeaxis,positive_mean_naive,lwd=2,col='red')
# lines(timeaxis,negative_mean_naive,lwd=2,col='green')
lines(timeaxis,product_of_means_naive,lwd=lwd_likelihoods,col="grey")
lines(timeaxis,real_likelihood,lwd=lwd_likelihoods,col=col_truth)


######


# Figure 3c
############


# goto_3c
# Here we have two tests, on the same day, where the less sensitive test yields a negative result while the more sensitive test yields 
# a positive result.
n=7
detail=10
timeaxis=seq(0,50,1/detail)

#                       TEST 1 (negative)

#     Describe individual (person) test sensitivity form with population mean-delay and standard deviation of delay
# delay is the variable we distribute across the population - it could in principle be anything else of course
#so each individual has the same SHAPE of sensitivity, but different delays

## Visuals

lwd_means <- 2
lwd_ind <- 1.7
col_negative <- rgb(102/255,194/255,165/255)
col_positive <- rgb(252/255,141/255,98/255)
col_mean <- rgb(141/255,160/255,203/255)
col_truth <- rgb(51/255,160/255,44/255)

scale_t1 = 5    #High scale causes slower swap
shape_t1 = 5    #high shape causes quicker and steeper swap

mean_delay_t1 = 24
sd_size_t1 = 5
#   Time of negative test (relative to arbitrary t=0)

test_time_1 =45

##                      TEST 2 (positive)

scale_t2 = scale_t1
shape_t2 = shape_t1

mean_delay_t2 = mean_delay_t1
sd_size_t2 = sd_size_t1

#   Time of positive test
test_time_2 = test_time_1


## Generate the individual likelihood curves for the first (negative) and second (positive) test
#Test 1
plotdata_negative = family_negative_likelihood_weibul(n=n, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#for generating mean curve
plotdata_negative_background <- family_negative_likelihood_weibul(n=n+50, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#Test 2
plotdata_positive = family_positive_likelihood_weibul(n=n, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)
#for generating mean curve
plotdata_positive_background <- family_positive_likelihood_weibul(n=n+50, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)

likelihood_discordant_3a <- likelihood_by_DDI(plotdata_negative,plotdata_positive,timeaxis)
pdf("figure_3c.pdf")

plot(timeaxis,plotdata_negative[,1],type='l',xlim=c(timeaxis[1],timeaxis[length(timeaxis)]),ylim=c(-0.001,1),xaxt='n',yaxt='n',xlab='',ylab='',bty='l',xaxs='i',yaxs='i',col=col_negative) #clarify label in comment
title(xlab="Time", line=1.5, cex.lab=1.2)
title(ylab=expression('Likelihood'), line=1.7, cex.lab=1.05)


yaxis_pos <- c(0,0.5,1)
yaxis_names <- c('0','0.5','1')

xaxis_pos <- c(test_time_1)
xaxis_names <- c(expression('t'['+/-']))


axis(side=2, at=yaxis_pos, labels= yaxis_names,tck=-0.023, padj=.437)
axis(side=1, at=xaxis_pos, labels= xaxis_names,padj=-.35,hadj=-.137)

#points(plotdata[,1],plotdata[,3])
for (i in seq(1:n)){
  lines(timeaxis,plotdata_negative[,i],col=col_negative,lwd=lwd_ind)
}
#points(plotdata[,1],plotdata[,3])
for (i in seq(1:n)){
  lines(timeaxis,plotdata_positive[,i],col=col_positive,lwd=lwd_ind)
}



positive_mean_naive <- rowMeans(plotdata_positive)                              #not _naive
negative_mean_naive <- rowMeans(plotdata_negative)
positive_mean_background <- rowMeans(plotdata_positive_background)
negative_mean_background <- rowMeans(plotdata_negative_background)
product_of_means_naive <- positive_mean_background*negative_mean_background # naive product of individual likelihoods


real_likelihood <- likelihood_by_DDI(times = timeaxis, set_of_positive_curves = plotdata_positive_background, set_of_negative_curves = plotdata_negative_background)
difference <- product_of_means_naive - real_likelihood


lines(timeaxis,negative_mean_background, lwd=lwd_means, col=col_negative)
lines(timeaxis,positive_mean_background, lwd=lwd_means, col=col_positive)
segments(x0=test_time_1,y0=0,x1=test_time_1,y1=1,lty=4)
segments(x0=test_time_2,y0=0,x1=test_time_2,y1=1,lty=4,col=col_mean)

segments(x0=0,y0=1.004,x1=timeaxis[length(timeaxis)],y1=1.004,lty=8,lwd=1.2)


print("The maximum difference for this scenario between the true likelihood and the totally naive approximation is on the next line:")
print(max(difference))
#lines(timeaxis,difference,lwd=1,col="blue")
# lines(timeaxis,positive_mean_naive,lwd=2,col='red')
# lines(timeaxis,negative_mean_naive,lwd=2,col='green')
lines(timeaxis,product_of_means_naive,lwd=2,col='grey',lty=3)
lines(timeaxis,real_likelihood,lwd=4,col=col_mean)
dev.off()
legend()

######


# Figure 3d
############

# This figure shows the less-likely (same-day discordant) scenario of the more sensitive testing negative while the less sensitive testing positive

# goto_3c
# Here we have two tests, on the same day, where the less sensitive test yields a negative result while the more sensitive test yields 
# a positive result.
n=10
detail=10
timeaxis=seq(0,70,1/detail)

#                       TEST 1 (negative)

#     Describe individual (person) test sensitivity form with population mean-delay and standard deviation of delay
# delay is the variable we distribute across the population - it could in principle be anything else of course
#so each individual has the same SHAPE of sensitivity, but different delays

## Visuals

lwd_means <- 2
lwd_ind <- 1.37
col_negative <- 'green'
col_positive <- 'red'


scale_t1 = 5    #High scale causes slower swap
shape_t1 = 5    #high shape causes quicker and steeper swap

mean_delay_t1 = 24
sd_size_t1 = 5
#   Time of negative test (relative to arbitrary t=0)

test_time_1 =67

##                      TEST 2 (positive)

scale_t2 = scale_t1
shape_t2 = shape_t1

mean_delay_t2 = mean_delay_t1*1.2
sd_size_t2 = sd_size_t1*1.37

#   Time of positive test
test_time_2 = test_time_1


## Generate the individual likelihood curves for the first (negative) and second (positive) test
#Test 1
plotdata_negative = family_negative_likelihood_weibul(n=n, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#for generating mean curve
plotdata_negative_background <- family_negative_likelihood_weibul(n=n+500, scale=scale_t1, shape=shape_t1, mean_delay=mean_delay_t1, sd_size= sd_size_t1, times = timeaxis, test_time = test_time_1)
#Test 2
plotdata_positive = family_positive_likelihood_weibul(n=n, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)
#for generating mean curve
plotdata_positive_background <- family_positive_likelihood_weibul(n=n+500, scale=scale_t2, shape=shape_t2, mean_delay=mean_delay_t2, sd_size= sd_size_t2, times = timeaxis, test_time = test_time_2)

likelihood_discordant_3a <- likelihood_by_DDI(plotdata_negative,plotdata_positive,timeaxis)

pdf("figure_3d.pdf")

plot(timeaxis,plotdata_negative[,1],type='l',xlim=c(timeaxis[1],timeaxis[length(timeaxis)]),ylim=c(0,1),xaxt='n',yaxt='n',xlab='',ylab='',col='green') #clarify label in comment
title(xlab="t", line=1.5, cex.lab=1.2)
title(ylab=expression('P(-/+ at t'['1/2']*' | DDI=t)'), line=1.4, cex.lab=1.05)


yaxis_pos <- c(0,0.5,1)
yaxis_names <- c('0','0.5','1')

xaxis_pos <- c(test_time_1)
xaxis_names <- c(expression('t'['+/-']))

zero_pos <- c(0)
zero_name <- c(expression('0'['']))

axis(side=2, at=yaxis_pos, labels= yaxis_names,tck=-0.023, padj=.437)
axis(side=1, at=xaxis_pos, labels= xaxis_names,padj=-.35,hadj=-.137)
axis(side=1, at=zero_pos, labels=zero_name,padj=-0.45,hadj=0.37)

#points(plotdata[,1],plotdata[,3])
for (i in seq(1:n)){
  lines(timeaxis,plotdata_negative[,i],col=col_negative,lwd=lwd_ind)
}
#points(plotdata[,1],plotdata[,3])
for (i in seq(1:n)){
  lines(timeaxis,plotdata_positive[,i],col=col_positive,lwd=lwd_ind)
}



positive_mean_naive <- rowMeans(plotdata_positive)                              #not _naive
negative_mean_naive <- rowMeans(plotdata_negative)
positive_mean_background <- rowMeans(plotdata_positive_background)
negative_mean_background <- rowMeans(plotdata_negative_background)
product_of_means_naive <- positive_mean_background*negative_mean_background # naive product of individual likelihoods


real_likelihood <- likelihood_by_DDI(times = timeaxis, set_of_positive_curves = plotdata_positive_background, set_of_negative_curves = plotdata_negative_background)
difference <- product_of_means_naive - real_likelihood


lines(timeaxis,negative_mean_background, lwd=lwd_means, col='grey')
lines(timeaxis,positive_mean_background, lwd=lwd_means, col='grey')
segments(x0=test_time_1,y0=0,x1=test_time_1,y1=1,lty=4)
segments(x0=test_time_2,y0=0,x1=test_time_2,y1=1,lty=4)

segments(x0=0,y0=1.004,x1=timeaxis[length(timeaxis)],y1=1.004,lty=8,lwd=1.2)


print("The maximum difference for this scenario between the true likelihood and the totally naive approximation is on the next line:")
print(max(difference))
#lines(timeaxis,difference,lwd=1,col="blue")
# lines(timeaxis,positive_mean_naive,lwd=2,col='red')
# lines(timeaxis,negative_mean_naive,lwd=2,col='green')
lines(timeaxis,product_of_means_naive,lwd=2,col='grey')
lines(timeaxis,real_likelihood,lwd=1,col='purple')

Arrows(x0=1,y0=.75,x1=20,y1=.75,code=3, arr.type='triangle')
dev.off()
#####


# Figure 3d
##################


####
# 
# 
# plot_individual_time_likelihood(n=n,times=timeaxis,time=illustration_timestart,set_of_positive_curves=plotdata_positive,set_of_negative_curves=plotdata_negative)
# 
# jpeg("frame_time_%03d.jpg")
# for (time in seq(illustration_timestart,illustration_timestart + illustration_number_timesteps*illustration_timestep_size,illustration_timestep_size)){
#   plot_individual_time_likelihood(n=n, times=timeaxis,time=time,set_of_positive_curves = plotdata_positive,set_of_negative_curves = plotdata_negative)
# }
# dev.off()

# plot_individual_time_likelihood(n=n, times=timeaxis,time=38,set_of_positive_curves = plotdata_positive,set_of_negative_curves = plotdata_negative,cuttoff=1)

DDI_hypothetical=80

plot_individual_time_likelihood(test_of_interest = "positive",n=n, times=timeaxis,time=DDI_hypothetical,set_of_positive_curves = plotdata_positive,set_of_negative_curves = plotdata_negative)

#   at some point:
#   	- calculate/plot mean curve for a set of curves DONE
#   next:
#   	- generate positive likelihood curves DONE
#   for every time point:
#   	- we want to select a curve from the family of negative curves (randomly - or do we just select one of each) and get the likelihood DONE for selecting one of each
#   	- select the same curve from the family of positive curves (randomly) and get the likelihood (this is the conditional likelihood)
#   	- get the product of the likelihoods
#   	- do this a bunch of times (or for all the people), representing sampling from the population for a particular fDDI - first Date of Detectable Infection DONE "For all the people"

#   Next up:
#     - portray more likely people with dotted lines, given a particular time point
#         - choose a nice step amount and pick particular values in the timeaxis
#         - for all curves that have a value (at that time) of less than 1/2 display as dotted line.
























## Now old code removed in favor of slightly more *sensitive* code ;)


#put in a check to make sure nobody is detectable before infection

# The next functions generate families of positive/negative curves. These are meant to represent the population-variability in the probabilities of testing positive/negative given some
# delay between infection and testing.

# #negative curves
# individual_negative_curve_weibul = function(x,scale,shape,position){
#   #ifelse(x-position<0,0,1-exp(-((x-position)/shape)^shape))
#   return(ifelse(x-position<0,0,1-exp(-((x-position)/scale)^shape))) #will definitely not test negative if fDDT is before position = center position minus shift
# }
# 
# 
# generate_individual_negative_curve_weibul = function(scale,shape,position,timeaxis){
#   #scale is lambda
#   #shape is k (exponent of exponent)
#   #center_position is the position of the half-likelihood
#   #timeaxis is a vector of t-axis values. Suggest creating one centrally then passing to all functions
#   return(individual_negative_curve_weibul(timeaxis,scale,shape,position))
# }
# 
# generate_family_negative_curves = function(n,scale,shape,mean_center_position,sd_size,timeaxis){
#   list_of_positions = generate_positions_for_individual_curves_normal(n=n, scale=scale, shape=shape, mean_center_position=mean_center_position, sd_size=sd_size)
#   set_of_negative_curves = matrix(nrow=length(timeaxis),ncol=n)
#   for (i in seq(1,n)){
#     set_of_negative_curves[,i]=generate_individual_negative_curve_weibul(scale=scale, shape=shape, position = list_of_positions[i], timeaxis=timeaxis)
#   }
#   return(set_of_negative_curves)
# }
# #positive curves
# individual_positive_curve = function(x,scale,shape,position){
#   #ifelse(x-position<0,1,exp(-((x-position)/shape)^shape))
#   return(ifelse(x-position<0,1,exp(-((x-position)/scale)^shape))) #definitely test positive if fDDT is before position = center position minus shift
# }
# 
# 
# #rules for update:
# # each functional form should be defined so that the position input is at the half-likelihood point.
# 
# 
# 
# 
# generate_individual_positive_curve = function(scale,shape,position,timeaxis){
#   return(individual_positive_curve(timeaxis,scale,shape,position))
# }
# 
# generate_family_positive_curves = function(n,scale,shape, mean_center_position,sd_size,timeaxis){
#   list_of_positions = generate_positions_for_individual_curves_normal(n=n, scale=scale, shape=shape, mean_center_position = mean_center_position, sd_size=sd_size)
#   set_of_positive_curves = matrix(nrow=length(timeaxis),ncol=n)
#   for (i in seq(1,n)){
#     set_of_positive_curves[,i] = generate_individual_positive_curve(scale=scale, shape=shape, position=list_of_positions[i], timeaxis=timeaxis)
#   }
#   return(set_of_positive_curves)
#   
# }






    ###extra stuff for testing (delete)
#myseq = seq(1/(2*n),1-1/(2*n),1/n)
#diff(myseq);
#diff(qnorm(myseq,mean=mean_center_position,sd=.1))
#n/30
#length(qnorm(myseq,mean=0.5,sd=.24))
#plot(myseq,qnorm(myseq,mean=0.5,sd=.24),xlim=c(0,1),ylim=c(0,1))
#plot(qnorm(myseq,mean=.5,.24),as.list(rep(1, n)),xlim=c(0,1))
#plot(x, y, main="title", sub="subtitle",xlab="X-axis label", ylab="y-axix label",xlim=c(xmin, xmax), ylim=c(ymin, ymax))
#qnorm(myseq,mean=mean_center_position,sd=sd_size)

#calculate_nth_person_total_likelihood = function(family_negative_likelihoods,family_positive_likelihoods,n) {#unnecessary function
#return(family_positive_likelihoods[,n]*family_negative_likelihoods[,n])
#}

##given a time, find where in the timeshape it fits
#calculate_time_index = function(timeshape, time){
#  return(which(abs(timeshape-time) == min(abs(timeshape-time))))
  
#}

##given a time, calculate the likelihood that one person would get the two test results
#calculate_total_likelihood_for_nth_person = function(timeshape,time, n, family_negative_likelihoods, family_positive_likelihoods){
#  time_index = calculate_time_index(timeshape=timeshape, time=time)
#  return(family_negative_likelihoods[time_index,n]*family_positive_likelihoods[time_index,n])
#}

#select an individual curve
#select_individual_curve_randomly = function(set_of_curves){
#}

#So, at the end of the day I want to be able to input a shape of an arbitrary representative set of test sensitivity_functions, assume uniform distribution of probabilities of infection times, and calculate the probability of being infected but not detected at some test time t. So given a distribution of sensitivity curves, I'll shift them according to the test time.
#ie I should generate the sensitivity curves first, THEN reverse them and [for negative test] flip them, then add them to the test time. (so they will all be defined just for negative time but if we add them to the positive test time that will constitute a shift - so they will all be for some time BEFORE the test). Does that make sense?
#



#Generality attempt


# generate_positions_for_individual_curves_normal = function(n,mean_displacement,sd_size){
#   myseq <- seq(1/(2*n),1-1/(2*n),1/n)
#   positions <- qnorm(myseq,mean=mean_displacement,sd=sd_size)
#   return(positions)
# }
# 
# n=50
# 
# mean_diagnostic_delay_postive
# mean_diagnostic_delay_negative
# 
# time_neg
# time_pos
# 
# 
# [pos,neg] <-
# 
# 
#   generate_ind_likelihoods <- function(test_pos, test_neg, time_pos, time_neg) {
#     return(pos_matrix, neg_matrix)
#   }



#complete-ISH attempt

# #############################################################################################################################################################################################################
# 
# # 
# # 
# # weibull <- function(t, params){
# #   return(ifelse(t-params$position<0,0,1-exp(-((t-params$position)/params$scale)^params$shape)))
# # }
# # # New rough draft
# # 
# # cum_norm_param_vals <- function(n,mean_delay,sd_delay) {
# #   myseq <- seq(1/(2*n),1-1/(2*n),1/n)
# #   param_vals <- qnorm(myseq,mean=mean_delay,sd=sd_delay)
# #   return(param_vals)
# # }
# # weibul_sensitivity = function(x,params){
# #   #position is an optional displacement
# #   return(ifelse(x-params$position<0,0,1-exp(-((x-params$position)/params$scale)^params$shape)))
# # }
# # 
# # neg_positions <- cum_norm_param_vals(n=15, mean_delay = 15, sd_delay = 10)
# # pos_positions <- cum_norm_param_vals(n=15, mean_delay = 10, sd_delay = 7) 
# # 
# # #specify scenario. I suggest:
# # # specify test profiles
# # # specify test times
# # # generate the rest...
# # test1 <- c(sensitivity_function = "weibull", test_params = c(scale = 5, shape = 5, position = 0), 
# #               variable_param = "position", variable_param_values = neg_positions)
# # 
# # test2 <- list(sensitivity_function=weibull, params=list(shape=5,color=2,slope=100, position = list(cum_norm_param_vals(10,10,1))), result="negative")
# # 
# # generate_individual_likelihood_curve <- function(test, timeaxis, test_time) { #this function can't take a set of positions - maybe just leave this out and generate a whole set every time....
# #     #browser()
# #     print(test$params)
# #     with(test, {
# #       #create array of parameters
# #       #empty array
# #       #for each item in the params list (manualy? add it to the )
# #       #then feed that array to the function, which takes only the peieces it wants...
# #       print(sensitivity_function)
# #       print("parameters are")
# #       print(params)
# #       if (result == "positive"){
# #         return(1 - sensitivity_function(t = test_time - timeaxis, params=params))}
# #       else if (result == "negative"){
# #       return(sensitivity_function(t = test_time - timeaxis, params=params))}
# #   })
# # }
# 
# # generate_family_likelihood_curves <- function(test,timeaxis,test_time){
# #   with(test,{
# #     for (i in which(length(params)>1)){
# #     print(i)  
# #     }
# #   })
# # }
# 
# 
# generate_family_likelihood_curves(test=test2,timeaxis=timeaxis,test_time=50)
# generate_individual_likelihood_curve(test2,timeaxis,50)

