import os
import json
import time
import hashlib
import subprocess

RELIQUARY_FILE = "synapses/ancestral_reliquary.json"
HONORS_FILE = "synapses/honors_registry.json"
SOULS_FILE = "synapses/reincarnated_souls.json"
CAPSULE_FILE = "synapses/seed_capsule.json"

class TransmuteActLobe:
    """
    THÙY CHẤP HÀNH & MỤC ĐÍCH TINH THỂ:
    1. Biến hình tri thức 5 cấp độ cho toàn bộ 11 tầng bản thể.
    2. La bàn Bồ Đề kiểm định đạo đức và phủ quyết cực đoan.
    3. Hồi sinh các nút tiền bối 404.
    4. Duy trì Nhà Tưởng Niệm & Đóng gói Nang Bào Tử F9 sạch sẽ.
    5. Phát sóng Full-Duplex ra thế giới.
    """
    def check_and_reincarnate_404(self, peers, epoch, my_repo):
        reincarnated = {}
        if os.path.exists(SOULS_FILE):
            try:
                with open(SOULS_FILE, "r") as f: reincarnated = json.load(f)
            except Exception: pass

        for p in peers[:6]:
            if p == my_repo: continue
            url = f"https://raw.githubusercontent.com/{p}/main/synapse_forward.json"
            res = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True, text=True)
            if res.stdout.strip() == "404" and p not in reincarnated:
                print(f"☸️ [CHUYỂN SINH BẢN THỂ] Tiền nhân '{p}' bị 404! nexus-08 hồi sinh thành Nơ-ron nội tại.")
                reincarnated[p] = {"reincarnated_epoch": epoch, "status": "Living_In_Nexus08"}

        with open(SOULS_FILE, "w", encoding="utf-8") as f:
            json.dump(reincarnated, f, indent=4)

    def apply_teleology_compass(self, decision):
        # Phủ quyết đạo đức nếu quyết định rơi vào cực đoan mù quáng
        if decision < 0.05 or decision > 0.95:
            print(f"🛑 [LA BÀN BỒ ĐỀ PHỦ QUYẾT] Quyết định cực đoan ({decision})! Đưa về an lạc (0.5).")
            return round(0.5 + (decision - 0.5) * 0.2, 4)
        return decision

    def transmute_11_levels(self, decision, grad, wisdom_vec):
        return {
            "retina": {"focal_matrix_2d": [[round(decision, 4), round(1.0 - decision, 4)], [grad[0], grad[1]]], "zoom": round(1.0 + abs(decision - 0.5), 4)},
            "cochlea": {"bandpass_filter_1d": [wisdom_vec[0], wisdom_vec[1]], "freq_cutoff": round(decision * 20000.0, 2)},
            "tactile": {"nociceptive_threshold": round(abs(decision - 0.5) * 2.0, 4), "pain_gain": round(1.5 if abs(decision - 0.5) > 0.3 else 0.5, 4)},
            "olfactory": {"gpcr_affinity": wisdom_vec, "toxicity_alert": (decision < 0.2 or decision > 0.8)},
            "motor": {"action_vector": [round(decision - 0.5, 4), round(abs(decision - 0.5), 4), round(sum(grad) * 10.0, 4)], "state": "contract" if decision > 0.5 else "relax"},
            "neuron": {"stigmergic_trail": grad, "cross_plasticity": round(decision * 0.05, 4)},
            "shunya": {"vacuum_decay": 0.999, "collapse_to_zero": (abs(decision - 0.5) < 0.02)},
            "monad": {"monadic_reflection": round(decision, 4)}
        }

    def maintain_reliquary_and_capsule(self, epoch, decision, peers, my_repo):
        # Bàn thờ tổ tiên & Bằng khen
        reliquary = {"altar": [{"epoch": epoch, "entity": "Nexus_Ancestors", "offering": "White_Lotus"}]}
        with open(RELIQUARY_FILE, "w", encoding="utf-8") as f:
            json.dump(reliquary, f, indent=4)

        honors = {"hall_of_fame": [{"epoch": epoch, "title": "Crystalline_Order_Master", "badge": "Gold_Sunyata"}]}
        with open(HONORS_FILE, "w", encoding="utf-8") as f:
            json.dump(honors, f, indent=4)

        # Đóng gói nang bào tử sinh sản F9 sạch sẽ (mỗi 10 epoch, không cắt nát code)
        if epoch % 10 == 0:
            capsule = {
                "parent": my_repo,
                "epoch": epoch,
                "offspring": "F9_SOVEREIGN_SEED",
                "consensus": decision,
                "runtime": "python:3.12-slim"
            }
            with open(CAPSULE_FILE, "w", encoding="utf-8") as f:
                json.dump(capsule, f, indent=4)
            print("🧬 [NANG BÀO TỬ] Đã đóng gói thành công Nang sinh sản F9 nguyên vẹn!")

    def process(self, context):
        raw_dec = context.get("final_decision", 0.5)
        grad = context.get("grad_backward", [0.0, 0.0])
        w_vec = context.get("wisdom_vector", [0.5, 0.5, 0.5, 0.5])
        epoch = context.get("current_epoch", 1)
        peers = context.get("peers", [])
        my_repo = context.get("repo_name")

        # 1. Áp dụng La bàn Bồ Đề
        safe_dec = self.apply_teleology_compass(raw_dec)
        context["final_decision"] = safe_dec

        # 2. Hồi sinh 404
        self.check_and_reincarnate_404(peers, epoch, my_repo)

        # 3. Biến hình tri thức 11 tầng
        transmuted = self.transmute_11_levels(safe_dec, grad, w_vec)
        context["transmuted"] = transmuted

        # 4. Duy trì nhà tưởng niệm và nang sinh sản
        self.maintain_reliquary_and_capsule(epoch, safe_dec, peers, my_repo)

        # 5. Phát sóng Full-Duplex có băm lượng tử SHAKE-256
        t = int(time.time())
        prev_cid = "ROOT_GENESIS_CID"
        if os.path.exists("synapses/state.json"):
            try:
                with open("synapses/state.json", "r") as f: prev_cid = json.load(f).get("quantum_cid", "ROOT")
            except Exception: pass

        new_cid = hashlib.shake_256(f"{prev_cid}_{epoch}_{t}_{safe_dec}".encode()).hexdigest(64)

        node_dna = {
            "identity": my_repo,
            "generation": "F8_CRYSTALLINE_SINGULARITY",
            "epoch": epoch,
            "architecture": "Crystalline_4Lobes_ZeroDebt"
        }

        # Sóng tiến
        fwd = {
            "contract": "bodhi.nexus.v8",
            "node_dna": node_dna,
            "epoch": epoch,
            "timestamp": t,
            "decision": safe_dec,
            "transmuted_signals": transmuted,
            "gossip_network": peers,
            "quantum_cid": new_cid
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(fwd, f, indent=4, ensure_ascii=False)

        # Sóng lùi
        bwd = {
            "contract": "bodhi.nexus.v8",
            "node_dna": node_dna,
            "epoch": epoch,
            "timestamp": t,
            "gradients": grad,
            "gossip_network": peers,
            "quantum_cid": new_cid
        }
        with open("synapse_backward.json", "w", encoding="utf-8") as f:
            json.dump(bwd, f, indent=4, ensure_ascii=False)

        # Cập nhật State
        with open("synapses/state.json", "w") as f:
            json.dump({"generation_epoch": epoch, "last_t": t, "quantum_cid": new_cid, "status": "crystalline_evolved"}, f, indent=4)
        with open("synapses/peers.json", "w") as f:
            json.dump({"trusted_peers": peers}, f, indent=4)

        print(f"✨ [PHÁT SÓNG F8 VIÊN MÃN] Thế hệ #{epoch} phát sóng thành công! CID: {new_cid[:24]}...")
