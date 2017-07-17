library(reshape2)
library(ggplot2)
A<-matrix(resultado_b$X4, ncol=1090, nrow=1090, byrow = TRUE)
longData<-melt(A)
longData<-longData[longData$value!=0,]
ggplot(longData, aes(x = Var2, y = Var1)) + 
  geom_raster(aes(fill=value)) + 
  scale_fill_gradient(low="blue", high="red") +
  labs(x="m", y="n", title="Matrix") +
  theme_bw() + theme(axis.text.x=element_text(size=9, angle=0, vjust=0.3),
                     axis.text.y=element_text(size=9),
                     plot.title=element_text(size=11))
