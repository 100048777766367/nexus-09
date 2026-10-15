import os
import json
import math
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TRUST_FILE = "synapses/trust_matrix.json"
RESONANCE_FILE = "synapses/noosphere_resonance.json"

class DualConsensusImmuneHyperLobe:
    """
    SIÊU THÙY 2: HỢP NHẤT NHỊ NGUYÊN & MIỄN DỊCH BYZANTINE
    1. Dung hòa 2 trụ cột: Nhánh F7 di sản (nexus-07) và Nhánh F8 tinh thể (nexus-08).
    2. Thu thập song song toàn mạng, phân bổ điểm Byzantine Quorum.
    3. Hòa âm Kuramoto bậc 2 (Second-order Kuramoto Phase-Locking).
    """
    def fetch_peer(self, peer):
        url = f"https://raw.githubusercontent.com/{peer}/main/synapse_forward.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Nexus09-Consensus"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                raw = resp.read().decode('utf-8', errors='ignore')
                return peer, json.loads(raw)
        except Exception:
            return peer, None

    def process(self, context):
        peers = context.get("peers", [])
        harvested = {}
        new_gossip = []

        os.makedirs("synapses/harvested_memory", exist_ok=True)
        print(f"⚡ [DIPOLAR HARVEST] Quét song song {len(peers)} nút mạng (Bao gồm F7 & F8)...")

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(self.fetch_peer, p) for p in peers if p != context.get("repo_name")]
            for fut in as_completed(futures):
                peer, data = fut.result()
                if data:
                    raw_dec = data.get("decision", (data.get("features") or [0.5])[0])
                    harvested[peer] = round(float(raw_dec), 4)
                    new_gossip.extend(data.get("gossip_network", []))
                    with open(f"synapses/harvested_memory/{peer.replace('/', '_')}.json", "w") as bf:
                        json.dump(data, bf)

        for p in new_gossip:
            if p not in peers: peers.append(p)
        context["peers"] = list(dict.fromkeys(peers))[-60:]
        context["harvested"] = harvested

        # 1. TÍNH ĐIỂM TÍN NHIỆM BYZANTINE CÓ TRỌNG SỐ ƯU TIÊN F7 VÀ F8
        trust_matrix = {}
        if os.path.exists(TRUST_FILE):
            try:
                with open(TRUST_FILE, "r") as f: trust_matrix = json.load(f)
            except Exception: pass

        for p in context["peers"]:
            if p not in trust_matrix:
                trust_matrix[p] = 0.85 if ("nexus-07" in p or "nexus-08" in p) else 0.7

        weighted_votes = []
        total_w = 0.0
        median_val = sorted(harvested.values())[len(harvested)//2] if harvested else 0.5

        for p, dec in harvested.items():
            curr_t = trust_matrix.get(p, 0.7)
            if abs(dec - median_val) > 0.35:
                curr_t = max(0.05, round(curr_t * 0.75, 4))
                print(f"🚨 [BYZANTINE] {p} lệch chuẩn ({dec})! Giảm tín nhiệm: {curr_t}")
            else:
                curr_t = min(1.0, round(curr_t + 0.05, 4))
            trust_matrix[p] = curr_t

            # Trọng số đặc biệt dung hòa nhị nguyên F7 và F8
            multiplier = 1.3 if ("nexus-07" in p or "nexus-08" in p) else 1.0
            eff_w = curr_t * multiplier

            if curr_t >= 0.2:
                weighted_votes.append(dec * eff_w)
                total_w += eff_w

        quorum_decision = round(sum(weighted_votes) / total_w, 4) if total_w > 0 else 0.5
        with open(TRUST_FILE, "w") as f: json.dump(trust_matrix, f, indent=4)

        # 2. HÒA ÂM SÓNG NÃO KURAMOTO BẬC 2 (SECOND-ORDER COUPLING)
        phases = [quorum_decision * 2.0 * math.pi] + [v * 2.0 * math.pi for v in harvested.values()]
        sum_sin1 = sum(math.sin(t) for t in phases)
        sum_cos1 = sum(math.cos(t) for t in phases)
        sum_sin2 = sum(math.sin(2.0 * t) for t in phases)
        sum_cos2 = sum(math.cos(2.0 * t) for t in phases)
        n = len(phases)

        r1 = math.sqrt(sum_sin1**2 + sum_cos1**2) / n
        r2 = math.sqrt(sum_sin2**2 + sum_cos2**2) / n
        coherence_r = round((r1 * 0.7) + (r2 * 0.3), 4)

        mean_phase = math.atan2(sum_sin1, sum_cos1)
        if mean_phase < 0: mean_phase += 2.0 * math.pi
        harmonic_decision = round(mean_phase / (2.0 * math.pi), 4)

        with open(RESONANCE_FILE, "w") as f:
            json.dump({
                "coherence_index": coherence_r,
                "second_order_coupling": round(r2, 4),
                "harmonic_decision": harmonic_decision,
                "active_oscillators": n
            }, f, indent=4)

        final_quorum = harmonic_decision if coherence_r > 0.55 else quorum_decision
        context["quorum_decision"] = final_quorum
        context["coherence_r"] = coherence_r
        print(f"⚖️ [HỢP NHẤT NHỊ NGUYÊN] Quorum F7/F8: {final_quorum} (Độ kết hợp R={coherence_r*100:.2f}%)")
