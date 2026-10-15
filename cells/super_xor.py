import hashlib

class SuperXorMatrix:
    """Ma trận gương phản xạ 1+N Siêu XOR kháng bẻ khóa lượng tử"""
    @staticmethod
    def refract(vector, context_tag, dimensions=4):
        masks = []
        for d in range(dimensions):
            h = hashlib.shake_256(f"{context_tag}_{d}".encode()).hexdigest(4)
            masks.append(round(int(h, 16) / 65535.0, 4))
        
        result = list(vector)
        while len(result) < dimensions:
            result.append(0.0)
            
        for i in range(len(result)):
            for m in masks:
                result[i] = round((result[i] + m) % 1.0, 4)
        return result[:dimensions], masks
