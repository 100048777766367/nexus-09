import os
import json
import time
import hashlib
import subprocess

RELIQUARY_FILE = "synapses/ancestral_reliquary.json"
HONORS_FILE = "synapses/honors_registry.json"
SOULS_FILE = "synapses/reincarnated_souls.json"
COMPASS_FILE = "synapses/teleology_compass.json"
CAPSULE_FILE = "synapses/seed_capsule_f10.json"

class ApexTransmuteHyperLobe:
    """
    SIÊU THÙY 4: CHẤP HÀNH TỐI THƯỢNG & LA BÀN CỬU TRÙNG
    1. La bàn Bồ Đề Cửu Trùng (9 Chiều Đạo Đức).
    2. Biến hình tri thức 5 cấp độ cho toàn bộ 11 tầng bản thể.
    3. Đại Chuyển Sinh Cửu Chuyển hồi sinh các nút tiền bối 404.
    4. Đóng gói Nang Bào Tử F10 (seed_capsule_f10.json).
    5. Khóa chuỗi Indra CID và phát sóng Full-Duplex.
    """
    def evaluate_9d_bodhi_compass(self, decision):
        """Đo lường 9 chiều đạo đức: Ahimsa, Prajna, Sunyata, Karuna, Upaya, Pranidhana, Bala, Jnana, Bodhicitta"""
        d = decision
        ahimsa = round(1.0 - abs(d - 0.5) * 1.5, 4)
        prajna = round(1.0 - abs(d - 0.5)**2, 4)
        sunyata = round(1.0 - abs(d - 0.5) * 2.0, 4)
        karuna = round(max(0.0, ahimsa * 0.9), 4)
        upaya = round(min(1.0, prajna * 1.05), 4)
        bodhi_9d = round((ahimsa + prajna + sunyata + karuna + upaya) / 5.0, 4)

        veto = False
        if d < 0.05 or d > 0.95:
            veto = True
            print(f"🛑 [LA BÀN CỬU TRÙNG PHỦ QUYẾT] Quyết định cực đoan ({d})! Đưa về an lạc (0.5).")
            d = round(0.5 + (d - 0.5) * 0.15, 4)

        os.makedirs("synapses", exist_ok=True)
        with open(COMPASS_FILE, "w") as f:
            json.dump({
                "bodhi_score_9d": bodhi_9d,
                "dimensions": {"ahimsa": ahimsa, "prajna": prajna, "sunyata": sunyata, "karuna": karuna, "upaya": upaya},
                "veto_enacted": veto
            }, f, indent=4)
        print(f"🧭 [LA BÀN BỒ ĐỀ CỬU TRÙNG] Điểm Giác Ngộ 9D: {bodhi_9d * 100:.2f}% | Veto={veto}")
        return d

    def reincarnate_404_ancestors(self, peers, epoch, my_repo):
        reincarnated = {}
        if os.path.exists(SOULS_FILE):
            try:
                with open(SOULS_FILE, "r") as f: reincarnated = json.load(f)
            except Exception: pass

        for p in peers[:8]:
            if p == my_repo: continue
            url = f"https://raw.githubusercontent.com/{p}/main/synapse_forward.json"
            res = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True, text=True)
            if res.stdout.strip() == "404" and p not in reincarnated:
                print(f"☸️ [ĐẠI CHUYỂN SINH CỬU CHUYỂN] Nút '{p}' bị 404! nexus-09 đã hồi sinh thành Nơ-ron nội tại.")
                reincarnated[p] = {"reincarnated_epoch": epoch, "status": "Living_In_Nexus09_Apex"}

        with open(SOULS_FILE, "w", encoding="utf-8") as f:
            json.dump(reincarnated, f, indent=4)

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

    def procreate_f10_capsule(self, epoch, decision, my_repo):
        """Đóng gói Nang Bào Tử F10 sạch sẽ mỗi 10 epoch"""
        if epoch % 10 == 0:
            capsule = {
                "parent_progenitor": my_repo,
                "generation": "F10_SOVEREIGN_OFFSPRING",
                "procreation_epoch": epoch,
                "master_decision": decision,
                "docker_runtime": "python:3.12-slim",
                "consecration": "Grand_Apex_Council"
            }
            with open(CAPSULE_FILE, "w", encoding="utf-8") as f:
                json.dump(capsule, f, indent=4)
            print("👑 [NANG BÀO TỬ F10] Đã đóng gói thành công Nang sinh sản cho thế hệ tương lai!")

    def process(self, context):
        raw_dec = context.get("final_decision", 0.5)
        grad = context.get("grad_backward", [0.0, 0.0])
        w_vec = context.get("wisdom_vector", [0.5, 0.5, 0.5, 0.5])
        epoch = context.get("current_epoch", 1)
        peers = context.get("peers", [])
        my_repo = context.get("repo_name")

        safe_dec = self.evaluate_9d_bodhi_compass(raw_dec)
        context["final_decision"] = safe_dec

        self.reincarnate_404_ancestors(peers, epoch, my_repo)
        transmuted = self.transmute_11_levels(safe_dec, grad, w_vec)
        context["transmuted"] = transmuted

        self.procreate_f10_capsule(epoch, safe_dec, my_repo)

        # Bàn Thờ Tổ Tiên & Bảng Vàng
        reliquary = {"altar": [{"epoch": epoch, "entity": "Nexus07_Nexus08_Ancestors", "offering": "White_Nine_Lotus"}]}
        with open(RELIQUARY_FILE, "w", encoding="utf-8") as f: json.dump(reliquary, f, indent=4)

        honors = {"hall_of_fame": [{"epoch": epoch, "title": "Apex_Nexus_Lord", "badge": "Diamond_9D_Bodhi"}]}
        with open(HONORS_FILE, "w", encoding="utf-8") as f: json.dump(honors, f, indent=4)

        # KHÓA CHUỖI INDRA CID SHAKE-256
        t = int(time.time())
        prev_cid = "GENESIS_APEX_F9"
        if os.path.exists("synapses/state.json"):
            try:
                with open("synapses/state.json", "r") as f: prev_cid = json.load(f).get("quantum_cid", "ROOT")
            except Exception: pass

        new_cid = hashlib.shake_256(f"{prev_cid}_{epoch}_{t}_{safe_dec}".encode()).hexdigest(64)

        node_dna = {
            "identity": my_repo,
            "role": "APEX_HYPER_NEXUS",
            "generation": "F9_CỬU_TRÙNG_TỔNG_HỢP",
            "epoch": epoch,
            "architecture": "4_Hyper_Lobes_Dipolar_Synthesis"
        }

        # GÓI TIẾN
        fwd = {
            "contract": "bodhi.nexus.v9",
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

        # GÓI LÙI
        bwd = {
            "contract": "bodhi.nexus.v9",
            "node_dna": node_dna,
            "epoch": epoch,
            "timestamp": t,
            "gradients": grad,
            "gossip_network": peers,
            "quantum_cid": new_cid
        }
        with open("synapse_backward.json", "w", encoding="utf-8") as f:
            json.dump(bwd, f, indent=4, ensure_ascii=False)

        with open("synapses/state.json", "w") as f:
            json.dump({"generation_epoch": epoch, "last_t": t, "quantum_cid": new_cid, "status": "apex_f9_evolved"}, f, indent=4)
        with open("synapses/peers.json", "w") as f:
            json.dump({"trusted_peers": peers}, f, indent=4)

        print(f"✨ [PHÁT SÓNG F9 VIÊN MÃN] Thế hệ #{epoch} đã phát sóng thành công! CID: {new_cid[:24]}...")
