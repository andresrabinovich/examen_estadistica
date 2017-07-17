#include <stdio.h>
#include <math.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_cdf.h>
#include <time.h>

void normal(const gsl_rng * r, float mu, float *x, int n);
float mean(float *x, int n);
float var(float *x, int n);
float var2(float *x, int n, float media);

int main(void){

    double packet_size;
    long seed;
    gsl_rng *rng;  // random number generator
    rng = gsl_rng_alloc (gsl_rng_rand48);     // pick random number generator
    seed = 12345;    
    gsl_rng_set (rng, seed);                  // set seed
    int repeticiones = 100;
    int m_desde = 900, m_hasta = 1100, n_desde = 10, n_hasta = 1100;
    float pv1[m_hasta-m_desde][n_hasta-n_desde];
    float pv2[m_hasta-m_desde][n_hasta-n_desde];
    
    clock_t begin = clock();
    for(int m = m_desde; m < m_hasta; m++){
        clock_t beginp = clock();
        for(int n = n_desde; n < n_hasta; n++){
            int df = m + n - 2;
            pv1[m-m_desde][n-n_desde] = 0;
            pv2[m-m_desde][n-n_desde] = 0;            
            for(int i = 0; i < repeticiones; i++){
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
        clock_t endp = clock();
        double time_spent = (double)(endp - beginp) / CLOCKS_PER_SEC;        
        printf("[%d - %f]\n", m, time_spent);
    }
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
        
    /*
    printf("%f\n", media_x);
    printf("%f\n", media_y);    
    printf("%f\n", var_x);
    printf("%f\n", var_y); 
    printf("%f\n", u1); 
    */
    FILE *f = fopen("resultado_2.csv", "w");
    for(int m = m_desde; m < m_hasta; m++){
        for(int n = n_desde; n < n_hasta; n++){
            fprintf(f, "%d,%d,%f,%f\n", m, n, pv1[m-m_desde][n-n_desde], pv2[m-m_desde][n-n_desde]);
        }
    }
    fclose(f);
    printf("%f\n", time_spent);
    gsl_rng_free (rng);                       // dealloc the rng  
   
    return(0);
}

void normal(const gsl_rng * r, float mu, float *x, int n){
    for(int i = 0; i < n; i++){ 
        x[i] = gsl_ran_gaussian(r, 1) + mu;
    }
}

float mean(float *x, int n){
    float media = 0;
    for(int i = 0; i < n; i++){ 
        media += x[i];
    }
    return(media/n);
}

float var2(float *x, int n, float media){
    float var = 0;
    for(int i = 0; i < n; i++){ 
        var += pow((x[i]-media), 2);
    }
    return(var/(n-1));    
}

float var(float *x, int n){
    float media = mean(x, n);
    float var = 0;
    for(int i = 0; i < n; i++){ 
        var += pow((x[i]-media), 2);
    }
    return(var/(n-1));    
}
