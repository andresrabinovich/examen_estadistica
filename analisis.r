library(ggplot2)

U1 <- function(mu_x, mu_y, var_x, var_y, m, n){
  df = (m + n - 1)
  denominador = (1/m + 1/n)*(var_x*(m-1)+var_y*(n-1));
  U1 = (mu_x-mu_y)*sqrt(df/denominador);
  return(U1)
}

U2 <- function(mu_x, mu_y, var_x, var_y, m, n){
  U2 = (mu_x-mu_y)/sqrt( var_x/(m*(m-1)) + var_y/(n*(n-1)) );
  return(U2)
}

poder_U1 <- c()
poder_U2 <- c()
for (m in seq(from=10, to=1100, by=50)){
  for (n in seq(from=10, to=1100, by=50)){
    x <- matrix(rnorm(m*2000, 0.1, 1), ncol=m, byrow=TRUE)
    y <- matrix(rnorm(m*2000, 0, 1), ncol=m, byrow=TRUE)
    mu_x <- rowMeans(x)
    mu_y <- rowMeans(y)
    var_x <- apply(x, 1, var)
    var_y <- apply(y, 1, var)
    H1_U1<-U1(mu_x, mu_y, var_x, var_y, m, n)
    H1_U2<-U2(mu_x, mu_y, var_x, var_y, m, n)    
    x <- matrix(rnorm(m*2000, 0, 1), ncol=m, byrow=TRUE)
    y <- matrix(rnorm(m*2000, 0.1, 1), ncol=m, byrow=TRUE)
    mu_x <- rowMeans(x)
    mu_y <- rowMeans(y)
    var_x <- apply(x, 1, var)
    var_y <- apply(y, 1, var)    
    H0_U1<-sort(U1(mu_x, mu_y, var_x, var_y, m, n))
    H0_U2<-sort(U2(mu_x, mu_y, var_x, var_y, m, n))
    v_critico_U1 <- H0_U1[floor(0.95*2000)]
    poder_U1 <- c(poder_U1, 1-sum(H1_U1 < v_critico_U1)/2000)
    v_critico_U2 <- H0_U2[floor(0.95*2000)]
    poder_U2 <- c(poder_U2, 1-sum(H1_U2 < v_critico_U2)/2000)    
  }
  print(m)
}

mpoder <- expand.grid(n = seq(from=10, to=1100, by=50)
                      ,m = seq(from=10, to=1100, by=50)
)
mpoder$poder_U1 <- poder_U1
mpoder$poder_U2 <- poder_U2

write.csv(mpoder, file = "~/Desktop/examen_estadistica/corridas/poder_02.csv")

ggplot(data = mpoder) +
  geom_raster(aes(x = m, y = n, fill = poder_U2), interpolate = TRUE) +
  scale_fill_gradient(low = "darkblue", high = "darkred")

n = m = 900

H <- data.frame(resultado=c(H0_U1, H1_U1), test=rep(c("H0_U1", "H1_U1"), each=length(H0_U1)))
ggplot(H, aes(x=resultado, fill=test)) + geom_histogram(alpha=0.2, position="identity") +  
   labs(x = "U", y = "Cantidad", title = "Distribución de U1 con diferencia de medias 0.1" ) + 
   geom_vline(xintercept=v_critico_U1, colour="red")

H <- data.frame(resultado=c(H0_U2, H1_U2), test=rep(c("H0_U2", "H1_U2"), each=length(H0_U1)))
ggplot(H, aes(x=resultado, fill=test)) + geom_histogram(alpha=0.2, position="identity") +  
  labs(x = "U", y = "Cantidad", title = "Distribución de U2 con diferencia de medias 0.1" ) + 
  geom_vline(xintercept=v_critico_U2, colour="red")

poder_U1 <- c()
poder_U2 <- c()
for (m in seq(from=10, to=1100, by=50)){
  for (n in seq(from=10, to=1100, by=50)){
    x <- matrix(rnorm(m*20000, 0.1, 1), ncol=m, byrow=TRUE)
    y <- matrix(rnorm(m*20000, 0, 1), ncol=m, byrow=TRUE)
    mu_x <- rowMeans(x)
    mu_y <- rowMeans(y)
    var_x <- apply(x, 1, var)
    var_y <- apply(y, 1, var)
    H1_U1<-U1(mu_x, mu_y, var_x, var_y, m, n)
    H1_U2<-U2(mu_x, mu_y, var_x, var_y, m, n)    
    x <- matrix(rnorm(m*2000, 0, 1), ncol=m, byrow=TRUE)
    y <- matrix(rnorm(m*2000, 0.1, 1), ncol=m, byrow=TRUE)
    mu_x <- rowMeans(x)
    mu_y <- rowMeans(y)
    var_x <- apply(x, 1, var)
    var_y <- apply(y, 1, var)    
    H0_U1<-sort(U1(mu_x, mu_y, var_x, var_y, m, n))
    H0_U2<-sort(U2(mu_x, mu_y, var_x, var_y, m, n))
    #for(i in seq(from=0, to=1, by=))
    v_critico_U1 <- H0_U1[floor(0.95*2000)]
    poder_U1 = c()
    for(i in sort(H1_U1)){
      poder_U1 <- c(poder_U1, sum(H1_U1 <= i))
    }
    poder_U1 <- poder_U1/20000
    v_critico_U2 <- H0_U2[floor(0.95*2000)]
    poder_U2 <- c(poder_U2, 1-sum(H1_U2 < v_critico_U2)/2000)    
  }
  print(m)
}
