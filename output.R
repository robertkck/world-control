library(tidyverse)

pdf('foo.pdf', paper='a4', pagecentre=FALSE)
plot.new()
text(0, .5, df %>% select(text) %>% print(), pos=4, offset=0)
dev.off()