#include <cuda_runtime.h>
#include <stdio.h>

__global__ void double_exponential_smoothing(float *values, float **projections, int num_values, int *periods, int num_periods) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < num_values) {
        for (int p = 0; p < num_periods; p++) {
            int period = periods[p];
            if (idx >= period) {
                float alpha = 2.0 / (period + 1);
                float beta = alpha / 2;
                float s1 = values[idx - period];
                float s2 = s1;
                for (int i = idx - period + 1; i <= idx; i++) {
                    s1 = alpha * values[i] + (1 - alpha) * s1;
                    s2 = beta * s1 + (1 - beta) * s2;
                }
                projections[p][idx] = 2 * s1 - s2;
            }
        }
    }
}

int main() {
    int num_values = 100; 
    float *values; 
    cudaMalloc(&values, num_values * sizeof(float));
    // Copia pra GPU

    int periods[] = {3, 4, 5, 6, 7, 12, 30};
    int num_periods = sizeof(periods) / sizeof(periods[0]);

    float **projections;
    projections = (float **)malloc(num_periods * sizeof(float *));
    for (int i = 0; i < num_periods; i++) {
        cudaMalloc(&projections[i], num_values * sizeof(float));
    }

    int *d_periods;
    cudaMalloc(&d_periods, num_periods * sizeof(int));
    cudaMemcpy(d_periods, periods, num_periods * sizeof(int), cudaMemcpyHostToDevice);

    int threadsPerBlock = 256;
    int blocksPerGrid = (num_values + threadsPerBlock - 1) / threadsPerBlock;

    double_exponential_smoothing<<<blocksPerGrid, threadsPerBlock>>>(values, projections, num_values, d_periods, num_periods);

    cudaFree(values);
    cudaFree(d_periods);
    for (int i = 0; i < num_periods; i++) {
        cudaFree(projections[i]);
    }
    free(projections);

    return 0;
}

