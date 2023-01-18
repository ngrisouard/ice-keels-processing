def integrands(UD, ncgrp):
    """
    IN: UD='U' if upstream, 'D' if downstream
    ncgrp: netcdf group (data from one experiment)
    """
    from numpy import mean, meshgrid, ones, cumsum
    phi = ncgrp['phi' + UD][:, :]  # integrand of the mixing rate
    nz = phi.shape[1]
    Ns2 = mean(ncgrp['N2' + UD][:, :], axis=1)  # depth average
    _, N2 = meshgrid(ones(nz,), Ns2[:])  # replicate vertically
    cumphi = cumsum(phi, axis=1)
    _, Phi = meshgrid(ones(nz,), cumphi[:, -1])  # replicate vertically the sum
    
    return phi, N2, phi/N2, cumphi/Phi


def depth_averages(UD, ncgrp, t, z, phi, kap):
    """
    IN: UD='U' if upstream, 'D' if downstream
    ncgrp: netcdf group (data from one experiment)
    t, z: time and depth
    """
    from numpy import meshgrid, trapz
    
    L = ncgrp['L' + UD][:]
    Lt, _ = meshgrid(L, t)  # length of domain, replicated in time
    A = trapz(L, x=z)  # Surface area
    Phi = trapz(Lt*phi, x=z, axis=1)/A
    Kap = trapz(Lt*kap, x=z, axis=1)/A
    
    return Phi, Kap

def plot_one_exp(EXP, data):
    """ 
    """
    from numpy import meshgrid, amax, mean, cumsum, amin
    # from numpy import sum as npsum
    from matplotlib.pyplot import figure, colorbar, axes, show
    from matplotlib.colors import LogNorm
    from matplotlib.gridspec import GridSpec
    
    # INITIALIZING =============== #
    # These quantities never change
    z0 = 8.  # MLD [m]
    DB = 0.015  # total buoyancy dfference [m/s2]
    t0 = (z0/DB)**.5  # time unit
    mu = 2e-3  # molecular diffusivity
    
    # Coordinates
    time = data['time'][:]
    depth = data['z'][:]
    Z, T = meshgrid(depth/z0, time/t0)
    
    
    # COMPUTING =============== #
    phiU, N2U, kU, cumphiU = integrands('U', data)  # Upstream fields
    kU /= mu
    
    phiD, N2D, kD, cumphiD = integrands('D', data)  # Downstream fields
    kD /= mu
    
    PhiU, KU = depth_averages('U', data, time, depth, phiU, kU)
    PhiD, KD = depth_averages('D', data, time, depth, phiD, kD)
    
    # COMPUTING ZMIX ========== #
    
    # phiUSum = npsum(phiU, , axis=1)
    
    # PLOTTING ================ #
    fig = figure(tight_layout=True, figsize=(10, 4))
    gs = GridSpec(2, 2)
    fig.suptitle(EXP)
    
    t_start = 79.  # time at which I suggest to start the analysis
    
    # left subpanel: time series of up and down, superposed
    ax = fig.add_subplot(gs[:, 0])
    ax.semilogy(time/t0, KU, label='$K_U$')
    ax.semilogy(time/t0, KD, '--', label='$K_D$')
    ax.set_xlim(time[0]/t0, time[-1]/t0)
    ax.set_xlabel('$t/t_0$')
    ax.axvline(t_start, linewidth=1., color='m', linestyle=':')
    ax.grid()
    ax.legend()
    
    maxK = max(amax(kU), amax(kD))
    # top-right subpanel: Hovmoller of KU
    ax = fig.add_subplot(gs[0, 1])
    ca = ax.pcolormesh(T, Z, kU, norm=LogNorm(vmin=maxK*1e-10, vmax=maxK))
    ax.contour(T, Z, cumphiU, [0.9], colors='r', linewidths=1., linestyles='--')
    ax.invert_yaxis()
    ax.set_ylabel('$z/z_0$')
    ax.axvline(t_start, linewidth=1., color='m', linestyle=':')
    
    # bottom-right subpanel: Hovmoller of KD
    ax = fig.add_subplot(gs[1, 1])
    ax.pcolormesh(T, Z, kD, norm=LogNorm(vmin=maxK*1e-10, vmax=maxK))
    ax.contour(T, Z, cumphiD, [0.9], colors='r', linewidths=1., linestyles='--')
    ax.invert_yaxis()
    ax.set_xlabel('$t/t_0$')
    # ax.set_title('Downstream')
    ax.set_ylabel('$z/z_0$')
    # plt.colorbar(ca, ax=ax[0], orientation='vertical')
    ax.axvline(t_start, linewidth=1., color='m', linestyle=':')
    
    show()
    
    print('Time-averaged K_U = {0:2.1e}'.format(mean(KU)))
    print('Time-averaged K_D = {0:2.1e}'.format(mean(KD)))
    
    return