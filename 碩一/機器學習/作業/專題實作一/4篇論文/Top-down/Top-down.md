I. INTRODUCTION:



1\. 監督式方法與模型的定義

• 監督式方法旨在發現輸入屬性與目標屬性之間的關係。

• 這種被發現的關係會被表示在一個被稱為模型的結構中。

• 模型通常可用於在已知輸入屬性值的情況下，預測目標屬性值。

• 主要的監督式模型可區分為兩大類：分類模型（分類器）迴歸模型。

2\. 分類器與迴歸模型的區別

• 迴歸模型將輸入空間映射到實數值域。

• 分類器則將輸入空間映射到預定義的類別中。

• 舉例來說，分類器可用於將抵押貸款消費者分類為「良好」（按時全額還款）或「不良」（延遲還款）。

3\. 決策樹的重要性

• 決策樹是表示分類器最廣泛使用的方法之一。

• 它最初在決策理論和統計學領域中被研究，但也被發現在資料探勘、機器學習和模式識別等其他學科中是有效的。

• 決策樹也應用於許多現實世界的應用中。

4\. 本次調查的焦點

• 鑑於決策樹的悠久歷史和高度關注，文獻中雖然已有幾份相關的調查報告 (如參考資料– 所述，即外部文獻)。

• 然而，本調查提出了一個深刻但簡潔的描述，專門針對決策樹的頂向下建構 (top-down construction) 相關議題。

• 頂向下建構被認為是最流行的建構方法。

• 這篇論文的目標是將所有已開發的重要方法組織成一個連貫且統一的參考資料。

• 摘要（Abstract）中也進一步指出，本論文建議了一個統一的演算法框架，並描述了各種分割準則 (splitting criteria) 和修剪方法 (pruning methodologies)。



----------



II. PRELIMINARIES:

1\. 監督式學習的基礎設定

本節首先設定了典型的監督式學習情境：

• 給定一個帶標籤的訓練集 (a training set of labeled examples)。

• 學習的目標是形成一種描述 (a description)，可以用來預測先前未見過的樣本 (predict previously unseen examples)。

2\. 數據的描述與結構

資料集的結構和屬性類型被形式化地定義：

• 訓練集描述語言： 訓練集通常被描述為某種「bag schema」的實例包 (bag instance)。

• Bag Schema： 提供屬性及其定義域的描述。

&nbsp;   ◦ 它由輸入屬性集合 A (包含 A 

1

​

&nbsp; 到 A 

m

​

&nbsp;) 以及類別變數或目標屬性 y 組成。

• 屬性類型： 屬性（有時稱為欄位、變數或特徵）通常分為兩種類型：

&nbsp;   ◦ 名義型 (Nominal)： 值屬於一個無序集合的成員。

&nbsp;   ◦ 數值型 (Numeric)： 值為實數，具有無限的基數 (infinite cardinalities)。

3\. 實例空間與訓練集定義

• 實例空間 (Instance Space \\Omega)： 定義為所有輸入屬性定義域的笛卡爾積。

• 標籤實例空間 (Universal/Labeled Instance Space \\Omega\_L)： 定義為所有輸入屬性域與目標屬性域的笛卡爾積。

• 訓練集 (Training Set S)： 由一組元組（或稱記錄）組成，這些元組根據 bag schema 的定義，由屬性值向量描述。

• 數據生成假設： 通常假設訓練集的元組是根據 Ω 

L

​

&nbsp; 上某個固定且未知的聯合概率分佈隨機且獨立生成的。

4\. 概念學習與分類問題

本節將學習問題從傳統概念擴展到更廣泛的分類：

• 概念學習 (Concept Learning)： 機器學習社群最初引入的問題，旨在從一組範例中推斷出概念的一般定義，將每個可能的實例分配給布林集合 {true, false}。

• 分類問題 (Classification Problem)： 資料探勘社群傾向於處理概念學習的直接延伸，即尋找一個函數，將所有可能的實例映射到預定義的類別標籤集合中，而不限於布林集合。

• 歸納器 (Inducer)： 歸納器是一個實體 (I)，它獲取訓練集 (S) 並形成一個分類器 (C)，該分類器代表了輸入屬性與目標屬性之間廣義化的關係。

5\. 最佳化目標與錯誤率

本節提供了分類器歸納器追求的正式目標：

• 目標： 在給定訓練集的情況下，目標是歸納出一個具有最小泛化錯誤 (minimum generalization error) 的最佳分類器。

• 泛化錯誤 (Generalization Error)： 定義為在分佈 P(x,y) 上的誤分類率 (misclassification rate)。

• 損失函數 (Loss Function)： 對於名義型屬性，泛化錯誤由公式 (1) 表示，其中損失函數 Λ(y,C(x)) 定義為：

&nbsp;   ◦ 如果預測 C(x) 等於真實目標 y，則 Λ=0。

&nbsp;   ◦ 如果預測不等於真實目標，則 Λ=1。

6\. 分類器類型

