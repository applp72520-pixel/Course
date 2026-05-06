import os

# 將路徑改成您電腦上的實際路徑
base_dir = r"c:\Users\user\Desktop\西醫\dataset"

files = [
    "sct2_Concept_Snapshot_INT_20260401.txt",
    "sct2_Description_Snapshot-en_INT_20260401.txt",
    "sct2_Relationship_Snapshot_INT_20260401.txt"
]

for filename in files:
    input_path = os.path.join(base_dir, filename)
    output_path = os.path.join(base_dir, "clean_" + filename)
    
    # 確保檔案存在才處理
    if not os.path.exists(input_path):
        print(f"找不到檔案: {input_path}")
        continue
        
    print(f"正在處理: {filename} ...")
    
    # 使用 utf-8 編碼讀取與寫入
    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:
        
        # 逐行讀取並替換
        for line in infile:
            # 移除單引號與雙引號
            clean_line = line.replace('"', '').replace("'", "")
            outfile.write(clean_line)
            
    print(f"儲存成功: {output_path}")