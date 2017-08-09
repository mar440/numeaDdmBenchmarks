from __future__ import print_function
import numpy as np
import sys
import imp


SYM_CASE = False


def setPar(argv,param):

	try:
            i = argv.index(param)
	except ValueError:
            i = -1
	if i < 0 or i == len(argv): 
            print("parameter %s does not exist" % (param))
            print("\n or  %s does not have specified a value" % (param))
            str0 = ""
	else:
            str0 = param + "=" + argv[i+1] 
	return str0 

def main(Nx1 = 1, Ny1 = 2, Nz1 = 1,nx1 = 4, ny1 = 2, nz1 = 2, \
         Nx2 = 1, Ny2 = 2, Nz2 = 1,nx2 = 4, ny2 = 2, nz2 = 2, benchmark = ''): 


    if len(sys.argv)>0:
        outStr = setPar(sys.argv,"Nx1")
        exec(outStr)
        outStr = setPar(sys.argv,"Ny1")
        exec(outStr)
        outStr = setPar(sys.argv,"Nz1")
        exec(outStr)
        outStr = setPar(sys.argv,"nx1")
        exec(outStr)
        outStr = setPar(sys.argv,"ny1")
        exec(outStr)
        outStr = setPar(sys.argv,"nz1")
        exec(outStr)
        outStr = setPar(sys.argv,"Nx2")
        exec(outStr)
        outStr = setPar(sys.argv,"Ny2")
        exec(outStr)
        outStr = setPar(sys.argv,"Nz2")
        exec(outStr)
        outStr = setPar(sys.argv,"nx2")
        exec(outStr)
        outStr = setPar(sys.argv,"ny2")
        exec(outStr)
        outStr = setPar(sys.argv,"nz2")
        exec(outStr)
        outStr = setPar(sys.argv,"benchmark")
        exec(outStr)


        Lx1 = Ly1 = Lz1 = 0.0; x10 = y10 = z10 = 0.0; R1 = 0.0
        Lx2 = Ly2 = Lz2 = 0.0; x20 = y20 = z20 = 0.0; R2 = 0.0

        if benchmark == 1:
	    R2 = 5.0  # outer radius 
	    R1 = 4.0  # inner radius
	    #  - square 
	    H = 2.0    
            x10 = 0.0
	    y10 = R1
	    Lx1 = 0.5 * np.pi 
	    Ly1 = (R2 - R1)


        elif benchmark == 2:
            H = 2.0    
            R1 = 4.0  # inner radius
            R2 = 5.0  # outer radius 
            #  - square 
            eps0 = 1e-5
            x10 = -0.5 * np.pi + eps0
            y10 = R1
            Lx1 = 1 * np.pi 
            Ly1 = (R2 - R1)
            #
            Lx2 = H 
            Ly2 = H
            x20 = -0.5 * Lx2 
            y20 = R2 
        elif benchmark == 3:
            c = 3
        elif benchmark == 4: 
            H = 2.0

            Lx1 = 5. 
            Ly1 = 5.
            x10 = -0.5 * Lx1
            y10 = 0.0
    
            Lx2 = H 
            Ly2 = H
            x20 = -0.5 * Lx2 
            y20 = 0.999 * Ly1 

        elif benchmark == 5:
            Lx1 = 6.
            Ly1 = 1.
            Lz1 = 1. 
            x10 = 0.0
            y10 = 0.0
            z10 = 0.0
        elif benchmark == 6:
            Lx1 = 8.
            Ly1 = 2.
            Lz1 = 2. 
            x10 = -0.5 * Lx1
            y10 = -0.5 * Ly1
            z10 = -0.5 * Lz1 
        elif benchmark == 7: 
            # lower (bigger)
            Lx1 = 4.00
            Ly1 = 2.00
            Lz1 = 2.00 
            x10 = -4.00
            y10 = -1.00
            z10 = -1.00 
            # upper (smaller)
            Lx2 = 4.00
            Ly2 = 2.00
            Lz2 = 2.00
            x20 = 0.00
            y20 = -1.00
            z20 = -1.00 
        elif benchmark == 8: 
            # lower (bigger)
            Lx1 = 5.00
            Ly1 = 5.00
            Lz1 = 0.75 
            x10 = -Lx1 * 0.50
            y10 =  0.00
            z10 = -Lz1 * 0.50
            
            # upper (smaller)
            Lx2 = 2.00
            Ly2 = 2.00
            Lz2 = 0.50
            x20 = -Lx2 * 0.50
            y20 =  0.999999 * Ly1
            z20 = -Lz2 * 0.50
        elif benchmark == 9:
            # lower (bigger)
            Lx1 = 2.50
            Ly1 = 5.00
            Lz1 = 0.75 
            x10 = -Lx1 * 0.30
            y10 = 0.00
            z10 = -Lz1 * 0.50
            
            # upper (smaller)
            Lx2 = 2.00
            Ly2 = 2.00
            Lz2 = 0.50
            x20 = -Lx2 * 0.50
            y20 =  Ly1
            z20 = -Lz2 * 0.50 
            
            R1 = 6.0 * Ly2
            R2 = 3.0 * Ly2 

    elements, coordinates, PartitionId, MaterialId, FormulationId, Piece, Piece_nod, dim = \
        create_fem(  Lx1, Ly1, Lz1, x10, y10, z10, nx1, ny1, nz1, Nx1, Ny1, Nz1, R1,\
                        Lx2, Ly2, Lz2, x20, y20, z20, nx2, ny2, nz2, Nx2, Ny2, Nz2, R2, benchmark) 
    
    file_name_r = 'mesh.vtu' 

    if Lz2 == 0:
        Nx2 = Ny2 = Nz2 = 0


    nxAll = nx1 * Nx1 + nx2 * Nx2
    nyAll = ny1 * Ny1 + ny2 * Ny2
    nzAll = nz1 * Nz1 + nz2 * Nz2 
    
    if dim == 2:
        vtu2d(elements,coordinates,MaterialId, PartitionId, FormulationId,file_name_r)
    elif dim == 3:
        vtu3d(   elements,coordinates,MaterialId, PartitionId, FormulationId, 
                            Piece, Piece_nod, file_name_r, benchmark, nxAll, nyAll, nzAll)


# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
#  MESH GENERATOR MODULE - START
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

def create_fem( Lx1, Ly1, Lz1, x10, y10, z10,\
                   nx1, ny1, nz1, Nx1, Ny1, Nz1, R1,\
                Lx2, Ly2, Lz2, x20, y20, z20,\
                    nx2, ny2, nz2, Nx2, Ny2, Nz2, R2, benchmark):


    if Lz1 == 0:
        dim = 2
    else:
        dim = 3
 

 

    if dim == 2:
        elements1, coordinates1, PartitionId1, MaterialId1, FormulationId1 = \
            create_fem2d(Lx1, Ly1, x10, y10, nx1, ny1, Nx1, Ny1)
        elements2, coordinates2, PartitionId2, MaterialId2, FormulationId2 = \
            create_fem2d(Lx2, Ly2, x20, y20, nx2, ny2, Nx2, Ny2)
    elif dim == 3:
        elements1, coordinates1, PartitionId1, MaterialId1, FormulationId1 = \
            create_fem3d(Lx1, Ly1, Lz1, x10, y10, z10, nx1, ny1, nz1, Nx1, Ny1, Nz1)
        elements2, coordinates2, PartitionId2, MaterialId2, FormulationId2 = \
            create_fem3d(Lx2, Ly2, Lz2, x20, y20, z20, nx2, ny2, nz2, Nx2, Ny2, Nz2)


    if benchmark == 9:
        coordinates1, coordinates2 = \
            transformCoord(coordinates1,coordinates2, Lx1, Ly1, R1, Lx2, Ly2, R2) 
    if benchmark == 1 or benchmark == 2: 
	x_transform = coordinates1[:,1] * np.sin(coordinates1[:,0])
	y_transform = coordinates1[:,1] * np.cos(coordinates1[:,0])
	coordinates1[:,0] = x_transform; coordinates1[:,1] = y_transform

    elements = np.vstack((elements1,elements2 + coordinates1.shape[0]))
    coordinates = np.vstack((coordinates1,coordinates2))
    MaterialId1 = np.ones(MaterialId1.shape[0],dtype = np.int32) * 1
    MaterialId2 = np.ones(MaterialId2.shape[0],dtype = np.int32) * 2
    MaterialId = np.concatenate((MaterialId1,MaterialId2))
    PartitionId = np.concatenate((PartitionId1,PartitionId2 + PartitionId1.max() + 1)) 


    FormulationId = np.concatenate((FormulationId1,FormulationId2))
    PieceId1 = np.ones(MaterialId1.shape[0],dtype = np.int32) * 1
    PieceId2 = np.ones(MaterialId2.shape[0],dtype = np.int32) * 2 
    Piece = np.concatenate((PieceId1,PieceId2)) 
    PieceId_nod_1 = np.ones(coordinates1.shape[0],dtype = np.int32) * 1
    PieceId_nod_2 = np.ones(coordinates2.shape[0],dtype = np.int32) * 2
    Piece_nod = np.concatenate((PieceId_nod_1,PieceId_nod_2))



    if benchmark == 7:
        np.savetxt('coordinatesLeft.dat',coordinates1)
        np.savetxt('coordinatesRight.dat',coordinates2)
        np.savetxt('elements.dat',elements) 

    return elements, coordinates, PartitionId, MaterialId, FormulationId, Piece, Piece_nod, dim


