d <- read.csv2("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: studenci średnio przytyli się o 2kg
# H1: studenci średnio przytyli się o inną wartość niż 2kg

t.test(d$Waga_przed, d$Waga_po, mu = 2)

# p-value: 0.006601
# Odrzucamy na poziomie istotności 1% (0,001<p<0,01): Mamy mocne dowody przeciwko H0
