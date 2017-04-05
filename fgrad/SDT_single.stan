data {
	int<lower=1> k; # number of subjects
	int<lower=0> h[k]; # Hits
	int<lower=0> f[k]; # False Alarms
	int<lower=1> n[k]; # False Alarms + correct rejections 
	int<lower=1> s[k]; # Hits + misses
}

parameters {
	real muc; # mean bias
	real mud; # mean discriminability
	real<lower=0> sigmac; # sd bias
	real<lower=0> sigmad; # sd discriminability
	real c[k];
	real<lower=0> d[k];

}

model {

	#Priors
	muc ~ normal(0,100);
	mud ~ normal(0,100);
	sigmac ~ cauchy(0,1)T[0,];
	sigmad ~ cauchy(0,1)T[0,];
	c ~ normal(muc,sigmac);
	d ~ normal(mud,sigmad);
	
	for (i in 1:k) {
          h[i] ~ binomial(s[i],Phi(d[i]/2-c[i]));
          f[i] ~ binomial(n[i],Phi(-d[i]/2-c[i]));
	}
}