分類器根據其輸出的形式可以分為兩類：

• 確定性分類器 (Crisp Classifier)： 通過明確地將一個未見過的元組分配給一個特定的類別來進行分類。

• 機率分類器 (Probabilistic Classifier)： 提供一個機率向量，代表給定實例屬於每個類別的條件機率。



--------

III. DECISION TREE REPRESENTATION:



1\. 決策樹的結構與定義

決策樹被定義為對\*\*實例空間 14, 15]：

1\. 決策樹的結構與定義

決策樹被定義為對實例空間 (instance space) 進行遞迴分割 (recursive partition) 的一種分類器。

決策樹的組成要素包括：

• 根節點 (Root node)： 它是樹的起點，沒有任何進入邊 (incoming edges)。

• 內部節點或測試節點 (Internal or Test node)： 具有引出邊 (outgoing edges) 的節點。

• 葉節點或決策節點 (Leaves or Decision nodes)： 沒有引出邊的節點。

除了根節點外，所有其他節點都恰好有一條進入邊。

2\. 決策樹如何進行分割與分類

• 分割機制： 每個內部節點會根據輸入屬性值的一個離散函數，將實例空間分割成兩個或多個子空間。

&nbsp;   ◦ 在最簡單且最常見的情況下，每個測試只考慮單一屬性，實例空間根據該屬性的值進行分割。

&nbsp;   ◦ 如果是數值型屬性 (numeric attributes)，條件通常涉及一個範圍 (a range)。

• 分類結果： 每個葉節點會被分配給一個類別，該類別代表了最合適的目標值。

&nbsp;   ◦ 或者，葉節點也可能帶有一個機率向量 (a probability vector)，指示目標值具有某一特定值的機率。

• 實例分類過程： 實例是通過從根節點開始，沿著樹向下導航，根據路徑上測試的結果，直到到達葉節點來進行分類的。

3\. 幾何解釋與規則轉換

• 幾何解釋： 在處理數值型屬性時，決策樹可以從幾何上解釋為一組超平面 (hyperplanes)，每個超平面都與其中一個軸正交 (orthogonal)。

• 規則轉換： 決策樹歸納與規則歸納 (rule induction) 密切相關。從決策樹的根節點到任一葉節點的每條路徑都可以轉換成一個規則 (rule)。

&nbsp;   ◦ 轉換方法是將路徑上的所有測試合取 (conjoining) 起來作為規則的前件部分 (antecedent part)。

&nbsp;   ◦ 並將葉節點的類別預測作為類別值 (class value)。

&nbsp;   ◦ 隨後，生成的規則集可以被簡化，以提高人類使用者對其的可理解性 (comprehensibility) 和準確性。

&nbsp;   ◦ 例如，圖1中的一條路徑可以轉換為規則：「如果客戶年齡 ≤30，且客戶性別為「男性」，則客戶將會回應郵件」。

4\. 決策樹的複雜度與優化

決策者傾向於不那麼複雜的決策樹，因為它們可能被認為更具全面性 (more comprehensive)。此外，樹的複雜度對其準確性表現 (accuracy performance) 有著關鍵性的影響。

樹的複雜度是通過停止準則 (stopping criteria) 和採用的修剪方法 (pruning method) 來明確控制的。

衡量樹複雜度的常見指標包括：

• 節點總數 (the total number of nodes)。

• 葉節點總數 (total number of leaves)。

• 樹的深度 (tree depth)。

• 使用的屬性數量 (number of attributes used)。



--------



IV. ALGORITHMIC FRAMEWORK FOR DECISION TREES:

1\. 演算法的目標與挑戰 (Goal and Challenges)

• 目標： 決策樹歸納演算法（Inducers）的目標是自動建構出一個最佳決策樹，以最小化泛化錯誤 (generalization error)。

&nbsp;   ◦ 不過，也可以定義其他的目標函數，例如：最小化節點數量或最小化平均深度。

• 挑戰 (NP-Hardness)： 從給定資料中歸納出一個最佳決策樹被認為是一個困難的任務。

&nbsp;   ◦ 研究顯示，找到一個與訓練集一致的最小決策樹是 NP-Hard 問題。

&nbsp;   ◦ 建構一個關於分類未見實例所需測試次數的最小二元樹是 NP-complete 問題。

&nbsp;   ◦ 這些參考資料表明，使用最佳決策樹演算法只在小問題中是可行的。因此，解決此類問題需要啟發式方法 (heuristics methods)。

2\. 演算法分類與主流方法

• 大致上，啟發式方法可分為兩組：頂向下 (top-down) 和底向上 (bottom-up)。

• 文獻中對頂向下方法有著明顯的偏好。

3\. 頂向下演算法框架 (Top-Down Framework)

• 頂向下歸納決策樹的演算法（如圖2所示）本質上是貪婪 (greedy) 的。

• 它們以頂向下、遞迴的方式建構決策樹（這也被稱為「分治法」，divide and conquer）。

• 建構步驟：

