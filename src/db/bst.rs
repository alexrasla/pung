use std::cmp;
use std::collections::VecDeque;

pub trait BSTOrder {
    fn as_bst_order(&mut self);
}

impl<T: Clone> BSTOrder for Vec<T> {
    // Takes a sorted array of elements and produces an array that corresponds
    // to the compact representation (no pointers) of a complete Binary search tree.
    fn as_bst_order(&mut self) {
        if self.len() == 0 {
            return;
        }
        let mut q = VecDeque::new();
        let mut copy: Vec<T> = Vec::with_capacity(self.len());

        q.push_back((0 as usize, self.len() - 1));
        // println!("as bst order {:?} {}", q, self.len());
        while !q.is_empty() {
            // println!("as bst order3");
            let (start, end) = q.pop_front().unwrap();
            let len = (end - start) + 1;
            // println!("len {}", len);
            if len <= 0 {
                continue;
            }

            let idx = start + find_idx(len as u32) as usize;
            // println!("as bst order4 {} {}", len, idx);
            copy.push(self[idx].clone());
            
            if idx > start {
                q.push_back((start, idx - 1));
            }

            if end > idx && idx + 1 < self.len() {
                q.push_back((idx + 1, end));
            }
        }
        // println!("as bst order5");
        *self = copy;
    }
}


fn find_idx(n: u32) -> u32 {
    if n == 1 {
        return 0;
    }

    let h = ((n + 1) as f32).log2().ceil() as u32; // height of tree
    let m_n = 2u32.pow(h) - 1; // # nodes if tree were full (>= n)

    let f_h = ((n + 1) as f32).log2().floor() as u32; // height of full portion (h or h-1)
    let f_n = 2u32.pow(f_h) - 1; // # nodes of full portion (<= n)

    (f_n / 2) + cmp::min(n - f_n, (m_n - f_n) / 2)
}
