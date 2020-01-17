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
    def __init__(self, data, row, col, by_row):
        self.data = data
        self.row = row
        self.col = col
        self.by_row = by_row

    @classmethod
    def from_cmatrix(cls, cm):
        return cls([cm.data[i] for i in range(cm.row * cm.col)], cm.row, cm.col, cm.by_row)

    def to_cmatrix(self):
        data = ffi.new("double []", self.data)
        cm = C.cmatrix(data, self.row, self.col, self.by_row)
        return cm

    def __add__(self, other):
        cm1 = C.cmatrix(ffi.new("double []", self.data), self.row, self.col, self.by_row)
        cm2 = other.to_cmatrix()
        print([cm1.data[i] for i in range(4)])
        cm = C.add(cm1, cm2)
        return PyMatrix.from_cmatrix(cm)

pm1 = PyMatrix([1,2,3,4], 2, 2, True)
pm2 = PyMatrix([1,2,3,4], 2, 2, False)

print(pm1.data)
print(pm2.data)

new_pm = pm1 + pm2
print(new_pm.data)
