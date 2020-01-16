from cffi import FFI
from ctypes import cdll

# Because of O3, we should include libopenblas.so
blas_ffi = FFI()
blas_ffi.dlopen("/opt/OpenBLAS/lib/libopenblas.so")

ffi = FFI()

ffi.cdef("""
    typedef struct {
        double *data;
        uint64_t row, col;
        bool by_row;
    } CMatrix;

    CMatrix cmatrix(double *ptr, uint64_t row, uint64_t col, bool by_row);
""")

# Include openblas
ffi.include(blas_ffi)

# Include pyroxide_rs
C = ffi.dlopen("pyroxide_rs/target/release/libpyroxide_rs.so")


# Make CMatrix
class PyMatrix:
    def __init__(self, data, row, col, by_row):
        cm = ffi.new("CMatrix *")
        cm.data = ffi.new("double []", data)
        cm.row = row
        cm.col = col
        cm.by_row = by_row
        self.cm = cm

pm = PyMatrix([1,2,3,4], 2, 2, True)
print(pm.cm.data)
for i in range(4):
    print(pm.cm.data[i])