def transformCoord(coordinates1,coordinates2, Lx1, Ly1, R1, Lx2, Ly2, R2):
    x_ = coordinates1[:,0]
    y_ = coordinates1[:,1]

    a0 = 1.0 / Ly1
    b0 = 0.0 
    yy = -np.sqrt(R1**2 - (x_ + 0.5 * Lx1)**2) + y_ + R1
    w = a0 * y_ + b0 
    coordinates1[:,1] = y_ + w * ( yy - y_ ) 

    x_ = coordinates2[:,0]
    y_ = coordinates2[:,1]

    a0 = - 1.0 / Ly2
    b0 = (Ly1 + Ly2) / Ly2 
    yy = -np.sqrt(R2**2 - (x_ + 0.5 * Lx1)**2) + y_ + R2
    w = a0 * y_ + b0 
    coordinates2[:,1] = y_ + w * ( yy - y_ ) 

    return coordinates1, coordinates2 

def create_fem2d(_Lx, _Ly , x0, y0, _nx, _ny, _Nx, _Ny): 

     
    
    if _Lx == 0 and _Ly == 0:
        nEl = 0
        nNod = 0
        elements=np.zeros((nEl,4),dtype=np.int32)
        coordinates=np.zeros((nNod,3),dtype=np.float64)
        MaterialId = np.ones(nEl,dtype = np.int32)
        MaterialId = np.ones(nEl,dtype = np.int32)
        PartitionId = np.zeros(nEl,dtype = np.int32)
        FormulationId = np.ones(nEl,dtype = np.int32) 
    else: 
        _nx0 = _nx
        _ny0 = _ny
        _nx = _Nx * _nx
        _ny = _Ny * _ny


        nEl=_nx*_ny
        nNod=(_nx+1)*(_ny+1)
        elements=np.zeros((nEl,4),dtype=np.int32)
        coordinates=np.zeros((nNod,3),dtype=np.float64)
        hx=_Lx/_nx
        hy=_Ly/_ny
        
        cnt=0
        for j in range(_ny):
            for i in range(_nx):
                elements[cnt,:]=np.array([  i,
                                            i+1,
                                            (_nx+1)+i+1,
                                            (_nx+1)+i]) + j*(_nx+1)
                cnt+=1
        cnt=0
        for j in range(_ny+1):
            for i in range(_nx+1):
                coordinates[cnt,[0,1]]=np.array([i*hx + x0,j*hy + y0])
                cnt+=1


        PartitionId = np.zeros(nEl,dtype = np.int32)



        if _Nx * _Ny > 1:
            X=np.zeros((_nx,_ny),dtype = np.int32)
            c=0

            for j in range(_Ny):
                for i in range(_Nx):
                    in1 = np.arange(i * _nx0,(i+1) * _nx0 )
                    in2 = np.arange(j * _ny0,(j+1) * _ny0 )
                    X[np.ix_(in1,in2)]=c
                    c+=1 
            PartitionId = X.reshape(_nx*_ny,order='F') 
        else:
            PartitionId = np.zeros(_nx*_ny,dtype = np.int32) 

        MaterialId = np.ones(nEl,dtype = np.int32)
        FormulationId = np.ones(nEl,dtype = np.int32)

    return elements, coordinates, PartitionId, MaterialId, FormulationId


