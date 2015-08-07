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

tempModel = ModelInfo()
tempModel.name = 'temp'
tempModel.path = 'data.xyzb'
##################################################
#pointCloudModel.options = "10000 100:1000000:5 20:100:4 6:20:2 0:5:1"
tempModel.options = "10000 100:1000000:20 20:100:10 6:20:5 0:5:5"

velModel = ModelInfo()
velModel.name = 'vel'
velModel.path = 'data2.xyzb'
velModel.options = "10000 100:1000000:20 20:100:10 6:20:5 0:5:5"

pressModel = ModelInfo()
pressModel.name = 'press'
pressModel.path = 'data3.xyzb'
pressModel.options = "10000 100:1000000:20 20:100:10 6:20:5 0:5:5"


#pointCloudModel.options = "10000 0:1000000:1"
scene.loadModel(tempModel)
scene.loadModel(velModel)
scene.loadModel(pressModel)

temp = StaticObject.create(tempModel.name)
temp.setPosition(-15, 0, -5)
temp.setScale(30, 100, 100)

vel = StaticObject.create(velModel.name)
vel.setPosition(-15, 0, -5)
vel.setScale(30, 100, 100)

press = StaticObject.create(pressModel.name)
press.setPosition(-15, 0, -5)
press.setScale(30, 100, 100)

# attach shader uniforms
mat = temp.getMaterial()
mat.setProgram(pointProgram.name)
mat.attachUniform(pointScale)

mat2 = vel.getMaterial()
mat2.setProgram(pointProgram.name)
mat2.attachUniform(pointScale)

mat3 = press.getMaterial()
mat3.setProgram(pointProgram.name)
mat3.attachUniform(pointScale)

getDefaultCamera().setPosition(0, 7, 30)
getDefaultCamera().lookAt(temp.getBoundCenter(), Vector3(0,1,0))
getDefaultCamera().getController().setSpeed(10.0)

def change(model):
    if model == 'temp':
        temp.setVisible(True)
        vel.setVisible(False)
        press.setVisible(False)
    elif model == 'vel':
        temp.setVisible(False)
        vel.setVisible(True)
        press.setVisible(False)
    elif model == 'press':
        temp.setVisible(False)
        vel.setVisible(False)
        press.setVisible(True)

def onEvent():
    e = getEvent()
    if e.isKeyDown(ord('m')):
        if menu.isVisible():
            menu.hide()
        else:
            menu.show()

setEventFunction(onEvent)

mm = MenuManager.createAndInitialize()
menu = mm.getMainMenu()
changeVar = menu.addSubMenu('Change Variable')
changeVar.addButton('Temperature', 'change("temp")')
changeVar.addButton('Velocity', 'change("vel")')
changeVar.addButton('Pressure', 'change("press")')