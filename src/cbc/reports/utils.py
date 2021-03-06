''' Collection of plotting utils. '''
from . import contract, np
from ..tools import create_histogram_2d
from cbc.demos.simplified_source import correlation_coefficient
from reprep.plot_utils import set_spines_look_A


fsize = 1.57
figsize_points = (fsize * 2, fsize)


#@contract(S='array[2xN]')
def util_plot_euclidean_coords2d(report, f, nid, S, caption=None):
    print('util_plot_euclidean_coords2d(%s)' % nid)

    with report.plot(nid, figsize=(fsize, fsize), caption=caption) as pylab:
        set_spines_look_A(pylab)
        # do not rasterize, they are small
        pylab.plot(S[0, :], S[1, :], 'ks', markersize=0.5)
        #M = np.abs(S).max()
        M = 1.1
        #pylab.axis('equal')
        pylab.axis([-M, +M, -M, +M])

    report.last().add_to(f)


plot_and_display_coords = util_plot_euclidean_coords2d


def util_plot_xy_generic(r, f, nid, x, y, xlabel, ylabel, caption):
    print('util_plot_xy_generic(%s)' % nid)
    with r.plot(nid) as pylab:
        pylab.plot(x, y, 'b.', markersize=0.2, rasterized=True)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
    r.last().add_to(f, caption)


@contract(S='directions', returns='array[2xK]')
def azi_elev_from_directions(S):
    N = S.shape[1]
    Z = np.zeros((2, N))
    Z[0, :] = np.arctan2(S[1, :], S[0, :])
    Z[1, :] = np.arccos(S[2, :]) - np.pi / 2
    return Z


def add_textdegree(val):
    def add_it(x):
        if x != '':
            return x + '$^\\circ$'
        else:
            return ''
    return map(add_it, val)


def set_xticks_from_seq(pylab, t):
    pos = [a for a, _ in t]
    val = [b for _, b in t]
    val = add_textdegree(val)
    pylab.xticks(pos, val)


def set_yticks_from_seq(pylab, t):
    pos = [a for a, _ in t]
    val = [b for _, b in t]
    val = add_textdegree(val)
    pylab.yticks(pos, val)


@contract(S='directions,array[3xN]')
def util_plot_3D_points(report, f, nid, S, caption=None):
    print('util_plot_3D_points(%s)' % nid)
    # let (1,0,0) be (0,0,1)
    S1 = np.empty_like(S)
    S1[0, :] = S[2, :]
    S1[1, :] = S[1, :]
    S1[2, :] = S[0, :]

    if np.mean(S1[0, :]) < 0:
        S1[0, :] *= -1

    # switch Y and Z if necessary
    if np.mean(np.abs(S1[1, :])) < np.mean(np.abs(S1[2, :])):
        S2 = np.empty_like(S1)
        S2[0, :] = S1[0, :]
        S2[1, :] = S1[2, :]
        S2[2, :] = S1[1, :]
        S1 = S2

    AE = azi_elev_from_directions(S1)

    A = AE[0, :]
    E = AE[1, :]
    A_deg = np.rad2deg(A)
    E_deg = np.rad2deg(E)
    with report.plot(nid, figsize=figsize_points) as pylab:
        set_spines_look_A(pylab)

        pylab.plot(A_deg, E_deg, 'bs', markersize=0.2)

        max_azi_deg = np.max(A_deg)
        max_ele_deg = np.max(E_deg)
        #print('max_azi_deg', max_azi_deg)
        #print('max_ele', np.max(E_deg))
        if max_azi_deg < 60: # mino
            #print('config mino')
            set_xticks_from_seq(pylab,
                                [#(-45, '-45'), 
                                 (-30, '-30'), (-15, ''), (0, '0'),
                                 (+15, ''), (30, '30'),
                                 #(45, '+45')
                                 ]
                                )
            MA = 30
        elif max_azi_deg < 90: # GOPRO
            #print('config gopro')
            set_xticks_from_seq(pylab,
                                [(-90, '-90'), (-75, ''), (-60, ''),
                                 (-45, '-45'),
                                 (-30, ''),
                                 (-15, ''), (0, '0'),
                                 (+15, ''), (30, ''), (45, '45'), (60, ''),
                                 (75, ''), (90, '+90')])
            MA = 95

        else: # omni
            #print('config omni')
            set_xticks_from_seq(pylab,
                                [(-180, '-180'), (-135, ''), (-90, '-90'),
                                 (-45, ''), (0, '0'),
                                 (+45, ''), (90, '+90'), (135, ''),
                                 (180, '+180')])
            MA = 180

        if max_ele_deg < 15:
            ME = 15
            set_yticks_from_seq(pylab,
            [(-15, '-15'), (-10, ''), (-5, ''), (0, '0'),
             (5, ''), (10, ''), (+15, '15')])
        elif max_ele_deg < 55:
            ME = 55
            set_yticks_from_seq(pylab,
            [(-45, '-45'), (-30, ''), (-15, ''), (0, '0'), (15, ''), (30, ''),
             (+45, '45')])

        else:
            ME = 90

            set_yticks_from_seq(pylab,
                [(-90, '-90'), (-45, '-45'), (0, '0'),
                 (+45, '+45'), (+90, '+90')])

        pylab.axis([-MA, MA, -ME, ME])
        pylab.ylabel('elevation')
        pylab.xlabel('azimuth')

        if False:
            pylab.gca().xaxis.set_label_coords(0.5, -0.02)
            pylab.gca().yaxis.set_label_coords(-0.02, 0.5)

    report.last().add_to(f, caption)