&nbsp;   1. 在每一次迭代中，演算法會考慮使用輸入屬性的離散函數的結果來分割訓練集。

&nbsp;   2. 選擇最合適函數的依據是某些分割準則 (splitting measures)。

&nbsp;   3. 選定合適的分割後，每個節點會進一步將訓練集細分為更小的子集。

&nbsp;   4. 這個過程會一直持續，直到沒有分割能獲得足夠的分割測量值，或滿足了停止準則 (stopping criteria) 為止。

4\. 演算法階段 (Conceptual Phases)

• 常見的頂向下決策樹歸納器包括 ID3、C4.5，以及 CART。

• 有些歸納器（如 C4.5 和 CART）包含兩個概念階段：

&nbsp;   1. 生長 (Growing) 階段。

&nbsp;   2. 修剪 (Pruning) 階段。

• 其他歸納器（如 ID3）則只執行生長階段。



------------

V. UNIVARIATE SPLITTING CRITERIA:

A. 概述 (Overview)

1\. 單變量分割的定義 (Univariate Meaning)：在大多數情況下，離散分割函數是單變量的。單變量意味著一個內部節點是根據單一屬性的值進行分割的。

2\. 歸納器尋找的目標：歸納器（Inducer）在單變量情境下，需要尋找最佳的屬性來進行分割。

3\. 準則的分類：文獻中存在多種單變量準則，這些準則可以根據不同的方式進行分類：

&nbsp;   ◦ 根據測量值的來源：包括資訊理論 (information theory)、依賴性 (dependence) 和距離 (distance)。

&nbsp;   ◦ 根據測量值的結構：包括基於不純度 (impurity based criteria)、基於正規化不純度 (normalized impurity based criteria) 和二元準則 (binary criteria)。

B. 基於不純度的準則 (Impurity Based Criteria)

基於不純度 (Impurity) 的準則衡量了目標屬性在分割前後的混亂程度（不確定性）的減少量。

1\. 不純度測量 (Impurity Measure)：

&nbsp;   ◦ 不純度函數 Imp(P) 應滿足一系列條件，例如：當概率向量 P 中有一個分量為 1 時（變量只取一個值，即純淨），不純度達到最小值。

&nbsp;   ◦ 如果所有分量都相等（最大程度的混亂），則不純度的水準達到最大值。

2\. 分割的優度 (Goodness-of-split)：由於離散屬性 A 造成的分割優度，被定義為目標屬性在根據 A 的值進行分割後，不純度的減少量。

3\. 資訊增益 (Information Gain)：這是一種基於不純度的準則，它使用熵 (entropy) 測量作為不純度測量，源自資訊理論。

4\. Gini 係數 (Gini Index)：

&nbsp;   ◦ Gini 係數是另一種基於不純度的準則，它測量目標屬性值的概率分佈之間的差異 (divergence)。它已被應用於各種文獻中

C. 其他單變量準則

1\. 可能性比率卡方統計量 (Likelihood Ratio Chi-Squared Statistics)：

&nbsp;   ◦ 可能性比率 (likelihood ratio) 可用於測量資訊增益準則的統計顯著性。

&nbsp;   ◦ 零假設是輸入屬性與目標屬性是條件獨立的。

2\. 正規化基於不純度的準則 (Normalized Impurity Based Criteria)：

&nbsp;   ◦ 前述的基於不純度的準則（如資訊增益）傾向於偏愛具有較大值域的屬性（即值較多的屬性）。

&nbsp;   ◦ 為了解決這種偏差，需要對這些測量進行\*\*「正規化」（normalize）\*\*。

3\. 增益比率 (Gain Ratio)：

&nbsp;Quinlan 提出了增益比率 (Gain Ratio)，用於對資訊增益進行正規化。

研究顯示，增益比率在準確性和分類器複雜度方面往往優於簡單的資訊增益準則。

4\. 距離測量 (Distance Measure)：

&nbsp;   ◦ Lopez de Mantras 引入了另一種距離測量，它也對不純度測量進行正規化，但使用不同的方式。

5\. 二元準則 (Binary Criteria)：

&nbsp;   ◦ 這些準則用於創建二元決策樹，其基礎是將輸入屬性的值域劃分為兩個子域。

&nbsp;   ◦ 只有當屬性值域被最佳劃分為兩個互斥且窮舉的子域時，得到的準則值才用於比較屬性。

6\. 兩分準則 (Twoing Criteria)：

&nbsp;   ◦ Breiman 等人建議在 Gini 係數可能遇到問題時使用兩分準則。

&nbsp;   ◦ 對於多類別問題，兩分準則偏好均勻分割的屬性。

7\. 正交準則 (Orthogonality Criterion, ORT)：

&nbsp;   ◦ 這是一個二元準則，它通過測量分割後兩個分佈向量之間的夾角來定義。

&nbsp;   ◦ 有研究顯示，該準則在特定的問題情境下優於資訊增益和 Gini 係數。

