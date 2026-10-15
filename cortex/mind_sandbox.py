import os
import json
import re
import random
from cells.neuron import AtomNeuron, sigmoid_derivative
from cells.super_xor import SuperXorMatrix

GRAPH_FILE = "synapses/knowledge_graph.json"

class MindSandboxLobe:
    """
    THÙY TÂM THỨC & NHÂN QUẢ TINH THỂ:
    1. Trích xuất Bộ ba biểu tượng (Knowledge Graph).
    2. Chạy phòng giả lập What-If 5 kịch bản tương lai.
    3. Giấc mơ số REM Sleep khi môi trường nhàn rỗi.
    4. Huấn luyện bầy nơ-ron qua Ma trận Siêu XOR.
    """
    def __init__(self, num_cells=8):
        self.num_cells = num_cells
        self.swarm = [AtomNeuron(f"n08_h_{i}", n_inputs=4, n_super_xor=4) for i in range(num_cells)]
        self.out_cell = AtomNeuron("n08_out", n_inputs=num_cells, n_super_xor=4)

    def extract_graph(self, text):
        triplets = []
        for s in re.split(r'[.\n]', text):
            words = [w.strip() for w in s.split() if len(w.strip()) > 2]
            if len(words) >= 3:
                triplets.append({"subject": words[0].capitalize(), "predicate": words[1].lower(), "object": " ".join(words[2:4])})
        
        graph = {"nodes": [], "edges": []}
        if os.path.exists(GRAPH_FILE):
            try:
                with open(GRAPH_FILE, "r") as f: graph = json.load(f)
            except Exception: pass

        for t in triplets[:5]:
            if t["subject"] not in graph["nodes"]: graph["nodes"].append(t["subject"])
            if t["object"] not in graph["nodes"]: graph["nodes"].append(t["object"])
            edge = f"{t['subject']} --[{t['predicate']}]--> {t['object']}"
            if edge not in graph["edges"]: graph["edges"].append(edge)

        graph["nodes"] = graph["nodes"][-100:]
        graph["edges"] = graph["edges"][-150:]
        os.makedirs("synapses", exist_ok=True)
        with open(GRAPH_FILE, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=4, ensure_ascii=False)

    def simulate_what_if(self, raw_decision):
        variations = [0.85, 0.95, 1.0, 1.05, 1.15]
        sims = []
        for factor in variations:
            cand = max(0.01, min(0.99, round(raw_decision * factor, 4)))
            loss = round((abs(cand - 0.5) * 0.5) + ((1.0 - cand) * 0.5), 4)
            sims.append((loss, cand))
        sims.sort(key=lambda x: x[0])
        return sims[0][1]

    def dream_rem_sleep(self, current_decision):
        mem_dir = "synapses/harvested_memory"
        if not os.path.exists(mem_dir): return current_decision
        files = [f for f in os.listdir(mem_dir) if f.endswith(".json")]
        if not files: return current_decision
        try:
            with open(os.path.join(mem_dir, random.choice(files)), "r") as f:
                past = float(json.load(f).get("decision", 0.5))
            recalled = round((current_decision * 0.8) + (past * 0.2), 4)
            print(f"🌙 [GIẤC MƠ REM] Chiêm nghiệm ký ức cũ: {past} ──► Điều biến: {recalled}")
            return recalled
        except Exception:
            return current_decision

    def process(self, context):
        self.extract_graph(context.get("wisdom_text", ""))
        v_wisdom = context.get("wisdom_vector", [0.5, 0.5, 0.5, 0.5])
        q_dec = context.get("quorum_decision", 0.5)

        # Hợp nhất qua Siêu XOR
        super_vec = [v_wisdom[0], v_wisdom[1], q_dec, round(1.0 - q_dec, 4)]
        entangled, masks = SuperXorMatrix.refract(super_vec, "nexus08_crystalline")

        # Lan truyền tiến
        h_outs = [cell.forward(entangled) for cell in self.swarm]
        internal_pred = self.out_cell.forward(h_outs)
        raw_decision = round((internal_pred + q_dec) / 2.0, 4)

        # Thử nghiệm What-If & Giấc mơ số nếu mạng tĩnh
        sandboxed_dec = self.simulate_what_if(raw_decision)
        if not context.get("harvested"):
            sandboxed_dec = self.dream_rem_sleep(sandboxed_dec)

        # Lan truyền ngược tự sửa sai
        target = 1.0 if super_vec[0] > super_vec[1] else 0.0
        delta_out = (target - sandboxed_dec) * sigmoid_derivative(sandboxed_dec)
        deltas_h = [delta_out * self.out_cell.weights[j] * sigmoid_derivative(h_outs[j]) for j in range(self.num_cells)]

        self.out_cell.backward(delta_out)
        for j, cell in enumerate(self.swarm): cell.backward(deltas_h[j])

        grad_backward = [
            round(sum(deltas_h[j] * self.swarm[j].weights[0] for j in range(self.num_cells)), 4),
            round(sum(deltas_h[j] * self.swarm[j].weights[1] for j in range(self.num_cells)), 4)
        ]

        context["final_decision"] = sandboxed_dec
        context["grad_backward"] = grad_backward
        context["super_xor_masks"] = masks
        context["swarm_weights"] = [c.weights for c in self.swarm]
        print(f"🔮 [TÂM THỨC NHÂN QUẢ] Phán quyết sau Giả lập & Siêu XOR: {sandboxed_dec}")
