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
    CMatrix add(CMatrix *c1, CMatrix *c2);
""")

# Include openblas
ffi.include(blas_ffi)

# Include pyroxide_rs
C = ffi.dlopen("pyroxide_rs/target/release/libpyroxide_rs.so")


# Make CMatrix
class PyMatrix:
    def __init__(self, C, data, row, col, by_row):
        cm = ffi.new("CMatrix *")
        cm.data = ffi.new("double []", data)
        cm.row = row
        cm.col = col
        cm.by_row = by_row
        self.cm = cm

    def from_cmatrix(self, cm):
        self.cm = cm

    def __add__(self, other):
        cm1 = ffi.new("CMatrix *")
        cm2 = ffi.new("CMatrix *")
        cm1 = self.cm
        cm2 = other.cm
        C = ffi.dlopen("pyroxide_rs/target/release/libpyroxide_rs.so")
        cm = C.add(cm1, cm2)
        return PyMatrix.from_cmatrix(cm)

pm1 = PyMatrix([1,2,3,4], 2, 2, True)
pm2 = PyMatrix([1,2,3,4], 2, 2, False)
#new_pm = pm1 + pm2

#print(new_pm)

print(pm1)
