import h5py
import numpy as np
import scipy.sparse as sp

def build_sparse_matrix_with_hdf5(filename, n, batch_size=100000):

    f = h5py.File(filename, 'w')
    f.attrs['n'] = n
    f.create_dataset('data', (0,), maxshape=(None,), dtype=np.float64)
    f.create_dataset('indices', (0,), maxshape=(None,), dtype=np.int32)
    f.create_dataset('indptr', (n+1,), dtype=np.int32)
    
    rows, cols, data = [], [], []
    current_row = 0
    
    def save_batch():
        if not rows:
            return
        
        matrix = sp.csr_matrix((data, (rows, cols)), shape=(n, n))
        
        current_size = f['data'].shape[0]
        new_size = current_size + len(matrix.data)
        f['data'].resize((new_size,))
        f['data'][current_size:new_size] = matrix.data
        
        current_size = f['indices'].shape[0]
        new_size = current_size + len(matrix.indices)
        f['indices'].resize((new_size,))
        f['indices'][current_size:new_size] = matrix.indices
        
        f['indptr'][current_row+1:] = matrix.indptr[-1]
    
    def add_edge(i, j, val=1):
        rows.append(i)
        cols.append(j)
        data.append(val)
        
        # When batch_size reached, convert to CSR and save
        if len(rows) >= batch_size:
            save_batch()
            rows.clear()
            cols.clear()
            data.clear()

    def cleanup():
        save_batch() 
        f.close()    

    return add_edge, save_batch, cleanup, f


if __name__ == '__main__':
    
    n = 1000
    edges = [(np.random.randint(0, n), np.random.randint(0, n)) for _ in range(100)]
    
    add_edge_hdf5, save_batch_hdf5, cleanup_hdf5, f = build_sparse_matrix_with_hdf5('matrix.h5', n)

    for i, j in edges:
        add_edge_hdf5(i, j)

    cleanup_hdf5()