# 3.
# a)
path <- "~/Documents/coding/coursework-wust/rpis/lab2/mieszkania.csv"
dane <- read.csv2(path)
# b)
head(dane)
# c)
str(dane)
# d)
mean(dane$Metraz)
mean(dane$Cena)
# e)
dane$Cena_za_m2 <- dane$Cena / dane$Metraz
# f)
# dane[dane$Dzielnica == "Psie Pole" & dane$Cena < 400000, ]
subset(dane, Dzielnica == "Psie Pole" & Cena < 400000)
# g)
# dane[dane$Dzielnica == "Srodmiescie" & dane$Metraz > 60, ]
subset(dane, Dzielnica == "Srodmiescie" & Metraz > 60)
# h)
sum(dane$Metraz > 60 & dane$Cena < 350000)
# i)
dane[which.max(dane$Metraz / dane$Pokoje / dane$Cena), ]
# j)
dzielnica <- c()
odchylenie <- c()
dzielnice_z_odchyleniem <- data.frame(
  dzielnica,
  odchylenie
)
for (dzielnica in unique(dane$Dzielnica)) {
  dane_w_dzielnicy <- dane[dane$Dzielnica == dzielnica, ]
  stddev <- sd(dane_w_dzielnicy$Cena)
  dzielnice_z_odchyleniem <- rbind(dzielnice_z_odchyleniem, c(dzielnica, stddev))
}
print(dzielnice_z_odchyleniem)
# najwiekszy odchylenie (najmniej stabilne)
dzielnice_z_odchyleniem[which.max(dzielnice_z_odchyleniem[, 2]), ]
# najmniejsze odchylenie (najbardziej stabilne)
dzielnice_z_odchyleniem[which.min(dzielnice_z_odchyleniem[, 2]), ]
