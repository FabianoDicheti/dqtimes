#include <cuda_runtime.h>
#include <stdio.h>

__global__ void holt_winters_smoothing_kernel(float *values, float *projections, int num_values, int period, float *seasonals) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < num_values && idx >= 2 * period) {
        float alpha = 0.5;
        float beta = 0.5;
        float gamma = 0.5;
        float s = values[idx - 2 * period];
        float b = values[idx - 2 * period + 1] - values[idx - 2 * period];
        for (int i = 0; i < period; i++) {
            seasonals[i] = values[idx - 2 * period + i] - s;
        }
        for (int i = idx - 2 * period + period; i <= idx; i++) {
            float value = values[i];
            float last_s = s;
            float last_b = b;
            s = alpha * (value - seasonals[i % period]) + (1 - alpha) * (last_s + last_b);
            b = beta * (s - last_s) + (1 - beta) * last_b;
            seasonals[i % period] = gamma * (value - s) + (1 - gamma) * seasonals[i % period];
        }
        projections[idx] = s + b + seasonals[idx % period];
    }
}



extern "C" {
    void holt_winters_smoothing(float *values, float *projections, int num_values, int period) {
        float *d_values, *d_projections, *d_seasonals;
        cudaError_t err;

        err = cudaMalloc(&d_values, num_values * sizeof(float));
        if (err != cudaSuccess) {
            fprintf(stderr, "Failed to allocate device memory for values: %s\n", cudaGetErrorString(err));
            return;
        }

        err = cudaMemcpy(d_values, values, num_values * sizeof(float), cudaMemcpyHostToDevice);
        if (err != cudaSuccess) {
            fprintf(stderr, "Failed to copy values to device: %s\n", cudaGetErrorString(err));
            cudaFree(d_values);
            return;
        }

        err = cudaMalloc(&d_projections, num_values * sizeof(float));
        if (err != cudaSuccess) {
            fprintf(stderr, "Failed to allocate device memory for projections: %s\n", cudaGetErrorString(err));
            cudaFree(d_values);
            return;
        }

        err = cudaMalloc(&d_seasonals, period * sizeof(float));
        if (err != cudaSuccess) {
            fprintf(stderr, "Failed to allocate device memory for seasonals: %s\n", cudaGetErrorString(err));
            cudaFree(d_values);
            cudaFree(d_projections);
            return;
        }

        int threadsPerBlock = 256;
        int blocksPerGrid = (num_values + threadsPerBlock - 1) / threadsPerBlock;

        holt_winters_smoothing_kernel<<<blocksPerGrid, threadsPerBlock>>>(d_values, d_projections, num_values, period, d_seasonals);
        err = cudaGetLastError();
        if (err != cudaSuccess) {
            fprintf(stderr, "Failed to launch holt_winters_smoothing_kernel: %s\n", cudaGetErrorString(err));
            cudaFree(d_values);
            cudaFree(d_projections);
            cudaFree(d_seasonals);
            return;
        }
    err = cudaMemcpy(projections, d_projections, num_values * sizeof(float), cudaMemcpyDeviceToHost);
    if (err != cudaSuccess) {
        fprintf(stderr, "Failed to copy projections to host: %s\n", cudaGetErrorString(err));
        cudaFree(d_values);
        cudaFree(d_projections);
        cudaFree(d_seasonals);
        return;
    }

    cudaFree(d_values);
    cudaFree(d_projections);
    cudaFree(d_seasonals);
 }
}