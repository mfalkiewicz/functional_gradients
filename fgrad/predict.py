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

def predict_performance(f_A, t_A, f_B, t_B, f_C, t_C, gradients = [0,1,2]):

    """
    Build a linear model on each of f_ datasets and test it on remaining datasets.
    For each train/test combination, test all combinations of features.
    """

    import itertools
    from sklearn.metrics import explained_variance_score
    from sklearn.preprocessing import StandardScaler
    import statsmodels.api as sm

    scaler = StandardScaler()

    train_labels = ['A', 'B', 'C']
    train_features = [f_A, f_B, f_C]
    train_targets = [t_A, t_B, t_C]

    test_features = [[f_B, f_C], [f_A, f_C], [f_A, f_B]]
    test_targets = [[t_B, t_C], [t_A, t_C], [t_A, t_B]]

    # Produce all combinations of features. Will assume that the features are without the constant term.
    gradients = range(f_A.shape[1])
    combs = []

    for L in range(0, len(gradients)+1):
        for subset in itertools.combinations(gradients, L):
            combs.append(list(subset))

    combs = combs[1:]

    print "Gradients   AIC   BIC   A (B, C)              AIC   BIC   B (A, C)              AIC   BIC   C (A, B)"
    print "============================================================================================================="
    for c in combs:
        perf = []
        aic = []
        bic = []
        for i, tr_g in enumerate(train_features):
            scaler.fit(tr_g)
            tr_g = scaler.transform(tr_g)
            ols = sm.OLS(train_targets[i], sm.add_constant(tr_g[:,c]))
            ols = ols.fit(cov_type="HC1")
            perf.append(explained_variance_score(train_targets[i], ols.predict(sm.add_constant(tr_g[:,c]))))
            aic.append(ols.aic)
            bic.append(ols.bic)
            for j, te_g in enumerate(test_features[i]):
                te_g = scaler.transform(te_g)
                perf.append(explained_variance_score(test_targets[i][j], ols.predict(sm.add_constant(te_g[:,c]))))
        print "%-10s  %.1f %.1f %.2f (%.2f, %.2f)     %.1f %.1f %.2f (%.2f, %.2f)     %.1f %.1f %.2f (%.2f, %.2f)" % (c, aic[0], bic[0], perf[0], perf[1], perf[2],
                                                                                    aic[1], bic[1], perf[3], perf[4], perf[5],
                                                                                    aic[2], bic[2], perf[6], perf[7], perf[8])
