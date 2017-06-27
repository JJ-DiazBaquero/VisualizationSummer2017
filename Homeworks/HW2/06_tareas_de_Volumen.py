import vtk

# Read the file (to test that it was written correctly)
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("D:\\Dropbox\\documentos\\Scientific Visualization\\06-20-2017\\SS_2017-master\\data\\wind_image.vti")
reader.Update()

#------------FILTER: RECTILINEAR GRID TO IMAGE DATA-----------
bounds = reader.GetOutput().GetBounds()
dimensions = reader.GetOutput().GetDimensions()
origin = (bounds[0], bounds[2], bounds[4])
spacing = (0.1,0.1,0.1)

imageData = vtk.vtkImageData()
imageData.SetOrigin(origin)
imageData.SetDimensions(dimensions)
imageData.SetSpacing(spacing)

probeFilter = vtk.vtkProbeFilter()
probeFilter.SetInputData(imageData)
probeFilter.SetSourceData(reader.GetOutput())
probeFilter.Update()

imageData2 = probeFilter.GetImageDataOutput()
#------------END RECTILINEAR GRID TO IMAGE DATA-----------

##------------FILTER, MAPPER, AND ACTOR: VOLUME RENDERING -------------------
# Create transfer mapping scalar value to opacity
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 1)
opacityTransferFunction.AddPoint(1, 1)
opacityTransferFunction.AddPoint(2, 0.1)
opacityTransferFunction.AddPoint(3, 1)

# Create transfer mapping scalar value to color
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(1, 0.5,0.5, 0.0)
colorTransferFunction.AddRGBPoint(2, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(2.5, 0.0, 0.0, 0.5)
colorTransferFunction.AddRGBPoint(3, 0, 1,0)


# The property describes how the data will look
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOff()
volumeProperty.SetInterpolationTypeToLinear()


# The mapper / ray cast function know how to render the data
#volumeMapper = vtk.vtkProjectedTetrahedraMapper()
#volumeMapper = vtk.vtkUnstructuredGridVolumeZSweepMapper()
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
#volumeMapper = vtk.vtkUnstructuredGridVolumeRayCastMapper()
volumeMapper.SetInputData(imageData2)

# The volume holds the mapper and the property and
# can be used to position/orient the volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

##------------END VOLUME RENDERING ----------------------

#---------RENDERER, RENDER WINDOW, AND INTERACTOR ----------
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddVolume(volume)
renderer.ResetCamera()

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(500, 500)
renderWindow.Render()

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)
iren.Start()
#---------END RENDERER, RENDER WINDOW, AND INTERACTOR -------