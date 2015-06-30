from cyclops import *
from pointCloud import *

scene = getSceneManager()
scene.addLoader(BinaryPointsLoader())

pointProgram = ProgramAsset()
pointProgram.name = "points"
pointProgram.vertexShaderName = "pointCloud/shaders/Sphere.vert"
pointProgram.fragmentShaderName = "pointCloud/shaders/Sphere.frag"
pointProgram.geometryShaderName = "pointCloud/shaders/Sphere.geom"
pointProgram.geometryOutVertices = 4
pointProgram.geometryInput = PrimitiveType.Points
pointProgram.geometryOutput = PrimitiveType.TriangleStrip
scene.addProgram(pointProgram)

pointScale = Uniform.create('pointScale', UniformType.Float, 1)
pointScale.setFloat(0.1)

pointCloudModel = ModelInfo()
pointCloudModel.name = 'pointCloud'
pointCloudModel.path = 'data.xyzb'
#pointCloudModel.options = "10000 100:1000000:5 20:100:4 6:20:2 0:5:1"
pointCloudModel.options = "10000 100:1000000:20 20:100:10 6:20:5 0:5:5"
#pointCloudModel.options = "10000 0:1000000:1"
scene.loadModel(pointCloudModel)

pointCloud = StaticObject.create(pointCloudModel.name)
pointCloud.setPosition(-15, 2, -5)
pointCloud.setScale(30, 100, 100)
# attach shader uniforms
mat = pointCloud.getMaterial()
mat.setProgram(pointProgram.name)
mat.attachUniform(pointScale)

getDefaultCamera().setPosition(0, 10, -35)
getDefaultCamera().lookAt(pointCloud.getBoundCenter(), Vector3(0,1,0))

pressure = getOrCreateCamera('press')
pressure.setHeadOffset(Vector3(0, 2, 0))

coutput = PixelData.create(250,250,PixelFormat.FormatRgba)
pressure.getOutput(0).setReadbackTarget(coutput)
pressure.getOutput(0).setEnabled(True)
uim = UiModule.createAndInitialize()
container = Container.create(ContainerLayout.LayoutVertical, uim.getUi())
container.setStyleValue('fill', 'black')
container.setPosition(Vector2(25, 25))
container.setAlpha(1)
img = Image.create(container)
img.setData(coutput)

pressure.setPosition(0, 10, 35)
pressure.lookAt(pointCloud.getBoundCenter(), Vector3(0,1,0))