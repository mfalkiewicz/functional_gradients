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

        d = nib.load(f).get_data()

        T = d.shape[1]
        Ng = gradients.shape[0]

        m = linear_model.LinearRegression(fit_intercept=True, n_jobs = n_jobs)
        m.fit(d.T, gradients)

        return m.coef_


def trim_data(d, s = None):
    """
    This function simply takes an array and removes all entries with empty rows.
    Additionally, it can remove respective items from a list (i.e. labels).

    Inputs:

    d : data array to clean
    s : subject list to remove data from
    """

    rem = np.where(np.sum(np.sum(d, axis = 1),axis = 1) == 0)[0]
    do = np.delete(dr, rem, axis = 0)

    if s is not None:
        so = np.delete(s, rem, axis = 0)
        return do, so
    else:
        return do
