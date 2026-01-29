# a) Próba z rozkładu wykładniczego
set.seed(123)
proba_exp <- rexp(1000, rate = 1)

# b) Testy dla próby wykładniczej
# i) Test z rozkładem normalnym
# H0: Próba pochodzi z rozkładu normalnego N(μ, σ²)
# H1: Próba nie pochodzi z rozkładu normalnego
srednia_exp <- mean(proba_exp)
odch_exp <- sd(proba_exp)
ks.test(proba_exp, "pnorm", mean = srednia_exp, sd = odch_exp)

# ii) Test z rozkładem wykładniczym
# H0: Próba pochodzi z rozkładu wykładniczego Exp(λ=1)
# H1: Próba nie pochodzi z rozkładu wykładniczego Exp(λ=1)
ks.test(proba_exp, "pexp", rate = 1)

# c) Próba z rozkładu Gamma
proba_gamma <- rgamma(1000, shape = 100, scale = 1)

# d) Testy dla próby Gamma
# i) Test z rozkładem normalnym
# H0: Próba pochodzi z rozkładu normalnego N(μ, σ²)
# H1: Próba nie pochodzi z rozkładu normalnego
srednia_gamma <- mean(proba_gamma)
odch_gamma <- sd(proba_gamma)
ks.test(proba_gamma, "pnorm", mean = srednia_gamma, sd = odch_gamma)

# ii) Test z rozkładem Gamma
# H0: Próba pochodzi z rozkładu Gamma(100, 1)
# H1: Próba nie pochodzi z rozkładu Gamma(100, 1)
ks.test(proba_gamma, "pgamma", shape = 100, scale = 1)
