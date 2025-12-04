from typing import List, Tuple
import math
import heapq

# 型別別名
Point3D = Tuple[float, float, float]

# ========== 1. 基本支配關係與暴力法 skyline ==========

def dominates(p: Point3D, q: Point3D) -> bool:
    """回傳 p 是否支配 q（所有維度 <=，且至少一維 <）"""
    le_all = all(pi <= qi for pi, qi in zip(p, q))
    lt_any = any(pi < qi for pi, qi in zip(p, q))
    return le_all and lt_any


def brute_force_skyline_with_id(points_with_id):
    skyline = []
    n = len(points_with_id)
    for i in range(n):
        id_i, p = points_with_id[i]
        dominated = False
        for j in range(n):
            if i == j:
                continue
            id_j, q = points_with_id[j]
            if dominates(q, p):
                dominated = True
                break
        if not dominated:
            skyline.append((id_i, p))
    return skyline

# ========== 2. 讀取 point.txt ==========

def load_points_from_file(path: str):
    result = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # 假設第一行是 header: id A1 A2 A3
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) != 4:
            continue
        pid = parts[0]
        x, y, z = map(float, parts[1:])
        result.append((pid, (x, y, z)))
    return result

# ========== 3. 簡易 3D R-tree 結構 ==========

class MBR3D:
    def __init__(self, low, high):
        self.low = list(low)    # [min_x, min_y, min_z]
        self.high = list(high)  # [max_x, max_y, max_z]

    @staticmethod
    def from_point(p: Point3D):
        return MBR3D(p, p)

    def expand_to_include(self, other: "MBR3D"):
        for i in range(3):
            self.low[i] = min(self.low[i], other.low[i])
            self.high[i] = max(self.high[i], other.high[i])

    def mindist_to_origin(self) -> float:
        # 假設座標皆為正，對原點的最小距離就是 low 向量長度
        x, y, z = self.low
        return math.sqrt(x * x + y * y + z * z)

class RTreeNode:
    def __init__(self, is_leaf: bool):
        self.is_leaf = is_leaf
        self.children = []   # if leaf: List[(id, Point3D)]；else: List[RTreeNode]
        self.mbr: MBR3D | None = None

    def recompute_mbr(self):
        mbr = None
        if self.is_leaf:
            for _, p in self.children:
                pmbr = MBR3D.from_point(p)
                if mbr is None:
                    mbr = pmbr
                else:
                    mbr.expand_to_include(pmbr)
        else:
            for child in self.children:
                if mbr is None:
                    mbr = MBR3D(child.mbr.low, child.mbr.high)
                else:
                    mbr.expand_to_include(child.mbr)
        self.mbr = mbr

def bulk_load_rtree(points_with_id, max_children=3) -> RTreeNode:
    # 這裡用最簡單的 bulk-load：依 A1 排序後分組成葉節點
    points_sorted = sorted(points_with_id, key=lambda x: x[1][0])
    leaves = []
    for i in range(0, len(points_sorted), max_children):
        node = RTreeNode(is_leaf=True)
        node.children = points_sorted[i:i + max_children]
        node.recompute_mbr()
        leaves.append(node)

    # 自底向上做成一棵樹
    level = leaves
    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), max_children):
            node = RTreeNode(is_leaf=False)
            node.children = level[i:i + max_children]
            node.recompute_mbr()
            next_level.append(node)
        level = next_level
    return level[0]  # root

# ========== 4. 用 R-tree 做 skyline (BBS-style) ==========

def dominated_by_skyline(p: Point3D, skyline_points: List[Point3D]) -> bool:
    for s in skyline_points:
        if dominates(s, p):
            return True
    return False

def mbr_corner_dominated(mbr: MBR3D, skyline_points: List[Point3D]) -> bool:
    corner = tuple(mbr.low)
    return dominated_by_skyline(corner, skyline_points)

def skyline_with_rtree(root: RTreeNode):
    skyline_ids = []
    skyline_points = []  # 只存座標，用來判斷支配

    # heap 裡放：(mindist, kind, obj)
    # kind: 0 = node, 1 = point
    heap = []
    heapq.heappush(heap, (root.mbr.mindist_to_origin(), 0, root))

    while heap:
        dist, kind, obj = heapq.heappop(heap)

        if kind == 0:  # node
            node: RTreeNode = obj
            if skyline_points and mbr_corner_dominated(node.mbr, skyline_points):
                continue
            if node.is_leaf:
                for pid, p in node.children:
                    if not dominated_by_skyline(p, skyline_points):
                        md = math.sqrt(sum(c * c for c in p))
                        heapq.heappush(heap, (md, 1, (pid, p)))
            else:
                for child in node.children:
                    md = child.mbr.mindist_to_origin()
                    heapq.heappush(heap, (md, 0, child))

        else:  # point
            pid, p = obj
            if not dominated_by_skyline(p, skyline_points):
                skyline_ids.append((pid, p))
                skyline_points.append(p)

    return skyline_ids

# ========== 5. 主程式：讀檔、執行兩種 skyline、印結果 ==========

def main():
    points_with_id = load_points_from_file("point.txt")

    print("=== Brute-force Skyline ===")
    skyl_bf = brute_force_skyline_with_id(points_with_id)
    for pid, p in skyl_bf:
        print(f"{pid}: {p}")

    print("\n=== R-tree Skyline (BBS-style) ===")
    root = bulk_load_rtree(points_with_id, max_children=3)
    skyl_rt = skyline_with_rtree(root)
    for pid, p in skyl_rt:
        print(f"{pid}: {p}")

if __name__ == "__main__":
    main()