def create_fem3d(   Lx = 1., Ly = 1., Lz = 1., x0 = 0.0, y0 = 0.0, z0 = 0.0,\
                    nxd = 3, nyd = 3, nzd = 3,  Nx = 2, Ny = 2, Nz = 2):

#    Lx = 1.; Ly = 1.; Lz = 1.; nxd = 3;nyd = 3; nzd = 3; Nx = 2; Ny = 2; Nz = 2
#    x0 = 0.0; y0 = 0.0; z0 = 0.0;

    if Lx == 0 and Ly == 0 and Lz == 0:
        nEl = 0
        nNod = 0
        elements=np.zeros((nEl,8),dtype=np.int32)
        coordinates=np.zeros((nNod,3),dtype=np.float64)
        MaterialId = np.ones(nEl,dtype = np.int32)
        MaterialId = np.ones(nEl,dtype = np.int32)
        PartitionId = np.zeros(nEl,dtype = np.int32)
        FormulationId = np.ones(nEl,dtype = np.int32) 
    else:
#        return elements, coordinates, coarse_element_id, MaterialId, PartitionId, FormulationId
     
        nx = nxd * Nx
        ny = nyd * Ny
        nz = nzd * Nz
        nnods = (nx+1)*(ny+1)*(nz+1)
        nelem =  nx*ny*nz
        coordinates = np.zeros((nnods,3),dtype = np.float64)
        elements    = np.zeros((nelem,8),dtype = np.int32)   
        edges       = np.zeros((2*nx*ny+2*nx*nz+2*ny*nz,7), dtype = np.int32) 
        
        
        cnt = 0
        nxy = (nx + 1)*(ny + 1)
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    tmp = np.array([i + 0 + (j + 0) * (nx + 1),
                                    i + 1 + (j + 0) * (nx + 1),
                                    i + 1 + (j + 1) * (nx + 1),
                                    i + 0 + (j + 1) * (nx + 1)])
                    elements[cnt,:] = np.concatenate((tmp + k * nxy, tmp + (k + 1) * nxy))
                    cnt += 1
        
        dx = Lx/nx
        dy = Ly/ny
        dz = Lz/nz
        cnt = 0
        for k in range(nz+1):
            for j in range(ny+1):
                for i in range(nx+1):
                    coordinates[cnt,:] = np.array([i*dx + x0 , j*dy + y0 , k*dz + z0])
                    cnt += 1
        if Nx*Ny*Nz > 1:
            #a[ix_([1,3,4],[0,2])]
            X=np.zeros((nx,ny,nz), dtype = np.int32)
            c=0
            for k in range(Nz):
                for j in range(Ny):
                    for i in range(Nx):
                        in1 = np.arange((i)*nxd,(i+1)*nxd)
                        in2 = np.arange((j)*nyd,(j+1)*nyd)
                        in3 = np.arange((k)*nzd,(k+1)*nzd)
                        X[np.ix_(in1,in2,in3)]=c
                        c+=1 
            PartitionId = X.reshape(nelem, order='F') 
        else:
            PartitionId = np.zeros(nelem, dtype = np.int32) 

        edges = np.array([0,0])
        MaterialId = np.ones(nelem, dtype = np.int32)
        FormulationId = 30 * np.ones(nelem, dtype = np.int32 )
         
        
    #    elements = 0
    #    coordinates = 0
    #    edges = 0
    #    PartitionId = 0
    #    MaterialId = 0
    #    FormulationId = 0

    return elements, coordinates, PartitionId, MaterialId, FormulationId 

# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
#  MESH GENERATOR MODULE - END
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH


# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
#  VTK MODULE - START
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH


def vtu2d(elements,coordinates,MaterialId, PartitionId, FormulationId,file_name ):

    f = open(file_name, "w")

    sp1='  '
    
    str = '<?xml version=\"1.0\"?>\n'
    f.write(str)
    str = '<VTKFile type=\"UnstructuredGrid\" version=\"0.1\" byte_order=\"LittleEndian\" compressor=\"vtkZLibDataCompressor\">\n'
    f.write(str)
    str = '%s<UnstructuredGrid>\n' % (sp1)
    f.write(str)
    str = '%s<Piece NumberOfPoints="%d" NumberOfCells="%d">\n' % (2*sp1,coordinates.shape[0], elements.shape[0])
    f.write(str)
    str = '%s<PointData>\n' % (3*sp1)
    f.write(str)
    str = '%s</PointData>\n' % (3*sp1)
    f.write(str)
    str = '%s<CellData>\n'% (3*sp1)
    f.write(str)

    str = '%s<DataArray type="Int64" Name="MaterialId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,MaterialId.min(),MaterialId.max())
    f.write(str) 

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % MaterialId[ix])
        ix += 1
        if ix == MaterialId.shape[0]:
            break 
        cnt += 1 

    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)

    str = '%s<DataArray type="Int64" Name="FormulationId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,FormulationId.min(),FormulationId.max())
    f.write(str)

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % FormulationId[ix])
        ix += 1
        if ix == FormulationId.shape[0]:
            break 
        cnt += 1 



    str = '\n%s</DataArray>\n'%(4*sp1)
    f.write(str)

    str = '%s<DataArray type="Int64" Name="PartitionId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,PartitionId.min(),PartitionId.max())
    f.write(str)

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % PartitionId[ix])
        ix += 1
        if ix == PartitionId.shape[0]:
            break 
        cnt += 1 




    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
    str = '%s</CellData>\n' % (3*sp1)
    f.write(str)

    str = '%s<Points>\n' % (3*sp1)
    f.write(str)


    str = '%s<DataArray type="Float64" Name="Points" NumberOfComponents="%d" format="ascii" RangeMin="%e" RangeMax="%e">' % \
                                             (4*sp1,coordinates.shape[1], coordinates.min(),coordinates.max())
    f.write(str)

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%f ' % coordinates[ix,iy])

        if iy < coordinates.shape[1]-1:
            iy += 1
        else:
            iy = 0
            ix += 1
        if ix == coordinates.shape[0]:
            break

        cnt += 1
        
    str =  '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
    str = '%s</Points>\n' % (3*sp1)
    f.write(str)

    str = '%s<Cells>\n' % (3*sp1)
    f.write(str)

    str =  '%s<DataArray type="Int64" Name="connectivity" format="ascii" RangeMin="%d" RangeMax="%d">' % \
                                                                    (4*sp1, elements.min(), elements.max())
    f.write(str) 



    offset = np.zeros(elements.shape[0])
    cnt_ = 0
    for i in range(elements.shape[0]):
        cnt_ += elements.shape[1]
        offset[i] = cnt_ 

    go = True
    ix = 0
    iy = 0
    cnt = 0
    cnst_ = 6
    while (go): 
        if ((cnt%cnst_)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % elements[ix,iy])

        if iy < elements.shape[1]-1:
            iy += 1
        else:
            iy = 0
            ix += 1
        if ix == elements.shape[0]:
            break

        cnt += 1





    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)

    str =  '%s<DataArray type="Int64" Name="offsets" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,offset.min(),offset.max())
    f.write(str)
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % offset[ix])
        ix += 1
        if ix == offset.shape[0]:
            break 
        cnt += 1 

    str =  '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)


    types = 9 * np.ones(elements.shape[0],dtype = np.int32)
    str =  '%s<DataArray type="UInt8" Name="types" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,types.min(),types.max())
    f.write(str) 
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % types[ix])
        ix += 1
        if ix == types.shape[0]:
            break 
        cnt += 1 



    str =  '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
    str =  '%s</Cells>\n' % (3*sp1)
    f.write(str)
    str =  '%s</Piece>\n' % (2*sp1)
    f.write(str)
    str =  '%s</UnstructuredGrid>\n' % (1*sp1)
    f.write(str)
    str =  '</VTKFile>\n'
    f.write(str)

    f.close()



