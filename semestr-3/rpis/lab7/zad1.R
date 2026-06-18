obserwowane <- c(171, 200, 168, 213, 226, 222)

# a)
# H0: Kostka jest symetryczna (każda ściana ma takie samo prawdopodobieństwo 1/6)
# H1: Kostka nie jest symetryczna (przynajmniej jedno prawdopodobieństwo różni się od 1/6)
n <- sum(obserwowane)
oczekiwane <- rep(n / 6, 6)
oczekiwane

# b)
statystyka <- sum((obserwowane - oczekiwane)^2 / oczekiwane)
statystyka

# c)
df <- 5
p_value <- 1 - pchisq(statystyka, df)
p_value

# d)

# Odrzucamy na poziomie istotności 1% (0,001<p<0,01): Mamy mocne dowody przeciwko H0

# e)
chisq.test(obserwowane)
