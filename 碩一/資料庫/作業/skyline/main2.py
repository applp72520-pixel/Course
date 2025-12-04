from typing import List, Tuple
import math
import heapq
import time
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Point3D = Tuple[float, float, float]

def dominates(p: Point3D, q: Point3D) -> bool:
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

def sfs_skyline_with_id(points_with_id):
    scored = []
    for pid, (x, y, z) in points_with_id:
        score = x + y + z
        scored.append((score, pid, (x, y, z)))
    scored.sort(key=lambda t: t[0])
    skyline: List[Tuple[str, Point3D]] = []
    for _, pid, p in scored:
        dominated = False
        to_remove = []
        for idx, (sid, sp) in enumerate(skyline):
            if dominates(sp, p):
                dominated = True
                break
            if dominates(p, sp):
                to_remove.append(idx)
        if not dominated:
            if to_remove:
                skyline = [item for i, item in enumerate(skyline) if i not in to_remove]
            skyline.append((pid, p))
    return skyline

def load_points_from_file(path: str):
    result = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) != 4:
            continue
        pid = parts[0]
        x, y, z = map(float, parts[1:])
        result.append((pid, (x, y, z)))
    return result

class MBR3D:
    def __init__(self, low, high):
        self.low = list(low)
        self.high = list(high)

    @staticmethod
    def from_point(p: Point3D):
        return MBR3D(p, p)

    def expand_to_include(self, other: "MBR3D"):
        for i in range(3):
            self.low[i] = min(self.low[i], other.low[i])
            self.high[i] = max(self.high[i], other.high[i])

    def mindist_to_origin(self) -> float:
        x, y, z = self.low
        return math.sqrt(x * x + y * y + z * z)

class RTreeNode:
    def __init__(self, is_leaf: bool):
        self.is_leaf = is_leaf
        self.children = []
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
    points_sorted = sorted(points_with_id, key=lambda x: x[1][0])
    leaves = []
    for i in range(0, len(points_sorted), max_children):
        node = RTreeNode(is_leaf=True)
        node.children = points_sorted[i:i + max_children]
        node.recompute_mbr()
        leaves.append(node)
    level = leaves
    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), max_children):
            node = RTreeNode(is_leaf=False)
            node.children = level[i:i + max_children]
            node.recompute_mbr()
            next_level.append(node)
        level = next_level
    return level[0]

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
    skyline_points = []
    heap = []
    counter = itertools.count()  # <-- tie-breaker
    heapq.heappush(heap, (root.mbr.mindist_to_origin(), 0, next(counter), root))
    while heap:
        dist, kind, _, obj = heapq.heappop(heap)
        if kind == 0:
            node: RTreeNode = obj
            if skyline_points and mbr_corner_dominated(node.mbr, skyline_points):
                continue
            if node.is_leaf:
                for pid, p in node.children:
                    if not dominated_by_skyline(p, skyline_points):
                        md = math.sqrt(sum(c * c for c in p))
                        heapq.heappush(heap, (md, 1, next(counter), (pid, p)))
            else:
                for child in node.children:
                    md = child.mbr.mindist_to_origin()
                    heapq.heappush(heap, (md, 0, next(counter), child))
        else:
            pid, p = obj
            if not dominated_by_skyline(p, skyline_points):
                skyline_ids.append((pid, p))
                skyline_points.append(p)
    return skyline_ids

def plot_3d_skyline(points_with_id, skyline_with_id, filename="skyline_3d.png"):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('3D Skyline Query Visualization', fontsize=14, fontweight='bold')
    # 全點
    xs, ys, zs = zip(*[pt for _, pt in points_with_id])
    ax.scatter(xs, ys, zs, c='lightgray', s=80, alpha=0.6, label='All Points', edgecolor='gray')
    # Skyline 點（紅色大圓 + 深紅圈浮出）
    skyl_x, skyl_y, skyl_z = zip(*[pt for _, pt in skyline_with_id])
    ax.scatter(skyl_x, skyl_y, skyl_z, c='red', s=200, marker='o',
               label='Skyline Points', edgecolor='darkred', linewidths=2.5, alpha=0.9)
    for pid, (x, y, z) in points_with_id:
        ax.text(x+1, y+1, z+1, pid, color='black', fontsize=10, fontweight='bold')
    ax.set_xlabel("A1 (X)", fontsize=12)
    ax.set_ylabel("A2 (Y)", fontsize=12)
    ax.set_zlabel("A3 (Z)", fontsize=12)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_zlim(0, 100)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"圖檔已儲存: {filename}")
    plt.show()