def vtuHexa(elements,coordinates,MaterialId, PartitionId, FormulationId,file_name ):

    f = open(file_name, "w")

    sp1='  '
    
    
    str = '<?xml version=\"1.0\"?>\n'
    f.write(str)
    str = '<VTKFile type=\"UnstructuredGrid\" version=\"0.1\" byte_order=\"LittleEndian\" compressor=\"vtkZLibDataCompressor\">\n'
    f.write(str)
    str = '%s<UnstructuredGrid>\n' % (sp1)
    f.write(str)
    str = '%s<Piece NumberOfPoints="%d" NumberOfCells="%d">\n' % (2*sp1,coordinates.shape[0], elements.shape[0])
    f.write(str)
    str = '%s<PointData>\n' % (3*sp1)
    f.write(str)
    str = '%s</PointData>\n' % (3*sp1)
    f.write(str)
    str = '%s<CellData>\n'% (3*sp1)
    f.write(str)

    str = '%s<DataArray type="Int64" Name="MaterialId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,MaterialId.min(),MaterialId.max())
    f.write(str) 

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % MaterialId[ix])
        ix += 1
        if ix == MaterialId.shape[0]:
            break 
        cnt += 1 

    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)

    str = '%s<DataArray type="Int64" Name="FormulationId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,FormulationId.min(),FormulationId.max())
    f.write(str)

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % FormulationId[ix])
        ix += 1
        if ix == FormulationId.shape[0]:
            break 
        cnt += 1 



    str = '\n%s</DataArray>\n'%(4*sp1)
    f.write(str)

    str = '%s<DataArray type="Int64" Name="PartitionId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,PartitionId.min(),PartitionId.max())
    f.write(str)

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % PartitionId[ix])
        ix += 1
        if ix == PartitionId.shape[0]:
            break 
        cnt += 1 




    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
    str = '%s</CellData>\n' % (3*sp1)
    f.write(str)

    str = '%s<Points>\n' % (3*sp1)
    f.write(str)


    str = '%s<DataArray type="Float64" Name="Points" NumberOfComponents="%d" format="ascii" RangeMin="%e" RangeMax="%e">' % (4*sp1,coordinates.shape[1], coordinates.min(),coordinates.max())
    f.write(str)

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%f ' % coordinates[ix,iy])

        if iy < coordinates.shape[1]-1:
            iy += 1
        else:
            iy = 0
            ix += 1
        if ix == coordinates.shape[0]:
            break

        cnt += 1
        
    str =  '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
    str = '%s</Points>\n' % (3*sp1)
    f.write(str)

    str = '%s<Cells>\n' % (3*sp1)
    f.write(str)

    str =  '%s<DataArray type="Int64" Name="connectivity" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1, elements.min(), elements.max())
    f.write(str) 



    offset = np.zeros(elements.shape[0])
    cnt_ = 0
    for i in range(elements.shape[0]):
        cnt_ += elements.shape[1]
        offset[i] = cnt_ 

    go = True
    ix = 0
    iy = 0
    cnt = 0
    cnst_ = 6
    while (go): 
        if ((cnt%cnst_)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % elements[ix,iy])

        if iy < elements.shape[1]-1:
            iy += 1
        else:
            iy = 0
            ix += 1
        if ix == elements.shape[0]:
            break

        cnt += 1





    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)

    str =  '%s<DataArray type="Int64" Name="offsets" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,offset.min(),offset.max())
    f.write(str)
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % offset[ix])
        ix += 1
        if ix == offset.shape[0]:
            break 
        cnt += 1 



    str =  '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)


    types = 12 * np.ones(elements.shape[0], dtype = np.int32)
    str =  '%s<DataArray type="UInt8" Name="types" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,types.min(),types.max())
    f.write(str) 
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % types[ix])
        ix += 1
        if ix == types.shape[0]:
            break 
        cnt += 1 



    str =  '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
    str =  '%s</Cells>\n' % (3*sp1)
    f.write(str)
    str =  '%s</Piece>\n' % (2*sp1)
    f.write(str)
    str =  '%s</UnstructuredGrid>\n' % (1*sp1)
    f.write(str)
    str =  '</VTKFile>\n'
    f.write(str)

    f.close()