8\. Kolmogorov–Smirnov 準則：

&nbsp;   ◦ 這是一種利用 Kolmogorov–Smirnov 距離的二元準則。有研究表明，其擴展版本優於增益比率。

D. 單變量分割準則的比較

• 研究人員已對這些準則進行了比較研究。

• 大多數研究人員指出，在大多數情況下，分割準則的選擇對樹的性能影響不大。

• 如同「天下沒有白吃的午餐定理」(no-free-lunch theorem) 所暗示的，每個準則在某些情況下表現優異，但在其他情況下則較差。



----------

VI. MULTIVARIATE SPLITTING CRITERIA:

1\. 多變量分割準則的定義與特點

• 定義： 在多變量分割準則中，單一節點的分割測試可能會涉及多個輸入屬性。

• 複雜性： 顯然，尋找最佳的多變量準則要比尋找最佳的單變量分割複雜得多 (more complicated)。

2\. 性能與流行度

• 潛在優勢： 儘管實施複雜，這類準則可能會顯著改善決策樹的性能 (dramatically improve the tree’s performance)。

• 實際流行度： 然而，多變量準則遠不如單變量準則受歡迎 (much less popular)。

3\. 實施多變量準則的方法

大多數多變量分割準則都是基於輸入屬性的線性組合 (linear combination of the input attributes)。

尋找最佳線性組合的方法可以通過以下幾種技術來實現：

• 貪婪搜尋 (Greedy search)

• 線性規劃 (Linear programming)

• 線性判別分析 (Linear discriminant analysis, LDA)



------

VII. STOPPING CRITERIA:

停止準則的核心說明

頂向下決策樹的生長階段 (The growing phase) 會持續進行，直到觸發了某個停止準則為止。

資料中列出了常見的停止規則 (common stopping rules)，包括以下條件：

1\. 目標屬性純淨 (Homogeneity)：訓練集中的所有實例都屬於目標屬性 y 的單一值。

&nbsp;   ◦ （意即該節點已經「純淨」，不需要進一步分割。）

2\. 達到最大樹深度 (Maximum Depth)：決策樹已達到最大深度的限制。

3\. 父節點案例數不足 (Minimum Cases for Parent)：終端節點中的案例數少於作為父節點所需的最小案例數。

4\. 子節點案例數不足 (Minimum Cases for Child)：如果該節點進行分割，其中一個或多個子節點中的案例數將會少於作為子節點所需的最小案例數。

5\. 分割準則閾值限制 (Splitting Criteria Threshold)：最佳分割準則的值沒有大於某個特定的閾值。

&nbsp;   ◦ （意即找不到一個「足夠好」的分割屬性來改善數據純度。）

停止準則與修剪方法的關係

值得注意的是，停止準則的設定對於最終樹的複雜度影響重大，這也與下一節（Pruning Methods，修剪方法）有直接關係：

• 採用嚴格的停止準則 (tightly stopping criteria) 往往會生成較小且欠擬合 (under-fitted) 的決策樹。

• 相反地，採用寬鬆的停止準則 (loosely stopping criteria) 則傾向於生成較大且過度擬合 (over-fitted) 訓練集的決策樹。

• 修剪方法的開發，如 Breiman 等人 最早提出的方法，就是為了處理這種困境：通常會先使用寬鬆的停止準則讓決策樹過度擬合訓練集，然後再通過修剪來將過度擬合的樹縮減成更小的樹，以提高泛化準確性。

----------



VIII. PRUNING METHODS

A. 概述與動機 (Overview and Motivation)

1\. 解決兩難困境： 決策樹歸納器面臨一個兩難困境：

&nbsp;   ◦ 採用嚴格的停止準則 (tightly stopping criteria) 會生成較小且欠擬合 (under-fitted) 的決策樹。

&nbsp;   ◦ 採用寬鬆的停止準則 (loosely stopping criteria) 則會生成較大且過度擬合 (over-fitted) 訓練集的決策樹。

2\. 修剪方法的作用： 修剪方法 (Pruning methods)，最早由 Breiman 等人 提出，旨在解決這一困境。

3\. 修剪流程： 根據這種方法，通常會先使用寬鬆的停止準則讓決策樹過度擬合訓練集，然後再通過移除對泛化準確性沒有貢獻的子分支 (sub branches) 來將過度擬合的樹縮減成更小的樹。

4\. 性能提升： 多項研究顯示，在特別是嘈雜的領域 (noisy domains) 中，採用修剪方法可以改善決策樹的泛化性能。

5\. 核心目標： 修剪的另一個關鍵動機是實現 「以準確性換取簡潔性」 (trading accuracy for simplicity)。如果目標是生成一個足夠準確且緊湊的概念描述 (compact concept description)，修剪就非常有用。

6\. 實施方式： 大多數修剪技術都是通過頂向下 (top down) 或底向上 (bottom up) 的方式遍歷節點，如果該操作能夠改善特定的準則，則對該節點進行修剪。

B. 主要的修剪技術

