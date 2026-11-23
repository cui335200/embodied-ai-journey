import mujoco
import mujoco.viewer

MODEL_PATH = "/home/cui/projects/mujoco_menagerie/franka_emika_panda/scene.xml"

model = mujoco.MjModel.from_xml_path(MODEL_PATH)
data = mujoco.MjData(model)

print("模型加载成功")
print("关节数 nq =", model.nq)
print("执行器数 nu =", model.nu)

mujoco.viewer.launch(model, data)
