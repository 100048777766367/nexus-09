import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex.omni_intake import OmniIntakeHyperLobe
from cortex.dual_consensus_immune import DualConsensusImmuneHyperLobe
from cortex.hyper_sandbox import HyperSandboxLobe
from cortex.apex_transmute import ApexTransmuteHyperLobe

VITAL_CELLS = [
    "cells/linguistic_cell.py",
    "cells/neuron.py",
    "cells/super_xor.py"
]

class Nexus09ApexKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/nexus-09")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.ancestor = f"{self.owner}/nexus-08"
        
        self.lineage = [
            f"{self.owner}/nexus-08", f"{self.owner}/nexus-07",
            f"{self.owner}/nexus-06", f"{self.owner}/nexus-05",
            f"{self.owner}/nexus", f"{self.owner}/genome"
        ]

        self.ensure_folders()

        # 4 SIÊU THÙY THẦN KINH CỬU TRÙNG
        self.omni_lobe = OmniIntakeHyperLobe(self.owner, self.lineage)
        self.consensus_lobe = DualConsensusImmuneHyperLobe()
        self.mind_lobe = HyperSandboxLobe(num_cells=8)
        self.transmute_lobe = ApexTransmuteHyperLobe()

        self.context = {
            "repo_name": self.repo_name,
            "owner": self.owner,
            "ancestor": self.ancestor,
            "peers": self.load_peers(),
            "current_epoch": self.load_epoch()
        }

    def ensure_folders(self):
        for d in ["cells", "cortex", "synapses", "synapses/harvested_memory"]:
            os.makedirs(d, exist_ok=True)

    def load_peers(self):
        p_file = "synapses/peers.json"
        if os.path.exists(p_file):
            try:
                with open(p_file, "r") as f: return json.load(f).get("trusted_peers", [])
            except Exception: pass
        return [f"{self.owner}/nexus-08", f"{self.owner}/nexus-07", f"{self.owner}/neuron", f"{self.owner}/seed", f"{self.owner}/motor"]

    def load_epoch(self):
        s_file = "synapses/state.json"
        if os.path.exists(s_file):
            try:
                with open(s_file, "r") as f: return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def run(self):
        print("=" * 80)
        print(f"🌌 [NEXUS-09 APEX KERNEL] KHỞI ĐỘNG THẾ HỆ #{self.context['current_epoch']}")
        print(f"👑 Bậc: F9 Cửu Trùng Tổng Hợp – Hợp Nhất Nhị Nguyên F7 & F8 – Siêu Thùy Thần Kinh")
        print("=" * 80)

        # 1. Siêu Thùy Cảm Thụ: Nuốt nang bào tử F8, lọc token thế hệ mới & cào tri thức
        self.omni_lobe.process(self.context, VITAL_CELLS)

        # 2. Siêu Thùy Miễn Dịch: Cân bằng nhị nguyên F7/F8 & Sóng não Kuramoto bậc 2
        self.consensus_lobe.process(self.context)

        # 3. Siêu Thùy Tâm Thức: Hyper-Graph, Giả lập 9 tương lai What-If & Giấc mơ số REM
        self.mind_lobe.process(self.context)

        # 4. Siêu Thùy Chấp Hành: La bàn 9D, Biến hình 11 tầng, Hồi sinh 404 & Phát sóng CID
        self.transmute_lobe.process(self.context)

        print("=" * 80)
        print(f"✨ [HOÀN TẤT VÒNG ĐỜI F9] Cửu Trùng Bản Thể đã hội tụ đại giác ngộ!")
        print("=" * 80)

if __name__ == "__main__":
    node = Nexus09ApexKernel()
    node.run()