資料中介紹了數種重要的修剪技術：

1\. 成本複雜度修剪 (Cost-Complexity Pruning / Weakest Link Pruning / Error Complexity Pruning)

&nbsp;   ◦ 由 Breiman 等人 提出，分為兩個階段。

&nbsp;   ◦ 第一階段： 在訓練資料上建構一系列樹，其中 T 

0

​

&nbsp; 是原始樹， T 

t

​

&nbsp; 是根樹 (root tree)。

&nbsp;   ◦ 樹 T 

α

​

&nbsp; 是通過將前一個樹中，每修剪一個葉子，表觀錯誤率增加最低的子樹替換為合適的葉子而獲得的。

&nbsp;   ◦ 第二階段： 根據對泛化錯誤的估計，從這些修剪後的樹中選擇最佳的一個。

&nbsp;   ◦ 如果資料集夠大，作者建議將其劃分為訓練集和修剪集；如果資料集不夠大，則建議使用交叉驗證 (cross-validation)。

2\. 減少錯誤修剪 (Reduced-Error Pruning)

&nbsp;   ◦ 由 Quinlan 提出，是一種簡單的修剪過程。

&nbsp;   ◦ 它從底向上遍歷內部節點，檢查用最頻繁的類別替換該內部節點是否不會降低樹的準確性。如果是，則修剪該節點，直到任何進一步的修剪都會降低準確性為止。

&nbsp;   ◦ 為了估計準確性，Quinlan 建議使用修剪集 (pruning set)。

3\. 最小錯誤修剪 (Minimum-Error Pruning, MEP)

&nbsp;   ◦ 由 Niblett 和 Bratko 提出。

&nbsp;   ◦ 執行底向上遍歷，比較帶有和不帶有修剪時 l-機率錯誤率估計 (l-probability-error rate estimation)。

&nbsp;   ◦ 如果修剪一個節點不會增加機率錯誤，則修剪該節點。

4\. 悲觀修剪 (Pessimistic Pruning)

&nbsp;   ◦ Quinlan 的悲觀修剪避免了使用單獨的修剪集或交叉驗證。

&nbsp;   ◦ 它使用基於二項式分佈的悲觀統計校正測試 (pessimistic statistical correlation test)。

&nbsp;   ◦ 如果內部節點的錯誤率在一個標準誤差內與參考樹的錯誤率相符，則修剪該節點。該過程是頂向下遍歷的，如果一個節點被修剪，其所有後代都會被移除，從而實現相對快速的修剪。

5\. 基於錯誤的修剪 (Error-Based Pruning, EBP)

&nbsp;   ◦ 這是悲觀修剪的演進版，實施在著名的 C4.5 演算法中。

&nbsp;   ◦ 與悲觀修剪類似，它使用統計置信區間的上限來估計錯誤率。

&nbsp;   ◦ 該程序執行底向上遍歷，比較三種情況下的估計錯誤率：保持現狀、修剪該節點、或用該節點最頻繁的子節點替換該節點。

6\. 最佳修剪 (Optimal Pruning, OPT/OPT-2)

&nbsp;   ◦ Bratko 和 Bohanec 引入了 OPT 演算法，保證了最佳性，它使用動態規劃 (dynamic programming) 來找到最佳修剪。

&nbsp;   ◦ Almuallim 提出了 OPT-2，也使用動態規劃進行最佳修剪，通常在計算複雜度上比 OPT 更有效率。

7\. 最小描述長度修剪 (Minimum Description Length Pruning, MDL)

&nbsp;   ◦ MDL 原理 通過編碼樹所需的位元數來衡量決策樹的大小，傾向於選擇可以用更少位元編碼的決策樹。

C. 修剪方法的比較

• 多項研究對不同的修剪技術進行了比較。

• 結果表明，有些方法（如成本複雜度修剪和減少錯誤修剪）傾向於過度修剪 (over-pruning)，即生成較小但準確性較低的決策樹。

• 與分割準則的比較結果相似，大多數比較研究得出的結論是 「天下沒有白吃的午餐定理」 (no-free-lunch theorem) 在這裡也適用，即沒有一種修剪方法可以在所有情況下都優於其他方法。



--------



IX. OTHER ISSUES:

A. 實例加權 (Weighting Instances)

• 一些決策樹歸納器可以對不同的實例（即數據點）給予不同的處理。

• 這是通過為分析中的每個實例提供一個權重（介於 0 到 1 之間）來實現的，以調整其在分析中的貢獻。

B. 誤分類成本 (Misclassification Costs)

• 有些決策樹歸納器可以被提供數字化的懲罰 (numeric penalties)，用於將一個項目錯誤分類到某個類別時，而該項目實際屬於另一個類別。

• 例如，CART 演算法在樹歸納過程中就可以考慮誤分類成本。

C. 處理遺失值 (Handling Missing Values)

• 遺失值是現實世界資料集中常見的情況。

• 這種情況會使歸納（訓練集中部分值遺失）和分類（新實例遺失特定值）兩個階段都變得複雜。

