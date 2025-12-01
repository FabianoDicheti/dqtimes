#include <cuda_runtime.h>
#include <stdio.h>
#include <math.h>

__global__ void interpolation_kernel(float *indices, float *valores, float *result_multivariate, float *result_gaussian, float *result_polynomial, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n - 1) {
        float x = indices[idx];
        float x1 = indices[idx];
        float x2 = indices[idx + 1];
        float y1 = valores[idx];
        float y2 = valores[idx + 1];

        result_multivariate[idx] = (y1 + (x - x1) * (y2 - y1) / (x2 - x1));
        result_gaussian[idx] = (y1 * exp(-0.5 * pow((x - x1) / 1.0, 2)) / (1.0 * sqrt(2 * M_PI)) + y2 * exp(-0.5 * pow((x - x2) / 1.0, 2)) / (1.0 * sqrt(2 * M_PI)));
        result_polynomial[idx] = (y1 + (y2 - y1) * (x - x1) / (x2 - x1));
    }
}

extern "C" {
    void run_interpolation_kernel(float *indices, float *valores, float *result_multivariate, float *result_gaussian, float *result_polynomial, int n) {
        float *d_indices, *d_valores, *d_result_multivariate, *d_result_gaussian, *d_result_polynomial;

        cudaMalloc(&d_indices, n * sizeof(float));
        cudaMalloc(&d_valores, n * sizeof(float));
        cudaMalloc(&d_result_multivariate, n * sizeof(float));
        cudaMalloc(&d_result_gaussian, n * sizeof(float));
        cudaMalloc(&d_result_polynomial, n * sizeof(float));

        cudaMemcpy(d_indices, indices, n * sizeof(float), cudaMemcpyHostToDevice);
        cudaMemcpy(d_valores, valores, n * sizeof(float), cudaMemcpyHostToDevice);

        int blockSize = 256;
        int numBlocks = (n + blockSize - 1) / blockSize;
        interpolation_kernel<<<numBlocks, blockSize>>>(d_indices, d_valores, d_result_multivariate, d_result_gaussian, d_result_polynomial, n);

        cudaMemcpy(result_multivariate, d_result_multivariate, n * sizeof(float), cudaMemcpyDeviceToHost);
        cudaMemcpy(result_gaussian, d_result_gaussian, n * sizeof(float), cudaMemcpyDeviceToHost);
        cudaMemcpy(result_polynomial, d_result_polynomial, n * sizeof(float), cudaMemcpyDeviceToHost);

        cudaFree(d_indices);
        cudaFree(d_valores);
        cudaFree(d_result_multivariate);
        cudaFree(d_result_gaussian);
        cudaFree(d_result_polynomial);
    }
}
