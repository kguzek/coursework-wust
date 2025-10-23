# 1.
# a)
imie <- c("Krzysztof", "Maria", "Henryk", "Anna")
plec <- c("m", "k", "m", "k")
analiza <- c(3.5, 4.5, 5.0, 4.5)
algebra <- c(4.0, 5.0, 4.0, 3.5)
oceny <- data.frame(
  imie,
  plec,
  analiza,
  algebra
)
# b)
# oceny[1:2, ]
head(oceny, 2)
# c)
str(oceny)
# d)
mean(oceny[, 3])
# e)
oceny$Srednie <- (oceny[, 3] + oceny[, 4]) / 2
# f)
# oceny[oceny$plec == "k", ]
subset(oceny, plec == "k")
# g)
# oceny[oceny$analiza >= 4.5 | oceny$algebra >= 4.5, ]
subset(oceny, analiza >= 4.5 | algebra >= 4.5)
# h)
sum(oceny$analiza >= 4.5 | oceny$algebra >= 4.5)