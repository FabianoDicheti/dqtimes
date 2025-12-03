#include <cuda_runtime.h>
#include <stdio.h>

__global__ void moving_average_kernel(float *values, float *averages, int num_values, int period) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < num_values) {
        float sum = 0.0;
        int count = 0;
        for (int i = idx; i < idx + period && i < num_values; i++) {
            sum += values[i];
            count++;
        }
        if (count > 0) {
            averages[idx] = sum / count;
        }
    }
}

extern "C" {
    void moving_average(float *values, float *averages, int num_values, int period) {
        float *d_values, *d_averages;
        cudaError_t err;

        err = cudaMalloc(&d_values, num_values * sizeof(float));
        if (err != cudaSuccess) {
            printf("Erro ao alocar memória na GPU para valores: %s\n", cudaGetErrorString(err));
            return;
        }

        err = cudaMemcpy(d_values, values, num_values * sizeof(float), cudaMemcpyHostToDevice);
        if (err != cudaSuccess) {
            printf("Erro ao copiar valores para a GPU: %s\n", cudaGetErrorString(err));
            return;
        }

        err = cudaMalloc(&d_averages, num_values * sizeof(float));
        if (err != cudaSuccess) {
            printf("Erro ao alocar memória na GPU para médias: %s\n", cudaGetErrorString(err));
            return;
        }

        int threadsPerBlock = 256;
        int blocksPerGrid = (num_values + threadsPerBlock - 1) / threadsPerBlock;

        printf("Executando o kernel com %d blocos de %d threads cada\n", blocksPerGrid, threadsPerBlock);
        moving_average_kernel<<<blocksPerGrid, threadsPerBlock>>>(d_values, d_averages, num_values, period);
        err = cudaGetLastError();
        if (err != cudaSuccess) {
            printf("Erro ao executar o kernel: %s\n", cudaGetErrorString(err));
            return;
        }

        err = cudaMemcpy(averages, d_averages, num_values * sizeof(float), cudaMemcpyDeviceToHost);
        if (err != cudaSuccess) {
            printf("Erro ao copiar médias de volta para o host: %s\n", cudaGetErrorString(err));
            return;
        }

        cudaFree(d_values);
        cudaFree(d_averages);
    }
}
