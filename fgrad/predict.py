# Features and targets from time series of modes

def features_targets(data, subjects, inds, condnames, labels, gradients = None, fixation = True):
    """
    This function takes in data and returns features and targets for classifier

    Inputs:
    data : mode data (s, t, m)
    inds : indices of timepoints
    gradients : indices of gradients to use

    Outputs:

    features : feature matrix
    targets : targets vector
    """

    import numpy as np

    conds = np.unique(inds)

    if fixation is False:
        conds = conds[1:]
        condnames = condnames[1:]

    N_conds = len(conds)
    N_subs = len(subjects)
    if gradients is None:
        N_modes = data.shape[2]
    else:
        N_modes = len(gradients)

    d = data[subjects,:,:]
    d = d[:,:,gradients]

    features = np.zeros((N_subs, N_conds, N_modes))
    targets = np.empty(N_conds * N_subs)

    for i, ind in enumerate(conds):
        features[:,i,:] = np.mean(d[:,inds == ind,0:N_modes], axis = 1)

    features = features.reshape((N_conds * N_subs, N_modes))

    target_labels = [labels[k] for k in condnames]
    targets = target_labels * N_subs

    return features, np.array(targets)
