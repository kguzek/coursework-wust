(A <- rbind(c(-3, 1, -2), c(4, -5, 3)))
(B <- matrix(1:6, ncol = 2, byrow = TRUE))
(C <- matrix(c(7, -3, -2, 1), nrow = 2))
(D <- cbind(c(1, 3, 2), c(2, 5, 3), c(4, 7, 2)))

(A + B)
(t(A) + B)
(B %*% A)
(B * B)
(C_solved <- solve(C))
(C %*% C_solved)

(B %*% C_solved)
(solve(D, B))
