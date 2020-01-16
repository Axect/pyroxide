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