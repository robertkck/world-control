library(tidyverse)
library(rtweet)

token <- create_token(
  app = "world-control",
  consumer_key = "ayGzE6WOvZf5vLGTd5lrLpMes",
  consumer_secret = "HscCoFzBB29nABNc69OIuLXWK6tigib9KPkfbP4gBxV7pvsbyo")

# fakenewz <- search_tweets("#fakenewz", n = 18000, include_rts = FALSE)
tru <- search_tweets("@truWorldControl", n = 18000, include_rts = FALSE)

df <- tru %>% filter(str_detect(text, "fakenewz"))
