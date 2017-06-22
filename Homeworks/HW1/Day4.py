import vtk
#help(vtk.vtkRectilinearGridReader())

rectGridReader = vtk.vtkRectilinearGridReader()
rectGridReader.SetFileName("data/jet4_0.500.vtk")
# do not forget to call "Update()" at the end of the reader
rectGridReader.Update()

rectGridOutline = vtk.vtkRectilinearGridOutlineFilter()
rectGridOutline.SetInputData(rectGridReader.GetOutput())

# New vtkRectilinearGridGeometryFilter() goes here:
#
#
#
#
plane = vtk.vtkRectilinearGridGeometryFilter()
plane.SetInputData(rectGridReader.GetOutput())

rectGridOutlineMapper = vtk.vtkPolyDataMapper()
rectGridOutlineMapper.SetInputConnection(rectGridOutline.GetOutputPort())

rectGridGeomMapper = vtk.vtkPolyDataMapper()
rectGridGeomMapper.SetInputConnection(plane.GetOutputPort())
#

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(rectGridOutlineMapper)
outlineActor.GetProperty().SetColor(0, 0, 0)

gridGeomActor = vtk.vtkActor()
gridGeomActor.SetMapper(rectGridGeomMapper)
gridGeomActor.GetProperty().SetRepresentationToWireframe()
gridGeomActor.GetProperty().SetColor(0, 0, 0)

# Find out how to visualize this as a wireframe
# Play with the options you get for setting up actor properties (color, opacity, etc.)

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

renderer.AddActor(outlineActor)
renderer.AddActor(gridGeomActor)

renderer.SetBackground(1, 1, 1)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(60.0)
renderer.GetActiveCamera().Azimuth(30.0)
renderer.GetActiveCamera().Zoom(1.0)

renWin.SetSize(300, 300)

# interact with data
renWin.Render()
iren.Start()

magnitudeCalcFilter = vtk.vtkArrayCalculator()
magnitudeCalcFilter.SetInputConnection(rectGridReader.GetOutputPort())
magnitudeCalcFilter.AddVectorArrayName('vectors')
# Set up here the array that is going to be used for the computation ('vectors')
magnitudeCalcFilter.SetResultArrayName('magnitude')

#Se agrega esta linea para usar la funcion mag (magitute)
magnitudeCalcFilter.SetFunction("mag(vectors)")
# Set up here the function that calculates the magnitude of a vector
magnitudeCalcFilter.Update()

#Extract the data from the result of the vtkCalculator
points = vtk.vtkPoints()
grid = magnitudeCalcFilter.GetOutput()
grid.GetPoints(points)
scalars = grid.GetPointData().GetArray('magnitude')

#Create an unstructured grid that will contain the points and scalars data
ugrid = vtk.vtkUnstructuredGrid()
ugrid.SetPoints(points)
ugrid.GetPointData().SetScalars(scalars)

#Populate the cells in the unstructured grid using the output of the vtkCalculator
for i in range (0, grid.GetNumberOfCells()):
    cell = grid.GetCell(i)
    ugrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

# There are too many points, let's filter the points
subset = vtk.vtkMaskPoints()
subset.SetOnRatio(50)
subset.SetRandomModeType(1)
subset.SetInputData(ugrid)

# Make a vtkPolyData with a vertex on each point.
pointsGlyph = vtk.vtkVertexGlyphFilter()
pointsGlyph.SetInputConnection(subset.GetOutputPort())
# pointsGlyph.SetInputData(ugrid)
pointsGlyph.Update()

pointsMapper = vtk.vtkPolyDataMapper()
pointsMapper.SetInputConnection(pointsGlyph.GetOutputPort())
pointsMapper.SetScalarModeToUsePointData()

pointsActor = vtk.vtkActor()
pointsActor.SetMapper(pointsMapper)

renderer3 = vtk.vtkRenderer()
renWin3 = vtk.vtkRenderWindow()
renWin3.AddRenderer(renderer3)
iren3 = vtk.vtkRenderWindowInteractor()
iren3.SetRenderWindow(renWin3)

renderer3.AddActor(pointsActor)

renderer3.SetBackground(0, 0, 0)
renderer3.ResetCamera()
renderer3.GetActiveCamera().Elevation(60.0)
renderer3.GetActiveCamera().Azimuth(30.0)
renderer3.GetActiveCamera().Zoom(1.0)

renWin3.SetSize(300, 300)

# interact with data
renWin3.Render()
iren3.Start()

scalarRange = ugrid.GetPointData().GetScalars().GetRange()

isoFilter = vtk.vtkContourFilter()
isoFilter.SetInputData(ugrid)
isoFilter.GenerateValues(500, scalarRange)

isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(isoFilter.GetOutputPort())

isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetOpacity(0.5)

renderer3 = vtk.vtkRenderer()
renWin3 = vtk.vtkRenderWindow()
renWin3.AddRenderer(renderer3)
iren3 = vtk.vtkRenderWindowInteractor()
iren3.SetRenderWindow(renWin3)

renderer3.AddActor(isoActor)

renderer3.SetBackground(0, 0, 0)
renderer3.ResetCamera()
renderer3.GetActiveCamera().Elevation(60.0)
renderer3.GetActiveCamera().Azimuth(30.0)
renderer3.GetActiveCamera().Zoom(1.0)

renWin3.SetSize(300, 300)

# interact with data
renWin3.Render()
iren3.Start()
