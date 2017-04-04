import nibabel as nib

def regress_subject(f, gradients, n_jobs = 1):
        """
        This function estimates coefficients of a linear model that fits gradients to individual volumes.
        It will fit all gradients to each volume.

        Inputs:
        f: volume time series (V x T)
        gradients: matrix containing gradients in columns (V x Ng)

        Outputs:
        Ng x T matrix with linear regression coefficients
        """

        from sklearn.linear_model import LinearRegression
        from scipy.stats.mstats import zscore

        # Load the data
        d = nib.load(f).get_data()

        # Z-score
        d_z = zscore(d, axis = 0)

        # Regress
        m = LinearRegression(fit_intercept=True, n_jobs = n_jobs)
        m.fit(d_z.T, gradients)

        return m.coef_.T


def trim_data(d, s = None):
    """
    This function removes entries from the first dimension of d that have zeros
    anywhere in the remaining dimensions.

    Additionally, it can remove respective items from a list (i.e. labels).

    Inputs:

    d : data array to clean
    s : subject list to remove data from

    Outputs:
    do : cleaned data array
    rem : removed entries
    so : cleaned vector
    """

    import numpy as np

    rem = np.unique(np.where(d == 0)[0])
    do = np.delete(d, rem, axis = 0)

    if s is not None:
        so = np.delete(s, rem, axis = 0)
        return do, rem, so
    else:
        return do, rem