def vtu3d(  elements, coordinates, MaterialId, PartitionId, FormulationId, 
            PieceId_elem,PieceId_nod, file_name, benchmark,
            nxAll, nyAll, nzAll):
        
#        (elements,coordinates,MaterialId, PartitionId, FormulationId,file_name )

    f = open(file_name, "w")

    sp1='  '


    
    str = '<?xml version=\"1.0\"?>\n'
    f.write(str)
    str = '<VTKFile type=\"UnstructuredGrid\" version=\"0.1\" byte_order=\"LittleEndian\" compressor=\"vtkZLibDataCompressor\">\n'
    f.write(str)
    str = '%s<UnstructuredGrid>\n' % (sp1)
    f.write(str)




# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH 
# time harmonic problem only - dirichlet for all nodes ...
    if (benchmark == 5):
        str = '%s<FieldData>\n' % (2 * sp1)
        f.write(str)

        str = '%s<DataArray type=\"Int32\" Name=\"DSet_FIXE_TRACTION\" NumberOfComponents=\"2\" NumberOfTuples=\"%d\" format=\"ascii\" >\n' % (3 * sp1,coordinates.shape[0] * 2)
        f.write(str) 
        for i in range(coordinates.shape[0]):
            str = '%s %d %d %d %d\n' % (4 * sp1, i, 1, i, 2)
            f.write(str) 
        str = '%s</DataArray>\n' % (3 * sp1)
        f.write(str) 

        NumberOfTuples_DSet_TRACTION = (nyAll + 1) * (nzAll + 1)
        str = '%s<DataArray type=\"Int32\" Name=\"DSet_TRACTION\" NumberOfComponents=\"2\" NumberOfTuples=\"%d\" format=\"ascii\" >\n' % (3 * sp1, NumberOfTuples_DSet_TRACTION  )
        f.write(str) 
        tmp = np.arange(0, coordinates.shape[0], nxAll+1)
        for i in range(NumberOfTuples_DSet_TRACTION):
            str = '%s %d %d \n' % (4 * sp1, tmp[i], 0)
            f.write(str) 
        str = '%s</DataArray>\n' % (3 * sp1)
        f.write(str) 


    #	   <DataArray type="Int32" Name="DSet_TRACTION" NumberOfComponents="2" NumberOfTuples="4" format="ascii" >

        str = '%s</FieldData>\n' % (2 * sp1)
        f.write(str)
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH 
    str = '%s<Piece NumberOfPoints="%d" NumberOfCells="%d">\n' % (2*sp1,coordinates.shape[0], elements.shape[0])
    f.write(str)
#-------------------------------------------------------------------------------------------------------# 
    str = '%s<DataArray type="Int64" Name="RegionId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,PieceId_nod.min() - 1 ,PieceId_nod.max() - 1)
    f.write(str)
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % (PieceId_nod[ix] - 1))
        ix += 1
        if ix == PieceId_nod.shape[0]:
            break 
        cnt += 1 
    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str) 



#    str = '%s<PointData>\n' % (3*sp1)
#    f.write(str)
#    str = '%s</PointData>\n' % (3*sp1)
#    f.write(str)
    str = '%s<CellData>\n'% (3*sp1)
    f.write(str) 
#-------------------------------------------------------------------------------------------------------#
    str = '%s<DataArray type="Int64" Name="MaterialId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,MaterialId.min(),MaterialId.max())
    f.write(str) 

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % MaterialId[ix])
        ix += 1
        if ix == MaterialId.shape[0]:
            break 
        cnt += 1 

    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
#---------------------------------------------------------------------------------------------------------------------#
    str = '%s<DataArray type="Int64" Name="FormulationId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,FormulationId.min(),FormulationId.max())
    f.write(str)
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % FormulationId[ix])
        ix += 1
        if ix == FormulationId.shape[0]:
            break 
        cnt += 1 
    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)

