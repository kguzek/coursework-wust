d <- read.csv("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: studenci średnio przytyli się o 2kg
# H1: studenci średnio przytyli się o inną wartość niż 2kg

t.test(d$przed, d$po, paired = TRUE, mu = 2)

# Skoro p>0.05, nie odrzucamy H0 na poziomie istotnosci 5%.
# Nie mamy dowodow ze studenci przytyli sie o inna wartosc niz 2kg.
