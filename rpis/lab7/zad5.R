dane <- read.csv("~/Documents/coding/coursework-wust/rpis/lab7/bakteria.csv")

# a) Wykres rozrzutu masy względem czasu
plot(dane$czas, dane$masa)

# b) Model liniowy dla logarytmu masy
dane$log_masa <- log(dane$masa)
model_log <- lm(log_masa ~ czas, data = dane)
summary(model_log)

# c) Regresja wykładnicza - oszacowanie masy
a <- coef(model_log)[1]
b <- coef(model_log)[2]
masa_predykcja <- exp(a) * exp(b * dane$czas)
masa_predykcja
