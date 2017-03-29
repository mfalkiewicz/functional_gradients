from __future__ import print

def preprocess_dense_connectome(dc):
    """
    Preprocesses the dense connectome to be feasible for diffusion map embedding.

    Warning: 32k dense connectome requires ~130 GB RAM for this step.
    """

    from __future__ import print
    import nibabel as nib
    import numpy as np
    from sklearn.metrics import pairwise_distances

    try:
        dcon = nib.load(dc).get_data()
    except:
        print('Could not load the dense connectome.')
        raise

    # First transform the dense connectome back to Pearson correlation
    dcon = np.tanh(dcon)

    # Since the tanh does not get the diagonal perfectly, we fix it manually
    np.fill_diagonal(dcon,1)

    # Get the 90th percentile for each row and set everything below to zero
    perc = np.array([np.percentile(x, 90) for x in dcon])
    for i in range(dcon.shape[0]):
        dcon[i, dcon[i,:] < perc[i]] = 0

    # See if there are any negative values left
    neg_values = np.array([sum(dcon[i,:] < 0) for i in range(N)])
    print "Negative values occur in %d rows" % sum(neg_values > 0)

    # There should be very few of them, so we set them to 0 as well
    dcon[dcon < 0] = 0

    # We use cosine similarity to express the affinity between the rows
    aff = 1 - pairwise_distances(dcon, metric = 'cosine')
    
    del dcon

    return aff

def embed_dense_connectome(aff):
    """
    This function takes the affinity matrix and returns the low-dimensional
    embedding.
    """

    from mapalign import embed

    # Embedding using mapalign
    emb, res = embed.compute_diffusion_map(aff, alpha = 0.5, n_components = 300)
    
    # Divide each non-trivial eigenvector by the first one and remove the latter
    X = res['vectors']
    X = (X.T/X[:,0]).T[:,1:]

    return X

def save_embedding(X, target = 'rsFC_eigenvectors.dscalar.nii', temp = None):
    """
    Saves the low-dimensional embedding as a CIFTI file. Requires wb_command.
    
    X: the low-dimensional embedding
    target: file name with path (.dscalar.nii')
    temp: temporaty file directory, current directory by default
    """

    import subprocess
    import os

    if temp is None:
        temp = os.path.abspath(os.path.curdir)
        #temp = os.path.dirname(os.path.abspath(target))

    np.savetxt('%s/embedded_components.txt' % temp, X)

    labels = np.array(["Dimension %d" % (i+1) for i in range(X.shape[1])])
    np.savetxt('%s/component_labels.txt' % temp, labels, fmt = "%s")

    subprocess.call(['wb_command','-cifti-create-scalar-series %s/embedded_components.txt %s -name-file %s/component_labels.txt -series SECOND 1 1' % (temp, target, temp)])
