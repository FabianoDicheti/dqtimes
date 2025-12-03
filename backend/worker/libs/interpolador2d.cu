#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>

// Função para interpolação gaussiana em 2D
__device__ float gaussian_interpolation_2d(float x, float y, float x1, float y1, float x2, float y2, float f11, float f21, float f12, float f22) {
    float sigma = 1.0; 
    float gauss_x1 = exp(-0.5 * pow((x - x1) / sigma, 2)) / (sigma * sqrt(2 * M_PI));
    float gauss_x2 = exp(-0.5 * pow((x - x2) / sigma, 2)) / (sigma * sqrt(2 * M_PI));
    float gauss_y1 = exp(-0.5 * pow((y - y1) / sigma, 2)) / (sigma * sqrt(2 * M_PI));
    float gauss_y2 = exp(-0.5 * pow((y - y2) / sigma, 2)) / (sigma * sqrt(2 * M_PI));

    return f11 * gauss_x1 * gauss_y1 + f21 * gauss_x2 * gauss_y1 + f12 * gauss_x1 * gauss_y2 + f22 * gauss_x2 * gauss_y2;
}

// Kernel CUDA para realizar a interpolação gaussiana em 2D
__global__ void gaussian_interpolation_2d_kernel(float *input, float *output, int rows, int cols) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < rows && col < cols && input[row * cols + col] == -1) { // Supondo que -1 represente uma string
        // Encontre os quatro pontos mais próximos para interpolação
        int x1 = max(0, col - 1);
        int x2 = min(cols - 1, col + 1);
        int y1 = max(0, row - 1);
        int y2 = min(rows - 1, row + 1);

        float f11 = input[y1 * cols + x1];
        float f21 = input[y1 * cols + x2];
        float f12 = input[y2 * cols + x1];
        float f22 = input[y2 * cols + x2];

        output[row * cols + col] = gaussian_interpolation_2d(col, row, x1, y1, x2, y2, f11, f21, f12, f22);
    } else if (row < rows && col < cols) {
        output[row * cols + col] = input[row * cols + col];
    }
}

void interpolate_2d(float *input, float *output, int rows, int cols) {
    float *d_input, *d_output;

    cudaMalloc(&d_input, rows * cols * sizeof(float));
    cudaMalloc(&d_output, rows * cols * sizeof(float));

    cudaMemcpy(d_input, input, rows * cols * sizeof(float), cudaMemcpyHostToDevice);

    dim3 blockSize(16, 16);
    dim3 numBlocks((cols + blockSize.x - 1) / blockSize.x, (rows + blockSize.y - 1) / blockSize.y);
    gaussian_interpolation_2d_kernel<<<numBlocks, blockSize>>>(d_input, d_output, rows, cols);

    cudaMemcpy(output, d_output, rows * cols * sizeof(float), cudaMemcpyDeviceToHost);

    cudaFree(d_input);
    cudaFree(d_output);
}

int main() {
    // Exemplo
    int rows = 5;
    int cols = 5;
    float input[] = {
        0, 1, 2, 3, -1,
        2, 4, 5, 8, 2,
        -1, -1, 2, 1, 1,
        2, 2, 3, 5, 8,
        -1, -1, -1, -1, -1
    };
    float output[rows * cols];

    interpolate_2d(input, output, rows, cols);

    printf("Interpolated Matrix:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%f ", output[i * cols + j]);
        }
        printf("\n");
    }

    return 0;
}

