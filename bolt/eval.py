"""
The :mod:`eval` module contains various routines for model evaluation.

Metrics
???????

The following evaluation metrics are currently supported:

  :func:`errorrate`: the error rate of the binary classifier.
  
  :func:`rmse`: the root mean squared error of a regressor.
  
  :func:`cost`: the cost of a model w.r.t. a given loss function.

"""
from __future__ import division

from itertools import izip

import numpy as np
import bolt

def errorrate(model,ds):
    """Compute the misclassification rate of the model.
    Assumes that labels are coded as 1 or -1. 

    zero/one loss: if p*y > 0 then 0 else 1

    Args:
      model: A `LinearModel`.
      ds: A `Dataset`.

    Returns:
      `(100.0 / n) * sum( p*y > 0 ? 0 : 1 for p,y in ds)`.
    """
    n = 0
    err = 0
    for p,y in izip(model.predict(ds.iterinstances()),ds.iterlabels()):
        z = p*y
        if np.isinf(p) or np.isnan(p) or z <= 0:
            err += 1
        n += 1
    errrate = err / n
    return errrate * 100.0

def rmse(model,ds):
    """Compute the root mean squared error of the model.

    Args:
      model: A `LinearModel`.
      ds: A `Dataset`.

    Returns:
      `sum([(model(x)-y)**2.0 for x,y in ds])`.
    """
    n = 0
    err = 0
    for p,y in izip(model.predict(ds.iterinstances()),ds.iterlabels()):
        err += (p-y)**2.0
        n += 1
    err /= n
    return np.sqrt(err)

def cost(model,ds, loss):
    """The cost of the loss function.

    Args:
      model: A `LinearModel`.     
      ds: A `Dataset`.
      
    Returns:
      `sum([loss.(model(x),y) for x,y in ds])`
    """
    cost = 0
    for p,y in izip(model.predict(ds.iterinstances()),ds.iterlabels()):
        cost += loss.loss(p,y)
    return cost

def error(model, ds, loss):
    """Report the error of the model on the
    test examples. If the loss function of the model
    is

    Args:
      model: A `LinearModel`.   
      ds: A `Dataset`.

    Returns:
      Either `errorrate` or `rmse`; depending on the `loss` function.
    """
    err = 0.0
    if isinstance(loss,bolt.Classification):
        err = errorrate(model,ds)
    elif isinstance(loss,bolt.Regression):
        err = rmse(model,ds)
    else:
        raise ValueError, "lm.loss: either Regression or Classification loss expected"
    return err
