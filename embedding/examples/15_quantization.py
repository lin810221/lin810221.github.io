"""Per-vector symmetric scalar int8 quantization, with explicit scale."""
from embedding_core import dequantize_int8, quantize_int8

if __name__ == "__main__":
    original = [.1, .4, -1.2, 0.]
    codes, scale = quantize_int8(original)
    restored = dequantize_int8(codes, scale)
    print("int8 codes:", codes, "scale:", scale)
    print("restored:", restored)
    print("max absolute error:", max(abs(a - b) for a, b in zip(original, restored)))
