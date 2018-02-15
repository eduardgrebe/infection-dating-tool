#Tool for generating plots that illustrate the value of the knowing the details of individual HIV detectability
#Definitions



  # The next section of code defines functions that are used to:
# choose a set of half-likelihood positions for a family of curves, with spacing defined using an inverse cumulative normal distribution
# define and generate individual curves
# Generate families of n curves with half-likelihoods distributed around mean_center_position
# Note: generate_family function don't return the time axis - this should be defined somewhere more central in the script.

  ##parameters are as follows
#slope is lambda
#scale is k (exponent of exponent)
#center_position is the position of the half-likelihood for an individual curve
#mean_center_position is the mean position of half likelihood for a family of curves
#sd_size is the standard deviation size of the normal distribution which is used to generate the half-likelihood positions
#timeaxis is a vector of t-axis values. Should be defined centrally then passed to all functions


generate_positions_for_individual_curves = function(n,slope,scale,mean_center_position,sd_size){
  shift_to_half_likelihood = slope*(-1*log(1/2))^(1/scale)
  myseq <- seq(1/(2*n),1-1/(2*n),1/n)
  positions <- qnorm(myseq,mean=mean_center_position-shift_to_half_likelihood,sd=sd_size)
  return(positions)
}

#negative curves
individual_negative_curve = function(x,slope,scale,position){
  return(ifelse(x-position<0,0,1-exp(-((x-position)/slope)^scale))) #will definitely not test negative if fDDT is before position = center position minus shift
}
generate_individual_negative_curve = function(slope,scale,position,timeaxis){
  #slope is lambda
  #scale is k (exponent of exponent)
  #center_position is the position of the half-likelihood
  #timeaxis is a vector of t-axis values. Suggest creating one centrally then passing to all functions
  return(individual_negative_curve(timeaxis,slope,scale,position))
}

generate_family_negative_curves = function(n,slope,scale,mean_center_position,sd_size,timeaxis){
  list_of_positions = generate_positions_for_individual_curves(n=n, slope=slope, scale=scale, mean_center_position=mean_center_position, sd_size=sd_size)
  set_of_negative_curves = matrix(nrow=length(timeaxis),ncol=n)
  for (i in seq(1,n)){
    set_of_negative_curves[,i]=generate_individual_negative_curve(slope=slope, scale=scale, position = list_of_positions[i], timeaxis=timeaxis)
  }
  return(set_of_negative_curves)
}
#positive curves
individual_positive_curve = function(x,slope,scale,position){
  return(ifelse(x-position<0,1,exp(-((x-position)/slope)^scale))) #definitely test positive if fDDT is before position = center position minus shift
}
generate_individual_positive_curve = function(slope,scale,position,timeaxis){
  return(individual_positive_curve(timeaxis,slope,scale,position))
}

generate_family_positive_curves = function(n,slope,scale, mean_center_position,sd_size,timeaxis){
  list_of_positions = generate_positions_for_individual_curves(n=n, slope=slope, scale=scale, mean_center_position = mean_center_position, sd_size=sd_size)
  set_of_positive_curves = matrix(nrow=length(timeaxis),ncol=n)
  for (i in seq(1,n)){
    set_of_positive_curves[,i] = generate_individual_positive_curve(slope=slope, scale=scale, position=list_of_positions[i], timeaxis=timeaxis)
  }
  return(set_of_positive_curves)
  
}

#calculate the mean of a generic family of curves over a specified set of t-values
generate_mean_of_family = function(family_of_curves){
  return(rowMeans(family_of_curves))
}

#calculate the product of two curves
generate_product_curve = function(curve1,curve2){ #this doesn't need to be its own function I'm just renaming
  return(curve1*curve2)
}

#given a curve and find the likelihood for all times the combined test results.
likelihood_by_DDI = function(set_of_positive_curves,set_of_negative_curves,timeaxis){
  likelihoods_per_time = rep(0,length(timeaxis))
  for (tpos in seq(1:length(timeaxis))){
    cumu_likely=0
    for (person in seq(1:ncol(set_of_negative_curves))){ #chronological order makes a trivial difference - there is 
                                                          #just a product per person
      likelihood_forward = set_of_positive_curves[tpos,person]*set_of_negative_curves[tpos,person]
      likelihood_backward = "The same thing unless I don't actually understand this task"
      cumu_likely <- cumu_likely + likelihood_forward
    }
    likelihoods_per_time[tpos]=cumu_likely
  }
  return(likelihoods_per_time)
}


#ALSO
#nice plotting function showing likelihood for an individual time point (including dashed lines for unlikely people)

