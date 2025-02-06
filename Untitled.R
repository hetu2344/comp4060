
library(tidyverse)
library(ggplot2)
data <- read.csv("~/Documents/comp4060/assignments/as1/readings.csv")
head(data)

data <- data %>%
            mutate(x_diff = 0 - X) %>%
            mutate(y_diff = Y - 1000) %>%
            mutate(xdiff_bar = mean(x_diff)) %>%
            mutate(ydiff_bar = mean(y_diff)) %>%
            mutate(xdiff_sd = sd(x_diff)) %>%
            mutate(ydiff_sd = sd(y_diff))

head(data)

plot.10 <- ggplot(data, aes(x = x_diff, y = y_diff)) + 
           geom_point(data = subset(data, Hz == 10), col = "blue") +
           labs(x = "x error", y = "y error", title = "1m, 10hz, 100mm/s")
           
plot.10

plot.10 <- ggplot(data, aes(x = x_diff, y = y_diff)) + 
  geom_point(data = subset(data, Hz == 1), col = "blue") +
  labs(x = "x error", y = "y error", title = "1m, 1hz, 100mm/s")

plot.10

plot.10 <- ggplot(data, aes(x = x_diff, y = y_diff)) + 
  geom_point(data = subset(data, Hz == 30), col = "blue") +
  labs(x = "x error", y = "y error", title = "1m, 30hz, 100mm/s")

plot.10