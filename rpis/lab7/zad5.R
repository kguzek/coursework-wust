dane <- read.csv2("~/Documents/coding/coursework-wust/rpis/lab7/bakteria.csv")

# a)
plot(dane$czas, dane$masa)

# b)
dane$log_masa <- log(dane$masa)
model_log <- lm(log_masa ~ czas, data = dane)
summary(model_log)

# c)
a <- coef(model_log)[1]
b <- coef(model_log)[2]
masa_predykcja <- exp(a) * exp(b * dane$czas)
masa_predykcja
