from math import sqrt, log10
from scipy.optimize import minimize_scalar
import numpy as np
import matplotlib.pyplot as plt


def laminar_func(reynolds):
    return 64 / reynolds


def turbulent_func(reynolds, relative_roughness):
    def _func(lambda_):
        return abs(1 / sqrt(lambda_) + 2 * log10(2.51 / (reynolds * sqrt(lambda_)) + 1 / 3.71 * relative_roughness))

    lambda_bounds = (0.01, 0.1)
    return minimize_scalar(_func, method='bounded', bounds=lambda_bounds).x


def moody_chart():
    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')

    fig, ax = plt.subplots()

    glatt_reynolds = np.logspace(log10(1500), log10(2.5e6), 100)
    glatt_lambda = np.vectorize(lambda x: turbulent_func(x, 0))(glatt_reynolds)

    ax.plot(glatt_reynolds, glatt_lambda, c='k')

    border_laminar_turbulent = 6400

    laminar_reynolds = np.arange(1e3, border_laminar_turbulent, 3)
    laminar_lambda = np.vectorize(laminar_func)(laminar_reynolds)

    ax.plot(laminar_reynolds, laminar_lambda, c='k')

    k_d_list = [0.001, 0.002, 0.005, 0.01, 0.02, 0.033]
    for k_d in k_d_list:
        rau_reynolds = np.logspace(log10(border_laminar_turbulent), 7, 100)
        rau_lambda = np.vectorize(lambda x: turbulent_func(x, k_d))(rau_reynolds)

        ax.plot(rau_reynolds, rau_lambda, c='k')

        ax.text(3e6, rau_lambda[-3] + 0.0005, r'$k/d={}$'.format(k_d),
                verticalalignment='bottom', horizontalalignment='left')

    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposy='clip')

    ax.grid(True)
    ax.grid(True, which='minor')

    ax.set_xlim(1e3, 1e7)
    ax.set_xticks([1e3, 1e4, 1e5, 1e6, 1e7])
    ax.set_xticks([], minor=True)

    ax.set_ylim(0.01, 0.1)
    ax.set_yticks([0.01, 0.02, 0.03, 0.05, 0.07, 0.1])
    ax.set_yticks([0.015, 0.04], minor=True)

    ax.set_yticklabels([0.01, 0.02, 0.03, 0.05, 0.07, 0.10])

    ax.set_yticklabels([], minor=True)

    ax.set_ylabel(r'$\longrightarrow \lambda$', fontsize='x-large')
    ax.set_xlabel(r'$\longrightarrow Re=\frac{v*d}{\nu}$', fontsize='x-large')

    ax.text(1.7e3, 0.02,
            'laminar \n' + r'$\lambda=\frac{64}{Re}$',
            bbox=dict(facecolor='white', alpha=0.9, linewidth=0), rotation=-70, verticalalignment='top')

    ax.text(6e5, 0.075, 'hydraulisch rau \n' + r'$\frac{1}{\sqrt{\lambda}}=1.14-2*\log_{10}\left(\frac{k}{d}\right)$',
            bbox=dict(facecolor='white', alpha=0.9, linewidth=0))

    ax.text(7e3, 0.028,
            'hydraulisch glatt \n' + r'$\frac{1}{\sqrt{\lambda}}=2*\log_{10}\left(Re*\sqrt{\lambda}\right)-0.8$',
            bbox=dict(facecolor='white', alpha=0.9, linewidth=0), rotation=-30, verticalalignment='top')

    ax.text(7e3, 0.075,
            'Übergangsbereich\n' + r'$\frac{1}{\sqrt{\lambda}}=-2*\log_{10}\left(\frac{2,51}{Re*\sqrt{\lambda}}+\frac{1}{3,71}*\frac{k}{d}\right)$',
            bbox=dict(facecolor='white', alpha=0.9, linewidth=0))

    fig.set_size_inches(7, 5)
    fig.tight_layout()
    return fig


if __name__ == '__main__':
    fig = moody_chart()
    fig.savefig('moody_chart.png')

