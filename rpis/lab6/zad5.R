d <- read.csv("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: 80% studentów przybywa na wadze
# H1: odsetek przybierających na wadze jest inny niż 80%

d$przybral <- ifelse(d$po > d$przed, 1, 0)
prop.test(sum(d$przybral), nrow(d), p = 0.8, correct = FALSE)
