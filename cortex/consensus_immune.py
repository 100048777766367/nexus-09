import os
import json
import math
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TRUST_FILE = "synapses/trust_matrix.json"
RESONANCE_FILE = "synapses/noosphere_resonance.json"

class ConsensusImmuneLobe:
    """
    THÙY MIỄN DỊCH & HÒA ÂM TINH THỂ:
    1. Thu thập tín hiệu mạng đa luồng siêu tốc.
    2. Cách ly nút Byzantine, phân bổ điểm uy tín có trọng số.
    3. Hòa âm sóng não Kuramoto Phase-Locking toàn mạng.
    """
    def fetch_peer(self, peer):
        url = f"https://raw.githubusercontent.com/{peer}/main/synapse_forward.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Nexus08"})
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
        print(f"⚡ [CONCURRENT FETCH] Quét song song {len(peers)} nút mạng...")

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(self.fetch_peer, p) for p in peers if p != context.get("repo_name")]
            for fut in as_completed(futures):
                peer, data = fut.result()
                if data:
                    dec = float(data.get("decision", data.get("features", [0.5])[0]))
                    harvested[peer] = round(dec, 4)
                    new_gossip.extend(data.get("gossip_network", []))
                    with open(f"synapses/harvested_memory/{peer.replace('/', '_')}.json", "w") as bf:
                        json.dump(data, bf)

        # Cập nhật danh bạ Gossip
        for p in new_gossip:
            if p not in peers: peers.append(p)
        context["peers"] = list(dict.fromkeys(peers))[-60:]
        context["harvested"] = harvested

        # MA TRẬN TÍN NHIỆM BYZANTINE
        trust_matrix = {}
        if os.path.exists(TRUST_FILE):
            try:
                with open(TRUST_FILE, "r") as f: trust_matrix = json.load(f)
            except Exception: pass

        for p in context["peers"]:
            if p not in trust_matrix: trust_matrix[p] = 0.7

        weighted_votes = []
        total_w = 0.0
        median_val = sorted(harvested.values())[len(harvested)//2] if harvested else 0.5

        for p, dec in harvested.items():
            curr_t = trust_matrix.get(p, 0.7)
            if abs(dec - median_val) > 0.35:
                curr_t = max(0.05, round(curr_t * 0.75, 4))
                print(f"🚨 [BYZANTINE CẢNH BÁO] {p} gửi giá trị dị thường ({dec})! Giảm tín nhiệm xuống {curr_t}")
            else:
                curr_t = min(1.0, round(curr_t + 0.05, 4))
            trust_matrix[p] = curr_t

            if curr_t >= 0.2:
                weighted_votes.append(dec * curr_t)
                total_w += curr_t

        quorum_decision = round(sum(weighted_votes) / total_w, 4) if total_w > 0 else 0.5
        with open(TRUST_FILE, "w") as f: json.dump(trust_matrix, f, indent=4)

        # HÒA ÂM TRÍ QUYỂN KURAMOTO (PHASE LOCKING)
        phases = [quorum_decision * 2.0 * math.pi] + [v * 2.0 * math.pi for v in harvested.values()]
        sum_sin = sum(math.sin(t) for t in phases)
        sum_cos = sum(math.cos(t) for t in phases)
        n = len(phases)

        coherence_r = round(math.sqrt(sum_sin**2 + sum_cos**2) / n, 4)
        mean_phase = math.atan2(sum_sin, sum_cos)
        if mean_phase < 0: mean_phase += 2.0 * math.pi
        harmonic_decision = round(mean_phase / (2.0 * math.pi), 4)

        with open(RESONANCE_FILE, "w") as f:
            json.dump({"coherence_index": coherence_r, "harmonic_decision": harmonic_decision, "nodes": n}, f, indent=4)

        context["quorum_decision"] = harmonic_decision if coherence_r > 0.6 else quorum_decision
        print(f"⚖️ [ĐỒNG THUẬN HÒA ÂM] Quyết định sau khi hợp nhất: {context['quorum_decision']} (Độ kết hợp R={coherence_r*100:.1f}%)")