處理遺失值的策略：

研究人員提出了多種處理遺失值的方法：

1\. 忽略實例 (Ignoring Instances)：

&nbsp;   ◦ Friedman 建議在計算分割準則時，只需忽略在該屬性上遺失值的實例。

&nbsp;   ◦ 這意味著，如果屬性 A 的值遺失，則在計算分割準則時，僅使用那些在 A 上有已知值的實例子集。

2\. 按比例減少分割準則 (Proportional Reduction)：

&nbsp;   ◦ Quinlan 認為，在有遺失值的情況下，分割準則應按比例減少，因為演算法沒有從這些實例中學到任何東西。

&nbsp;   ◦ 這意味著，計算出的分割準則值會乘以一個修正係數，該係數是已知值的實例數佔總實例數的比例。

3\. 將遺失值視為附加值 (Treating Missing as Additional Value)：

&nbsp;   ◦ 如果準則值經過正規化（例如增益比率 Gain Ratio），則計算分母時，應將遺失值視為屬性域中的額外一個值來處理。

4\. 分配權重到子邊 (Assigning Weights to Sub-edges)：

&nbsp;   ◦ 一旦節點被分割，Quinlan 建議為每條引出邊分配對應的權重，權重基於屬於該子集的實例比例。

&nbsp;   ◦ 當對具有遺失屬性值的新實例進行分類時，如果該實例遇到一個因遺失值而無法評估分割準則的節點，它將被傳遞到所有引出邊。最終，預測的類別將是該實例結束於的所有葉節點的加權聯合中機率最高的類別。

5\. 替代分割 (Surrogate Splits)：

&nbsp;   ◦ Breiman 等人 提出了替代分割 (surrogate splits) 的方法，並在 CART 演算法中實施。

&nbsp;   ◦ 這個概念是為樹中的每個分割找到一個替代分割，該替代分割使用不同的輸入屬性，但最接近原始分割。

&nbsp;   ◦ 如果實例在原始分割所用的輸入屬性上遺失值，則使用替代分割來引導該實例向下傳播。

6\. 基於其他實例估計遺失值 (Estimating Missing Values)：

&nbsp;   ◦ Loh 和 Shih 建議根據其他實例來估計遺失值。

&nbsp;   ◦ 如果元組 t 中名義型屬性的值遺失，則使用所有具有相同目標屬性值 (y(t)) 的實例中，該屬性的眾數 (mode) 來估計。

&nbsp;   ◦ 如果遺失屬性是數值型，則應使用平均值 (mean) 來代替眾數



-----------

X. DECISION TREES INDUCERS:

本節詳細描述了幾個歷史上和當前文獻中最著名的頂向下歸納決策樹演算法：

A. ID3 (Iterative Dichotomiser 3)

• 提出者： 由 Quinlan 提出。

• 核心特點： 被認為是一個非常簡單的決策樹演算法。

• 分割準則： 使用資訊增益 (Information Gain) 作為分割準則。

• 停止條件： 當所有實例屬於目標特徵的單一值時，或當最佳資訊增益不大於零時，生長停止。

• 處理限制： ID3 不應用任何修剪程序。它也不處理數值型屬性，也不處理遺失值。

B. C4.5

• 提出者： 由 Quinlan 提出，是 ID3 的進化版。

• 分割準則： 使用增益比率 (Gain Ratio) 作為分割準則。

• 停止條件： 當要分割的實例數量低於某個閾值時，分割終止。

• 修剪： 在生長階段之後執行基於錯誤的修剪 (Error-Based Pruning, EBP)。

• 功能： C4.5 能夠處理數值型屬性。它也可以從包含遺失值的訓練集中進行歸納，方法是使用已修正的增益比率準則（如前一節 IX. C 所述）。

C. CART (Classification and Regression Trees)

• 提出者： 由 Breiman 等人開發。

• 核心特點： 它的特點是建構二元樹 (binary trees)，即每個內部節點恰好有兩條引出邊。

• 分割準則： 分割的選擇使用兩分準則 (twoing criteria)。

• 修剪： 歸納出的樹通過成本複雜度修剪 (cost-complexity pruning) 進行修剪。

• 特殊功能：

&nbsp;   ◦ CART 可以在樹歸納過程中考慮誤分類成本 (misclassification costs)。

&nbsp;   ◦ 它還允許使用者提供先驗機率分佈。

&nbsp;   ◦ CART 的一個重要功能是能夠生成迴歸樹 (regression trees)，其葉子預測的是實數而不是類別。在迴歸情況下，CART 使用最小平方偏差 (least-squared deviation) 作為分割優度測量。

D. CHAID (Chi-square Automatic Interaction Detection)

• 起源： 這是應用統計學研究人員從 1970 年代初開始開發的幾個程序之一 (如 AID、MAID、THAID)。

• 設計用途： CHAID 最初設計用於僅處理名義型屬性。

• 分割機制：

