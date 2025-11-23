# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* compilar c++ para usar no python: 
c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) seu_arquivo.cpp -o nome_do_modulo$(python3-config --extension-suffix)
para importar no python apenas chamar: 'import nome_do_modulo'

para compilar cuda e usar no python:
nvcc -arch=sm_75 -o sumArrayGPU.so -shared -Xcompiler -fPIC sumArrayGPU.cu
* nesse caso seguir este exemplo de uso no script:

# Python function calling the compiled C++/CUDA function

import ctypes
import pycuda.gpuarray as gpuarray
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import pycuda.autoinit

import numpy as np

# Load the CUDA library
cuda_lib = ctypes.CDLL('./sumArrayGPU.so')  # Update with the correct path

# Define the function prototype
cuda_lib.my_cuda_function.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
cuda_lib.my_cuda_function.restype = None

# Prepare data
input_data = np.array([3, 1, 33, -4]).astype(np.int32)
output_data = np.array([0, 0, 0, 0]).astype(np.int32)
size = len(input_data)

# Use PyCUDA to allocate GPU memory
input_gpu   = gpuarray.to_gpu(input_data)
output_gpu  = gpuarray.to_gpu(output_data)

# Call the CUDA function
cuda_lib.my_cuda_function(ctypes.cast(input_gpu.ptr, ctypes.POINTER(ctypes.c_int)), ctypes.cast(output_gpu.ptr, ctypes.POINTER(ctypes.c_int)), size)

print(input_gpu)
print(output_gpu)