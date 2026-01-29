# a)
set.seed(123)
proba_exp <- rexp(1000, rate = 1)

# b)
# i)
# H0: Próba pochodzi z rozkładu normalnego N(μ, σ²)
# H1: Próba nie pochodzi z rozkładu normalnego
srednia_exp <- mean(proba_exp)
odch_exp <- sd(proba_exp)
ks.test(proba_exp, "pnorm", mean = srednia_exp, sd = odch_exp)

# Odrzucamy na poziomie istotności 0,1% (p<0,001): Mamy bardzo mocne dowody przeciwko H0

# ii)
# H0: Próba pochodzi z rozkładu wykładniczego Exp(λ=1)
# H1: Próba nie pochodzi z rozkładu wykładniczego Exp(λ=1)
ks.test(proba_exp, "pexp", rate = 1)

# Nie odrzucamy na poziomie istotności 5% (p>0,05): Nie mamy dowodów przeciwko H0

# c)
proba_gamma <- rgamma(1000, shape = 100, scale = 1)

# d)
# i)
# H0: Próba pochodzi z rozkładu normalnego N(μ, σ²)
# H1: Próba nie pochodzi z rozkładu normalnego
srednia_gamma <- mean(proba_gamma)
odch_gamma <- sd(proba_gamma)
ks.test(proba_gamma, "pnorm", mean = srednia_gamma, sd = odch_gamma)

# Nie odrzucamy na poziomie istotności 5% (p>0,05): Nie mamy dowodów przeciwko H0

# ii)
# H0: Próba pochodzi z rozkładu Gamma(100, 1)
# H1: Próba nie pochodzi z rozkładu Gamma(100, 1)
ks.test(proba_gamma, "pgamma", shape = 100, scale = 1)

# Nie odrzucamy na poziomie istotności 5% (p>0,05): Nie mamy dowodów przeciwko H0
