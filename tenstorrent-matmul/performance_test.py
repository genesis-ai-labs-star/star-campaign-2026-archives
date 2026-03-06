import time
import numpy as np

def benchmark_matmul(size):
    print(f"Starting Matmul benchmark for size {size}x{size}...")
    A = np.random.rand(size, size).astype(np.float32)
    B = np.random.rand(size, size).astype(np.float32)
    
    start_time = time.time()
    C = np.dot(A, B)
    end_time = time.time()
    
    duration = end_time - start_time
    gflops = (2 * size**3) / (duration * 1e9)
    print(f"Duration: {duration:.4f}s, GFLOPS: {gflops:.2f}")
    return duration, gflops

if __name__ == "__main__":
    # 模拟不同负载下的性能表现
    sizes = [1024, 2048, 4096]
    for s in sizes:
        benchmark_matmul(s)