&nbsp;   ◦ 對於每個輸入屬性，CHAID 尋找在目標屬性方面最不顯著差異的一對值。

&nbsp;   ◦ 顯著差異的測量是通過統計檢定的值獲得的，檢定類型取決於目標屬性類型：連續屬性使用 F 檢定；名義型屬性使用 Pearson 卡方檢定；順序屬性使用可能性比率檢定。

&nbsp;   ◦ 如果得到的 p 值大於某個合併閾值，則將這些值合併，並重複此過程，直到找不到顯著對。

&nbsp;   ◦ 然後，它選擇最佳輸入屬性來分割當前節點，使得每個子節點由所選屬性的同質值組構成。

• 停止條件： 如果最佳輸入屬性的調整 p 值不小於某個分割閾值，則不進行分割。其他停止條件包括達到最大樹深度，以及節點中的案例數不足。

• 處理限制： CHAID 不執行修剪。它通過將所有遺失值視為單一有效類別來處理遺失值。

E. QUEST (Quick, Unbiased, Efficient, Statistical Tree)

• 提出者： 由 Loh 和 Shih 提出。

• 核心特點： QUEST 支援單變量和線性組合分割，並且偏差可忽略不計，產生二元決策樹。

• 分割選擇： 使用 ANOVA F 檢定或 Levene 檢定（適用於順序和連續屬性）或 Pearson 卡方檢定（適用於名義屬性）計算每個屬性與目標屬性之間的關聯度。

• 最佳分割點： 選擇具有最高關聯度的屬性進行分割，並應用二次判別分析 (Quadratic discriminant analysis, QDA) 來尋找最佳分割點。

• 修剪： 使用十重交叉驗證 (Ten-fold cross-validation) 來修剪樹。

F. 其他演算法的參考

本節還指出，文獻中存在許多其他決策樹演算法（例如在表 I 中），但大多數這些演算法都是基於前面所述的演算法框架的變體



---------

XI. ADVANTAGES AND DISADVANTAGES OF DECISION TREES:

A廣受歡迎的原因）以及限制（需要研究人員繼續改進的挑戰）。

根據資料，該節說明了以下幾個核心方面：

A. 決策樹的優點 (Advantages of Decision Trees)

文獻中指出了決策樹作為分類工具有以下幾個優勢：

1\. 易於理解和解釋 (Comprehensibility and Interpretability)：

&nbsp;   ◦ 決策樹是自我解釋的 (self-explanatory)，並且當它們被壓縮時，也容易追蹤 (easy to follow)。

&nbsp;   ◦ 此外，決策樹可以轉換成一組規則 (a set of rules)。

&nbsp;   ◦ 因此，這種表示法被認為是可理解的 (comprehensible)。

2\. 處理多樣化的輸入屬性 (Handles Diverse Attributes)：

&nbsp;   ◦ 決策樹能夠同時處理名義型 (nominal) 和數值型 (numeric) 的輸入屬性。

3\. 表示能力的豐富性 (Rich Representation)：

&nbsp;   ◦ 決策樹的表示法足夠豐富，可以表示任何離散值分類器 (discrete-value classifier)。

4\. 處理數據中的錯誤 (Handles Errors)：

&nbsp;   ◦ 決策樹能夠處理可能包含錯誤的資料集。

5\. 處理遺失值 (Handles Missing Values)：

&nbsp;   ◦ 決策樹能夠處理可能包含遺失值 (missing values) 的資料集。

6\. 非參數性 (Nonparametric Method)：

&nbsp;   ◦ 決策樹被認為是一種非參數方法 (nonparametric method)。

&nbsp;   ◦ 這意味著決策樹對空間分佈和分類器結構沒有任何假設。

B. 決策樹的缺點 (Disadvantages of Decision Trees)

然而，決策樹也存在一些限制和缺點：

1\. 對目標屬性的要求 (Target Attribute Requirement)：

&nbsp;   ◦ 大多數演算法（如 ID3 和 C4.5）要求目標屬性 (target attribute) 只能是離散值。

2\. 處理複雜交互作用的能力受限 (Limited handling of complex interactions)：

&nbsp;   ◦ 由於決策樹使用「分治法 (divide and conquer)」，如果存在少量高度相關的屬性，它們傾向於表現良好。

&nbsp;   ◦ 但如果存在許多複雜的交互作用，它們的表現會較差。

&nbsp;   ◦ 其中一個原因是，其他分類器可以緊湊地描述一個對於決策樹來說非常難以表示的分類器。

3\. 複製問題 (Replication Problem)：

&nbsp;   ◦ 這是一個簡單的現象，說明了決策樹的這種限制。

&nbsp;   ◦ 由於大多數決策樹將實例空間分割成互斥 (mutually exclusive) 的區域，為了表示分類器，樹可能需要包含相同子樹的多個重複。

&nbsp;   ◦ 資料中舉例說明，如果概念遵循布林函數 y=(A 1∩A 2)∪(A 3∩A 4)，則最小的單變量決策樹為了表示這個函數，將會包含兩個相同子樹的副本（如圖3所示）。