plot_individual_time_likelihood = function(n,timeaxis,set_of_positive_curves,set_of_negative_curves,time){
  #calculate means
  positive_mean_naive = rowMeans(set_of_positive_curves)
  negative_mean_naive = rowMeans(set_of_negative_curves)
  likelihood_naive <- negative_mean_naive*positive_mean_naive
  #position in timeaxis
  time_position <- which(timeaxis==time)
  #calculate_likelihood
  cumu_likely=0
  for (person in seq(1:ncol(set_of_negative_curves))){ #chronological order makes a trivial difference - there is 
    #just a product per person
    likelihood_forward = set_of_positive_curves[time_position,person]*set_of_negative_curves[time_position,person]
    likelihood_backward = "The same thing unless I don't actually understand this task"
    cumu_likely <- cumu_likely + likelihood_forward
  }
  likelihood_DDI_at_time_given_both_test_results = 1/n *cumu_likely
  #plot the curves
  plot(timeaxis,plotdata_negative[,1],type='l',xlim=c(timeaxis[1],timeaxis[length(timeaxis)]),ylim=c(0,1),xlab="t",ylab="Likelihood",col='red')
  #points(plotdata[,1],plotdata[,3])
  for (i in seq(1:n)){
    lines(timeaxis,plotdata_positive[,i],col='red') #what color should the positive curves be
  }
  #points(plotdata[,1],plotdata[,3])
  for (i in seq(2:n)){
    lines(timeaxis,plotdata_negative[,i],col='green') #what color should the negative curves be
  }
  lines(timeaxis,positive_mean_naive,lwd=2,col='red')
  lines(timeaxis,negative_mean_naive,lwd=2,col='green')
  lines(timeaxis,likelihood_naive, lwd=4,col='grey')
  points(time,likelihood_DDI_at_time_given_both_test_results)
}


# script
n=15
mean_center_position_negative_curves=45
mean_center_position_positive_curves=55
sd_size_positive = 15
sd_size_negative = sd_size_positive
detail = 10
timeaxis = seq(0,100,1/detail)
slope = 1
scale = 5

illustration_timestep_size = 2
illustration_timestart = 20
illustration_number_timesteps = 10

plotdata_negative = generate_family_negative_curves(n=n, slope=slope, scale=scale, mean_center_position=mean_center_position_negative_curves, sd_size= sd_size_negative, timeaxis = timeaxis)
plotdata_positive = generate_family_positive_curves(n=n, slope=slope, scale=scale, mean_center_position=mean_center_position_positive_curves, sd_size= sd_size_positive, timeaxis = timeaxis)

plot(timeaxis,plotdata_negative[,1],type='l',xlim=c(timeaxis[1],timeaxis[length(timeaxis)]),ylim=c(0,1.2),xlab="t",ylab="Likelihood",col='green')
#points(plotdata[,1],plotdata[,3])
for (i in seq(2:n)){
  lines(timeaxis,plotdata_negative[,i],col='green')
}
#points(plotdata[,1],plotdata[,3])
for (i in seq(1:n)){
  lines(timeaxis,plotdata_positive[,i],col='red')
}
positive_mean_naive <- rowMeans(plotdata_positive[,])
negative_mean_naive <- rowMeans(plotdata_negative[,])
product_of_means_naive <- positive_mean_naive*negative_mean_naive
real_likelihood <- 1/n*likelihood_by_DDI(timeaxis = timeaxis, set_of_positive_curves = plotdata_positive, set_of_negative_curves = plotdata_negative)
difference <- product_of_means_naive - real_likelihood
print("The maximum difference for this scenario between the true likelihood and the totally naive approximation is on the next line:")
print(max(difference))
lines(timeaxis,difference,lwd=1,col="blue")
lines(timeaxis,positive_mean_naive,lwd=2,col='red')
lines(timeaxis,negative_mean_naive,lwd=2,col='green')
lines(timeaxis,product_of_means_naive,lwd=4,col='grey')
lines(timeaxis,real_likelihood,lwd=1,col='purple')

plot_individual_time_likelihood(n=n,timeaxis=timeaxis,time=illustration_timestart,set_of_positive_curves=plotdata_positive,set_of_negative_curves=plotdata_negative)

jpeg("C:/Users/JumpCo Vostro3700/Pictures/code_for_discordant_test/frame_time_%03d.jpg")
for (time in seq(illustration_timestart,illustration_timestart + illustration_number_timesteps*illustration_timestep_size,illustration_timestep_size)){
  plot_individual_time_likelihood(n=n, timeaxis=timeaxis,time=time,set_of_positive_curves = plotdata_positive,set_of_negative_curves = plotdata_negative)
}
dev.off()
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

##given a time, find where in the timescale it fits
#calculate_time_index = function(timescale, time){
#  return(which(abs(timescale-time) == min(abs(timescale-time))))
  
#}

##given a time, calculate the likelihood that one person would get the two test results
#calculate_total_likelihood_for_nth_person = function(timescale,time, n, family_negative_likelihoods, family_positive_likelihoods){
#  time_index = calculate_time_index(timescale=timescale, time=time)
#  return(family_negative_likelihoods[time_index,n]*family_positive_likelihoods[time_index,n])
#}

#select an individual curve
#select_individual_curve_randomly = function(set_of_curves){
#}





