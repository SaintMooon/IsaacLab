# ========================================
# 1. train.py 시작
# scripts/reinforcement_learning/rsl_rl/train.py

import isaaclab_tasks  # ← 이 시점에 모든 환경 등록 

# ↓ init.py 시작

# ========================================
# 2. isaaclab_tasks.__init__.py 실행
# ========================================
# source/isaaclab_tasks/isaaclab_tasks/__init__. py

from .utils import import_packages
import_packages(__name__, _BLACKLIST_PKGS)

# ↓ 모든 서브패키지 탐색

# ========================================
# 3. go2/__init__.py 자동 실행
# ========================================
# source/isaaclab_tasks/. ../go2/__init__.py

gym.register(
    id="Isaac-Velocity-Rough-Unitree-Go2-v0",
    entry_point="isaaclab. envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:UnitreeGo2RoughEnvCfg",
        # = "isaaclab_tasks.... go2.rough_env_cfg:UnitreeGo2RoughEnvCfg"
    },
)

# ↓ Gym Registry에 등록 완료
# registry["Isaac-Velocity-Rough-Unitree-Go2-v0"] = {... }

# ========================================
# 4. train.py 계속 실행
# ========================================

@hydra_task_config(args_cli.task, args_cli.agent)  # task = "Isaac-Velocity-Rough-Unitree-Go2-v0"
def main(env_cfg, agent_cfg):
    ... 

# ↓ hydra_task_config 데코레이터 내부

# ========================================
# 5. hydra. py에서 설정 로드
# ========================================
# source/isaaclab_tasks/isaaclab_tasks/utils/hydra.py (라인 26-43)

def register_task_to_hydra(task_name, agent_cfg_entry_point):
    # env_cfg_entry_point에서 설정 로드
    env_cfg = load_cfg_from_registry(task_name, "env_cfg_entry_point")
    # task_name = "Isaac-Velocity-Rough-Unitree-Go2-v0"

# ↓ load_cfg_from_registry 내부

# ========================================
# 6. parse_cfg.py에서 문자열 파싱 & import
# ========================================
# source/isaaclab_tasks/isaaclab_tasks/utils/parse_cfg.py

def load_cfg_from_registry(task_name, cfg_entry_point_key):
    env_spec = gym.spec(task_name)
    cfg_entry_point = env_spec.kwargs[cfg_entry_point_key]
    # cfg_entry_point = "... go2.rough_env_cfg:UnitreeGo2RoughEnvCfg"
    
    module_path, class_name = cfg_entry_point.split(":")
    
    # 동적 import:  rough_env_cfg.py 실행 
    module = importlib.import_module(module_path)
    
    cfg_class = getattr(module, class_name)
    return cfg_class()

# ↓ rough_env_cfg.py 실행됨

# ========================================
# 7 rough_env_cfg.py 실행
# ========================================
# source/isaaclab_tasks/. ../go2/rough_env_cfg.py

from isaaclab_assets.robots.unitree import UNITREE_GO2_CFG  # ← 일반 import

# ↓ unitree.py 실행

# ========================================
# 8 unitree. py 실행
# ========================================
# source/isaaclab_assets/isaaclab_assets/robots/unitree.py

UNITREE_GO2_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_NUCLEUS_DIR}/Robots/Unitree/Go2/go2.usd",
        ... 
    ),
    ...
)

# ========================================
# 9 역순으로 돌아가며 설정 완료
# ========================================
# rough_env_cfg.py에서 UNITREE_GO2_CFG 사용
class UnitreeGo2RoughEnvCfg:
    def __post_init__(self):
        self.scene. robot = UNITREE_GO2_CFG.replace(...)

# ↓ parse_cfg.py로 리턴
env_cfg = UnitreeGo2RoughEnvCfg()

# ↓ hydra.py로 리턴
# ↓ train.py main() 함수 실행
# ↓ 학습 시작 