#---------------------------------------------------------------------------------------------------------------------# 
    str = '%s<DataArray type="Int64" Name="RegionId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,PieceId_elem.min() - 1 ,PieceId_elem.max() - 1)
    f.write(str)
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % (PieceId_elem[ix] - 1))
        ix += 1
        if ix == PieceId_elem.shape[0]:
            break 
        cnt += 1 
    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str) 
#---------------------------------------------------------------------------------------------------------------------#
    str = '%s<DataArray type="Int64" Name="PieceId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,PieceId_elem.min(),PieceId_elem.max())
    f.write(str)
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % PieceId_elem[ix])
        ix += 1
        if ix == PieceId_elem.shape[0]:
            break 
        cnt += 1 
    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str) 
#---------------------------------------------------------------------------------------------------------------------#
    str = '%s<DataArray type="Int64" Name="PartitionId" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,PartitionId.min(),PartitionId.max())
    f.write(str)

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % PartitionId[ix])
        ix += 1
        if ix == PartitionId.shape[0]:
            break 
        cnt += 1 
    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
#---------------------------------------------------------------------------------------------------------------------# 
    str = '%s</CellData>\n' % (3*sp1)
    f.write(str)

    str = '%s<Points>\n' % (3*sp1)
    f.write(str)


    str = '%s<DataArray type="Float64" Name="Points" NumberOfComponents="%d" format="ascii" RangeMin="%e" RangeMax="%e">' % (4*sp1,coordinates.shape[1], coordinates.min(),coordinates.max())
    f.write(str)

    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%f ' % coordinates[ix,iy])

        if iy < coordinates.shape[1]-1:
            iy += 1
        else:
            iy = 0
            ix += 1
        if ix == coordinates.shape[0]:
            break

        cnt += 1
        
    str =  '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
    str = '%s</Points>\n' % (3*sp1)
    f.write(str)

    str = '%s<Cells>\n' % (3*sp1)
    f.write(str)

    str =  '%s<DataArray type="Int64" Name="connectivity" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1, elements.min(), elements.max())
    f.write(str) 



    offset = np.zeros(elements.shape[0], dtype = np.int32)
    cnt_ = 0
    for i in range(elements.shape[0]):
        cnt_ += elements.shape[1]
        offset[i] = cnt_ 

    go = True
    ix = 0
    iy = 0
    cnt = 0
    cnst_ = 6
    while (go): 
        if ((cnt%cnst_)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % elements[ix,iy])

        if iy < elements.shape[1]-1:
            iy += 1
        else:
            iy = 0
            ix += 1
        if ix == elements.shape[0]:
            break

        cnt += 1





    str = '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)

    str =  '%s<DataArray type="Int64" Name="offsets" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,offset.min(),offset.max())
    f.write(str)
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % offset[ix])
        ix += 1
        if ix == offset.shape[0]:
            break 
        cnt += 1 



    str =  '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)


    types = 12 * np.ones(elements.shape[0],dtype = np.int32)
    str =  '%s<DataArray type="UInt8" Name="types" format="ascii" RangeMin="%d" RangeMax="%d">' % (4*sp1,types.min(),types.max())
    f.write(str) 
    go = True
    ix = 0
    iy = 0
    cnt = 0
    while (go): 
        if ((cnt%6)==0):
            f.write('\n%s' % (5*sp1))
        f.write('%d ' % types[ix])
        ix += 1
        if ix == types.shape[0]:
            break 
        cnt += 1 



    str =  '\n%s</DataArray>\n' % (4*sp1)
    f.write(str)
    str =  '%s</Cells>\n' % (3*sp1)
    f.write(str)
    str =  '%s</Piece>\n' % (2*sp1)
    f.write(str)
    str =  '%s</UnstructuredGrid>\n' % (1*sp1)
    f.write(str)
    str =  '</VTKFile>\n'
    f.write(str)

    f.close()

# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
#  VTK MODULE - START
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH


if __name__ == "__main__":
	main()
