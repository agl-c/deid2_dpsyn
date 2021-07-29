import numpy as np
from sklearn.isotonic import IsotonicRegression


def laplace(beta, data):
    np.random.seed(86175)
    return (data + np.random.laplace(0, beta, size=data.shape))


def lap_postprocess(beta, data):
    output = data + np.random.laplace(0, beta, size=data.shape)
    output = np.clip(output, a_min=0, a_max=np.inf)
    return output.round().astype(np.int)


def geometric(scale, data):
    """
    Output:
        The result of the geometric mechanism (x-y + true_answer).
    numpy.random.geometric draws from p.d.f. f(k) = (1 - p)^{k - 1} p   (k=1,2,3...)
                                                    p          -│k│
    The difference of two draws has the p.d.f    ──────── (1 - p)
                                                  2 - p
    """
    # Parameter p of the Geometric distribution as per class docstring
    p = 1 - np.exp(-1 / scale)

    x = np.random.geometric(p, size=data.shape) - 1  # numpy geometrics start with 1
    y = np.random.geometric(p, size=data.shape) - 1

    output = x - y + data
    return output
    # return iso(output)


# If the true values are originally sorted, this will make the noisy estimate sorted
# This does not enforce the estimates to be integers
def iso_direct(hist):
    iso_reg = IsotonicRegression(y_min=0).fit(range(len(hist)), hist)
    return iso_reg.predict(range(len(hist)))


# If the true values are not sorted, this will first accumulate (convert pdf to cdf)
# and then run the Isotonic regression, and finally convert the results back (cdf to pdf)
# The intuition is that this removes negative estimates
# It does not enforce the results to be integers
def iso(hist):
    shape = hist.shape
    flatten_hist = hist.flatten()
    flatten_hist = np.cumsum(flatten_hist)

    init_zeros = np.zeros(2 * len(flatten_hist))
    padded_flatten_hist = np.concatenate([init_zeros, flatten_hist])
    iso_reg = IsotonicRegression(y_min=0).fit(range(len(padded_flatten_hist)), padded_flatten_hist)
    hist_cdf = iso_reg.predict(range(len(init_zeros), len(padded_flatten_hist)))

    noisy_pdf = np.zeros_like(hist_cdf)
    noisy_pdf[0] = hist_cdf[0]
    noisy_pdf[1:] = hist_cdf[1:] - hist_cdf[:-1]
    return noisy_pdf.reshape(shape)


def svt(q_ans, eps, eps1_ratio=0, sensitivity=1, monotonic=True):
    svt_const = 1 if monotonic else 2 ** (2 / 3)
    eps1 = eps / (1 + svt_const)
    eps2 = svt_const * eps / (1 + svt_const)

    if eps1_ratio > 0:
        eps1 = eps * eps1_ratio
        eps2 = eps * (1 - eps1_ratio)

    beta1 = sensitivity / eps1
    beta2 = sensitivity / eps2 if monotonic else 2 * sensitivity / eps2

    noise_0 = laplace(beta1, [0])[0]
    noise_ans = laplace(beta2, q_ans)
    return np.argmax(noise_ans > noise_0)


def em(q_ans, eps, sensitivity=1, monotonic=True):
    coeff = eps / sensitivity if monotonic else eps / 2 / sensitivity
    probs = np.exp(coeff * q_ans)
    probs = probs / sum(probs) if sum(probs) > 0 else [1] * len(probs)
    probs = np.cumsum(probs)

    rand_p = np.random.rand()
    return np.searchsorted(probs, rand_p, side='left')

# noise max 
def nm(q_ans, eps, sensitivity=1, monotonic=True):
    coeff = eps / sensitivity if monotonic else eps / 2 / sensitivity
    noisy_ans = laplace(1 / coeff, q_ans)
    return np.argmax(noisy_ans)
