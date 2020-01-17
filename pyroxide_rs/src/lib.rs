extern crate peroxide;
extern crate c_vec;
use peroxide::*;
use c_vec::CVec;
use std::os::raw::c_double;

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

        let temp = self.clone();

        unsafe {
            let m = Matrix {
                data: CVec::new(temp.data, len).into(),
                row: self.row,
                col: self.col,
                shape: if self.by_row { Row } else { Col }
            };
            println!("to matrix");
            m.print();
            std::mem::forget(temp);
            m
        }
    }

    pub fn from_matrix(m: &Matrix) -> Self {
        m.print();
        let cvec = unsafe {
            CVec::new(m.data.clone().as_mut_ptr(), m.row * m.col)
        };
        unsafe {
            Self {
                data: cvec.into_inner(),
                row: m.row,
                col: m.col,
                by_row: match m.shape { Row => true, Col => false }
            }
        }
    }
}

#[no_mangle]
pub extern "C" fn cmatrix(ptr: *mut c_double, row: usize, col: usize, by_row: bool) -> CMatrix {
    unsafe {
        CMatrix {
            data: CVec::new(ptr, row * col).into_inner(),
            row,
            col,
            by_row
        }
    }
}

#[no_mangle]
pub extern "C" fn add(c1: &CMatrix, c2: &CMatrix) -> CMatrix {
    println!("Add");
    let m = c1.to_matrix() + c2.to_matrix();
    println!("from matrix from add");
    CMatrix::from_matrix(&m)
}