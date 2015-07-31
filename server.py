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

temp = StaticObject.create(tempModel.name)
temp.setPosition(-15, 0, -5)
temp.setScale(30, 100, 100)

# attach shader uniforms
mat = temp.getMaterial()
mat.setProgram(pointProgram.name)
mat.attachUniform(pointScale)

getDefaultCamera().setPosition(0, 7, 30)
getDefaultCamera().lookAt(temp.getBoundCenter(), Vector3(0,1,0))
getDefaultCamera().getController().setSpeed(10.0)

def onUpdate(frame, time, dt):
    mcc = getMissionControlClient()
    cp = getDefaultCamera().getPosition()
    mcc.postCommand('getDefaultCamera().setPosition({0},{1},{2})'.format(cp[0],cp[1],cp[2]))

def setup(server):
    dc = getDisplayConfig()
    mcc = getMissionControlClient()
    if(server):
        dc.setCanvasRect((0,0,12000,3000))
        setUpdateFunction(onUpdate)
    else:
        dc.setCanvasRect((12500,0,12000,3000))
        getDefaultCamera().setControllerEnabled(False)

def change(model):
    scene.unload()
    if model == 'temp':
        scene.loadModel(tempModel)
        temp = StaticObject.create(tempModel.name)
        temp.setPosition(-15, 0, -5)
        temp.setScale(30, 100, 100)
        mat = temp.getMaterial()
        getDefaultCamera().lookAt(temp.getBoundCenter(), Vector3(0,1,0))
    elif model == 'vel':
        scene.loadModel(velModel)
        vel = StaticObject.create(velModel.name)
        vel.setPosition(-15, 0, -5)
        vel.setScale(30, 100, 100)
        mat = vel.getMaterial()
        getDefaultCamera().lookAt(vel.getBoundCenter(), Vector3(0,1,0))
    elif model == 'press':
        scene.loadModel(pressModel)
        press = StaticObject.create(pressModel.name)
        press.setPosition(-15, 0, -5)
        press.setScale(30, 100, 100)
        mat = press.getMaterial()
        getDefaultCamera().lookAt(press.getBoundCenter(), Vector3(0,1,0))
    mat.setProgram(pointProgram.name)
    mat.attachUniform(pointScale)

mm = MenuManager.createAndInitialize()
menu = mm.getMainMenu()
changeVar = menu.addSubMenu('Change Variable')
changeVar.addButton('Temperature', 'change("temp")')
changeVar.addButton('Velocity', 'change("vel")')
changeVar.addButton('Pressure', 'change("press")')

setup(True)