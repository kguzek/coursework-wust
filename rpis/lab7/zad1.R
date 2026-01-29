obserwowane <- c(171, 200, 168, 213, 226, 222)

# a) Oczekiwane frekwencje przy hipotezie o symetrycznej kostce
# H0: Kostka jest symetryczna (każda ściana ma takie samo prawdopodobieństwo 1/6)
# H1: Kostka nie jest symetryczna (przynajmniej jedno prawdopodobieństwo różni się od 1/6)
n <- sum(obserwowane)
oczekiwane <- rep(n / 6, 6)
oczekiwane

# b) Statystyka testowa
statystyka <- sum((obserwowane - oczekiwane)^2 / oczekiwane)
statystyka

# c) Wartość p
df <- 5
p_value <- 1 - pchisq(statystyka, df)
p_value

# d) Wniosek
# Przy α=0.05, jeśli p < 0.05 odrzucamy H0, w przeciwnym razie nie ma podstaw do odrzucenia H0

# e) Test za pomocą chisq.test
chisq.test(obserwowane)
