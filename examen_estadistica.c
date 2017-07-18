//PARA COMPILAR:
//gcc examen_estadistica.c -o examen_estadistica -lgsl -lgslcblas -lm -lpthread

#include <stdio.h>
#include <math.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_cdf.h>
#include <time.h>
#include <pthread.h>

int hilos = 7;
int m_desde = 10, m_hasta = 1100, n_desde = 10, n_hasta = 1100;
int repeticiones = 100;
gsl_rng *rng;  // random number generator
float pv1[1090][1090];
float pv2[1090][1090];

void *myThreadFun(void *i);
void normal(const gsl_rng * r, float mu, float *x, int n);
float mean(float *x, int n);
float var(float *x, int n);
float var2(float *x, int n, float media);
struct timespec start, finish;

int main(void){

    long seed = 12345;
	pthread_t pth[hilos];	// this is our thread identifier
    int m, n, i;

    FILE *f = fopen("resultado.csv", "w");
	if (f == NULL) {
        printf ("Error al abrir el archivo de resultados, errno = %d\n", errno);
        return(1);
    }	
	
	rng = gsl_rng_alloc (gsl_rng_rand48);     // pick random number generator
    gsl_rng_set (rng, seed);                  // set seed	
	
	clock_t begin = clock();
	
	for(i = 0; i < hilos; i++){
		int *id = malloc(sizeof(*id));
		*id = i;
		pthread_create(&pth[i],NULL,myThreadFun, id);
	}
	
	for(i = 0; i < hilos; i++){
		pthread_join(pth[i],NULL);
	}
	
	
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

    for(m = m_desde; m < m_hasta; m++){
        for(n = n_desde; n < n_hasta; n++){
            fprintf(f, "%d,%d,%f,%f\n", m, n, pv1[m-m_desde][n-n_desde], pv2[m-m_desde][n-n_desde]);
        }
    }
    fclose(f);
	printf("%f\n", time_spent);
	//gsl_rng_free (rng);                       // dealloc the rng  
    return(0);
}

void normal(const gsl_rng * r, float mu, float *x, int n){
	int i;
    for(i = 0; i < n; i++){ 
        x[i] = gsl_ran_gaussian(r, 1) + mu;
    }
}

float mean(float *x, int n){
    float media = 0;
	int i;
    for(i = 0; i < n; i++){ 
        media += x[i];
    }
    return(media/n);
}

float var2(float *x, int n, float media){
    float var = 0;
	int i;	
    for(i = 0; i < n; i++){ 
        var += pow((x[i]-media), 2);
    }
    return(var/(n-1));    
}

float var(float *x, int n){
    float media = mean(x, n);
    float var = 0;
	int i;	
    for(i = 0; i < n; i++){ 
        var += pow((x[i]-media), 2);
    }
    return(var/(n-1));    
}

void *myThreadFun(void *tid){
    // Store the value argument passed to this thread
    int id = *((int *) tid);
	free(tid);
	struct timespec start, finish;
	double elapsed;	
	int carga = ceil((m_hasta - m_desde)/(float)hilos);
	int desde = carga*id + m_desde;
	int hasta = carga*(id+1) + m_desde;
	if(hasta > m_hasta) hasta = m_hasta; //Corregimos los límites para que no se pase
    int m, n, i;	
	for(m = desde; m < hasta; m++){
        clock_gettime(CLOCK_MONOTONIC, &start);
        for(n = n_desde; n < n_hasta; n++){
            int df = m + n - 2;
            pv1[m-m_desde][n-n_desde] = 0;
            pv2[m-m_desde][n-n_desde] = 0;            
            for(i = 0; i < repeticiones; i++){
                float *x = (float *) malloc(m * sizeof(float));
                float *y = (float *) malloc(n * sizeof(float));
                normal(rng, 0.2, x, m);
                normal(rng, 0, y, n);
                float media_x = mean(x, m);
                float media_y = mean(y, m);
                float var_x   = var2(x, m, media_x);
                float var_y   = var2(y, n, media_y);
                float denominador = (1./m + 1./n)*(var_x*(m-1)+var_y*(n-1));
                
                float u1 = (media_x-media_y)*sqrt(df/denominador);
                pv1[m-m_desde][n-n_desde] += 1-gsl_cdf_tdist_P(u1, df);
                
                float u2 = (media_x-media_y)/sqrt(var_x/m + var_y/n);
                float dof = round(pow(var_x/m + var_y/n, 2)/( pow(var_x/m, 2)/(m-1) + pow(var_y/n, 2)/(n-1) ));
                pv2[m-m_desde][n-n_desde] += 1-gsl_cdf_tdist_P(u2, dof);
                
                free(x);
                free(y); 
            }
            pv1[m-m_desde][n-n_desde] = pv1[m-m_desde][n-n_desde]/repeticiones;
            pv2[m-m_desde][n-n_desde] = pv2[m-m_desde][n-n_desde]/repeticiones;            
        }
        clock_gettime(CLOCK_MONOTONIC, &finish);
		elapsed = (finish.tv_sec - start.tv_sec);
		elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
		printf("thread: %d (%d,%d) : [%d - %f]\n", id, desde, hasta-1, m, elapsed);
    }
}
