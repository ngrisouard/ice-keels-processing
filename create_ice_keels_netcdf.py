def write_group(sID, t, z, LU, LD, pU, pD, N2U, N2D):
    """ Create and fill the group for simulation sID.
    IN:
    sID [str]: F05H09, etc
    t, z [np arrays]: the time and depth arrays
    LU, LD [1D np arrays]: Up, Downstream lengths of integration for each z 
    pU, pD [2D np arrays]: Up, Downstream integrands of for Phi 
    N2U, N2D [2D np arrays]: Up, Downstream vertical grad of the sorted b
    OUT: N/A. The netCDF file gets edited directly. """
    from netCDF4 import Dataset
    from numpy import float64
    
    ncID = Dataset('ice-keels.nc', mode='a')
    
    grp = ncID.createGroup(sID)
    grp.createDimension('time', len(t))
    grp.createDimension('depth', len(z))
    
    # Time variable
    time = grp.createVariable('time', float64, ('time',), zlib=True)
    time.units = 's'
    time.long_name = 'Time'
    time[:] = t
    
    # Depth variable
    depth = grp.createVariable('z', float64, ('depth',), zlib=True)
    depth.units = 'm'
    depth.long_name = 'Depth'
    depth[:] = z
    
    # L_U, L_D variables
    LengthU = grp.createVariable('LU', float64, ('depth',), zlib=True)
    LengthU.units = 'm'
    LengthU.long_name = 'Integration length upstream'
    LengthU[:] = LU
    LengthD = grp.createVariable('LD', float64, ('depth',), zlib=True)
    LengthD.units = 'm'
    LengthD.long_name = 'Integration length downstream'
    LengthD[:] = LD
    
    # Integrands
    phiU = grp.createVariable('phiU', float64, ('time', 'depth',), zlib=True)
    phiU.units = ''
    phiU.long_name = 'Flux integrand upstream'
    phiU[:, :] = pU
    phiD = grp.createVariable('phiD', float64, ('time', 'depth',), zlib=True)
    phiD.units = ''
    phiD.long_name = 'Flux integrand downstream'
    phiD[:, :] = pD
    
    # Sorted buoyancy density gradients
    N2sU = grp.createVariable('N2U', float64, ('time', 'depth',), zlib=True)
    N2sU.units = ''
    N2sU.long_name = 'N2* upstream'
    N2sU[:, :] = N2U
    N2sD = grp.createVariable('N2D', float64, ('time', 'depth',), zlib=True)
    N2sD.units = ''
    N2sD.long_name = 'N2* downstream'
    N2sD[:, :] = N2D
    
    ncID.close()
    
    return


def create_netcdf(sims, t, z, LUs, LDs, pUs, pDs, NUs, NDs):
    """ """
    from netCDF4 import Dataset
    
    try: ncfile.close()  # make sure dataset is not already open.
    except: pass
    ncfile = Dataset('ice-keels.nc', mode='w')
    ncfile.title = "Mixing under ice keels"
    ncfile.close()  # will re-open, re-close for each simulation
    
    for sim in sims:
        write_group(sim, t[sim], z, LUs[sim], LDs[sim],
                    pUs[sim], pDs[sim], NUs[sim], NDs[sim])
        
    ncfile = Dataset('ice-keels.nc', mode='r')
    print(ncfile)
    ncfile.close()  # will re-open, re-close for each simulation
    
            
if __name__ == "__main__":
    print("This is the create_ice_keels_netcdf module. Import it all!")