def print_skyline_and_time(
    skyl_bf, t_bf,
    skyl_sfs, t_sfs,
    skyl_rt, t_rt
):
    def to_set(skyl):
        return set((pid, tuple(p)) for pid, p in skyl)
    print("\n" + "="*60)
    print("Skyline Query 結果與時間比較")
    print("="*60)
    print("\n【暴力法 (Brute-force) Skyline】")
    for pid, (x, y, z) in sorted(skyl_bf):
        print(f"  {pid}: ({x:.0f}, {y:.0f}, {z:.0f})")
    print(f"  執行時間: {t_bf*1000:.3f} ms")
    print("\n【SFS Skyline】")
    for pid, (x, y, z) in sorted(skyl_sfs):
        print(f"  {pid}: ({x:.0f}, {y:.0f}, {z:.0f})")
    print(f"  執行時間: {t_sfs*1000:.3f} ms")
    print("\n【R-tree BBS Skyline】")
    for pid, (x, y, z) in sorted(skyl_rt):
        print(f"  {pid}: ({x:.0f}, {y:.0f}, {z:.0f})")
    print(f"  執行時間: {t_rt*1000:.3f} ms")
    same_bf_sfs = to_set(skyl_bf) == to_set(skyl_sfs)
    same_bf_rt = to_set(skyl_bf) == to_set(skyl_rt)
    print("\n結果一致性檢查：")
    print(f"  暴力法 vs SFS    : {'相同' if same_bf_sfs else '不同'}")
    print(f"  暴力法 vs R-tree : {'相同' if same_bf_rt else '不同'}")
    print("="*60)

def main():
    print("【 3D Skyline Query 整合程式（三種演算法+時間） 】\n")
    print("1. 讀取 point.txt...")
    try:
        points_with_id = load_points_from_file("point.txt")
        print(f"   成功讀取 {len(points_with_id)} 個點\n")
    except FileNotFoundError:
        print("   找不到 point.txt，請確認檔案在同一資料夾\n")
        return

    print("2. 執行 暴力法 (Brute-force) skyline...")
    t0 = time.perf_counter()
    skyl_bf = brute_force_skyline_with_id(points_with_id)
    t1 = time.perf_counter()
    t_bf = t1 - t0
    print(f"   完成，skyline 點數: {len(skyl_bf)}，花費 {t_bf*1000:.3f} ms\n")

    print("3. 執行 SFS (Sort-Filter-Skyline) ...")
    t0 = time.perf_counter()
    skyl_sfs = sfs_skyline_with_id(points_with_id)
    t1 = time.perf_counter()
    t_sfs = t1 - t0
    print(f"   完成，skyline 點數: {len(skyl_sfs)}，花費 {t_sfs*1000:.3f} ms\n")

    print("4. 建構 3D R-tree 並執行 BBS skyline...")
    t0 = time.perf_counter()
    root = bulk_load_rtree(points_with_id, max_children=3)
    skyl_rt = skyline_with_rtree(root)
    t1 = time.perf_counter()
    t_rt = t1 - t0
    print(f"   完成，skyline 點數: {len(skyl_rt)}，花費 {t_rt*1000:.3f} ms\n")

    print_skyline_and_time(skyl_bf, t_bf, skyl_sfs, t_sfs, skyl_rt, t_rt)

    print("\n5. 產生 3D 可視化（使用暴力法 skyline 結果）...")
    plot_3d_skyline(points_with_id, skyl_bf, filename="skyline_3d.png")
    print("\n程式執行完成。")

if __name__ == "__main__":
    main()
