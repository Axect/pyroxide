extern crate peroxide;
use peroxide::*;
use std::os::raw::{c_double};

#[repr(C)]
#[derive(Debug, Clone)]
pub struct CMatrix {
    pub data: *mut c_double,
    pub row: usize,
    pub col: usize,
    pub by_row: bool,
}

#[no_mangle]
impl CMatrix {
    pub fn to_matrix(&self) -> Matrix {
        let len = self.row * self.col;
        let cap = len;
        unsafe {
            Matrix {
                data: Vec::from_raw_parts(self.data, len, cap),
                row: self.row,
                col: self.col,
                shape: if self.by_row { Row } else { Col }
            }
        }
    }

    pub fn from_matrix(m: &Matrix) -> Self {
        let data = m.data.clone().as_mut_ptr();
        Self {
            data,
            row: m.row,
            col: m.col,
            by_row: match m.shape { Row => true, Col => false }
        }
    }
}

#[no_mangle]
pub extern "C" fn cmatrix(ptr: *mut c_double, row: usize, col: usize, by_row: bool) -> CMatrix {
    CMatrix {
        data: ptr,
        row,
        col,
        by_row
    }
}

#[no_mangle]
pub extern "C" fn add(c1: *const CMatrix, c2: *const CMatrix) -> CMatrix {
    let m = unsafe {
        (*c1).to_matrix() + (*c2).to_matrix()
    };
    CMatrix::from_matrix(&m)
}