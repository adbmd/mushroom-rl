import numpy as np

from PyPi.approximators.regressor import Regressor


class ActionRegressor(object):
    """
    This class is used to approximate the Q-function with a different
    approximator of the provided class for each action. It is often used in MDPs
    with discrete actions and cannot be used in MDPs with continuous actions.
    """
    def __init__(self, approximator, action_space, **params):
        """
        Constructor.

        # Arguments
            approximator (object): the model class to approximate the
                Q-function of each action;
            action_space (object): action_space of the MDP;
            **params (dict): parameters dictionary to co each regressor.
        """
        self._action_space = action_space
        self.models = list()

        for i in xrange(self._action_space.n):
            self.models.append(Regressor(approximator, fit_action=False,
                                         **params))

    def fit(self, x, y, **fit_params):
        """
        Fit the model.

        # Arguments
            x (np.array): input dataset containing states and actions;
            y (np.array): target;
            fit_params (dict): other parameters.
        """
        for i in xrange(len(self.models)):
            action = self._action_space.values[i]
            idxs = np.argwhere((x[1] == action)[:, 0]).ravel()

            if idxs.size:
                self.models[i].fit(x[0][idxs, :], y[idxs], **fit_params)

    def train_on_batch(self, x, y, **fit_params):
        """
        Fit the model on a single batch.

        # Arguments
            x (np.array): input dataset containing states and actions;
            y (np.array): target;
            fit_params (dict): other parameters.
        """
        for i in xrange(len(self.models)):
            action = self._action_space.values[i]
            idxs = np.argwhere((x[1] == action)[:, 0]).ravel()

            if idxs.size:
                self.models[i].train_on_batch(x[0][idxs, :],
                                              y[idxs],
                                              **fit_params)

    def predict(self, x):
        """
        Predict.

        # Arguments
            x (np.array): input dataset containing states and actions.

        # Returns
            The predictions of the model.
        """
        y = np.zeros((x[0].shape[0]))
        for i in xrange(len(self.models)):
            action = self._action_space.values[i]
            idxs = np.argwhere((x[1] == action)[:, 0]).ravel()

            if idxs.size:
                y[idxs] = self.models[i].predict(x[0][idxs, :])

        return y

    def predict_all(self, x, actions):
        """
        Predict Q-value for each action given a state.

        # Arguments
            x (np.array): input dataset containing states;
            actions (np.array): list of actions of the MDP.

        # Returns
            The predictions of the model.
        """
        n_states = x.shape[0]
        n_actions = actions.shape[0]
        y = np.zeros((n_states, n_actions))

        for action in xrange(n_actions):
            y[:, action] = self.models[action].predict(x)

        return y

    def __str__(self):
        return str(self.models[0]) + ' with action regression.'