def get_plot_params(nsamples):
    if nsamples < 10000:
        return dict(markersize=0.5, alpha=0.2, rasterized=False)
    else:
        return dict(markersize=1, alpha=0.01, rasterized=True)
        #return dict(markersize=0.4, alpha=0.05, rasterized=True)


def add_distance_vs_sim_figure(report, nid, figure, caption,
                                D, R, xlabel, ylabel, degrees=False):
    print('add_distance_vs_sim_figure(%s)' % nid)

    D = np.array(D.flat)
    R = np.array(R.flat)

    with report.plot(nid, figsize=(fsize, fsize)) as pylab:
        set_spines_look_A(pylab)

        plot_params = get_plot_params(nsamples=D.size)
        print(' using plot params: %s' % plot_params)
        pylab.plot(D, R, 'bs', **plot_params)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.axis([D.min(), D.max(), R.min(), R.max()])
        m = D.max()

        def set_ticks(t, M):
            pos = [a for a, _ in t]
            val = [b for _, b in t]
            if degrees:
                val = add_textdegree(val)
            pylab.xticks(np.deg2rad(pos), val)
            pylab.axis([0, np.deg2rad(M), -0.3, +1])

        # TODO: euclidean geometry
        if m < np.pi / 4:
            set_ticks([(0, '0'),
                     (10, '10'),
                     (20, '20'),
                     (30, '30'),
                     (40, '40'),
                      (50, '50')], 50)
        elif m < np.pi / 2:
            set_ticks([(0, '0'),
                     (15, ''),
                     (30, '30'),
                     (45, ''),
                     (60, '60'),
                      (75, ''),
                     (90, '90')], 90)
        else:
            set_ticks([(0, '0'),
                     (45, '45'),
                     (90, '90'),
                     (135, '135'),
                     (180, '180')], 180)

    report.last().add_to(figure, caption)


def add_order_comparison_figure(report, nid, figure, caption,
                                x_order, y_order, xlabel, ylabel):
    print('add_order_comparison_figure(%s)' % nid)

    x_order = np.array(x_order.flat)
    y_order = np.array(y_order.flat)
    n = x_order.size
    assert x_order.max() == n - 1
    assert y_order.max() == n - 1
    with report.plot(nid, figsize=(fsize, fsize)) as pylab:
        set_spines_look_A(pylab)

        pylab.plot(x_order, y_order, 'ms', **get_plot_params(x_order.size))

        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.xticks([0, n - 1], ['0', '$n-1$'])
        pylab.yticks([0, n - 1], ['0', '$n-1$'])
        r = correlation_coefficient(x_order, y_order)

        pylab.annotate('corr. = %.4f' % r,
                       va='top',
                       ha='right',
                       xy=(0.95, 0.95), # 0.25 for other
                       xycoords='figure fraction')

        pylab.axis([0, n - 1, 0, n - 1])

        pylab.gca().xaxis.set_label_coords(0.5, -0.25)
        pylab.gca().yaxis.set_label_coords(-0.25, 0.5)

    report.last().add_to(figure, caption)


def plot_one_against_the_other(r, nid, xval, yval):
    print('plot_one_against_the_other(%s)' % nid)
    h = create_histogram_2d(xval, yval, resolution=128)
    n = r.data(nid, np.flipud(h.T)).display('scale')
    return n


def zero_diagonal(R):
    ''' Returns a copy with diagonal set to zero. '''
    n = R.shape[0]
    return R * (1 - np.eye(n))