4\. 對訓練集的過度敏感性 (Oversensitivity)：

&nbsp;   ◦ 決策樹的貪婪 (greedy) 特性導致了另一個缺點，即它對訓練集、不相關屬性 (irrelevant attributes) 和雜訊 (noise) 過於敏感。

----------



XII. SPECIAL CASES OF TOP-DOWN DECISION TREES INDUCTION:

A. 遺忘式決策樹 (Oblivious Decision Trees, ODTs)

• 結構限制： 遺忘式決策樹是一種特殊的決策樹，其特點是同一層級 (level) 的所有節點都測試相同的屬性。

• 優勢與應用： 儘管結構受到限制，遺忘式決策樹被認為是一種有效的特徵選擇 (feature selection) 程序。

&nbsp;   ◦ Almuallim 和 Dietterich 以及 Schlimmer 曾提出通過建構遺忘式決策樹來進行正向特徵選擇 (forward feature selection)。

&nbsp;   ◦ Langley 和 Sage 則建議使用相同的方式進行逆向選擇 (backward selection)。

&nbsp;   ◦ Kohavi 和 Sommer 證明遺忘式決策樹可以轉換為決策表 (decision table)。

• 新演算法： 近期，Last 等人 提出了一種新的遺忘式決策樹建構演算法，稱為 資訊模糊網路 IFN()，該演算法基於資訊理論。

• 建構機制： 這種決策樹是通過貪婪演算法 (greedy algorithm) 建構的，該演算法試圖最大化每一層的互資訊測量 (maximize the mutual information measure in every layer)。

• 停止條件： 當沒有屬性能夠以統計顯著性來解釋目標屬性時，遞迴搜尋解釋性屬性的過程終止。

B. 適用於大型數據集的決策樹歸納器 (Decision Trees Inducers for Large Datasets)

• 動機： 由於資訊系統收集的數據量不斷增長，因此需要能夠處理大型數據集的決策樹歸納器。

• 早期的記憶體限制方法：

&nbsp;   ◦ Catlett 研究了兩種高效地從大型資料庫中生成決策樹的方法，以減少計算複雜度，但前提是所有資料都必須載入到主記憶體 (main memory) 中。

&nbsp;   ◦ Fifield 建議了 ID3 演算法的平行實施，但同樣假設整個數據集可以容納在主記憶體中。

&nbsp;   ◦ Chan 和 Stolfo 建議將數據集分割成幾個不相交的子集，分別歸納決策樹後再結合，但實驗結果顯示，這種分割可能降低分類性能。

• 基於次級記憶體的方法 (Secondary Memory)：

&nbsp;   ◦ Mehta 等人 提出了 SLIQ 演算法，它不需要將整個數據集載入主記憶體，而是使用次級記憶體（磁碟）。SLIQ 從整個數據集中建立單一決策樹，但仍有上限限制，因為它使用一個必須常駐在主記憶體且大小隨數據集規模擴展的數據結構。

&nbsp;   ◦ Shafer 等人 提出了類似的解決方案 SPRINT，該演算法建構決策樹的速度相對較快，並移除了決策樹歸納的所有記憶體限制，可以擴展任何基於不純度 (impurity based) 的分割準則來處理大型數據集。

&nbsp;   ◦ Gehrke 等人 提出了 RainForest，這是一個統一的框架，能夠擴展文獻中任何特定的演算法（包括 C4.5、CART 和 CHAID）來處理大型數據集。RainForest 比 SPRINT 效率提高約三倍，但它要求主記憶體需要有最低限度，這個記憶體量與輸入關係中某一列的不同值集合成比例。

• 其他相關工作： 還有其他針對大型數據集的決策樹歸納器，例如 Alsabti 等人的 CLOUDS、Freitas 和 Lavington 的工作，以及 Gehrke 等人的 BOAT 演算法。

C. 增量式歸納 (Incremental Induction)

• 挑戰： 大多數決策樹歸納器需要從頭開始重建整棵樹，才能反映新可用的數據。

• 增量式解決方案： 幾位研究人員致力於解決增量式更新決策樹的問題。

&nbsp;   ◦ Utgoff 提出了幾種增量式更新決策樹的方法。

&nbsp;   ◦ Crawford 描述了 CART 演算法的一個擴展，使其具備增量式歸納的能力。



XIII. CONCLUSION:

1\. 主題重申： 本文呈現了一份關於頂向下決策樹歸納演算法的最新調查報告。

2\. 主要發現與統一框架： 報告強調，大多數決策樹演算法都符合一個簡單的演算法框架。

3\. 差異集中點： 報告指出，各種演算法之間的差異主要集中在以下三個核心機制上：

&nbsp;   ◦ 分割準則 (splitting criteria)。

&nbsp;   ◦ 停止準則 (stopping criteria)。

&nbsp;   ◦ 修剪樹的方式 (the way trees are pruned)。









