dane <- floor(runif(600, 0, 1) * 6 + 1)
mean(dane)
var(dane)
35/12
table(dane)
ramka <- as.data.frame(dane)
var(ramka)

probka <- sample(1:6, size = 600, replace = TRUE)
mean(probka)
var(probka)
table(probka)
#hist(probka)
