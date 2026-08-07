### &代表取它的位置，*ptr = &va代表把var的位置塞給ptr，一個指標是指儲存位置的東西
```
int var = 4;
int *ptr = &var;
```
### 這個代碼片段中，val 的值為 4，因為 *ptr 的值為 var，也就是 4。
```
int var = 4;
int *ptr = &var;
int val = *ptr; 
```

### 當要取內容時，要用*加變數名稱，要取位置時，要用&加變數名稱，要指定東西到它的內容要用*加指標名稱
```
int main() {
    int num = 4;
    int *p = &num;   // 將 p 指向 num 的記憶體位置
    
    printf("num = %d\n", num);
    printf("*p = %d\n", *p);  // 透過指標 p 存取 num 的值
    *p = 20;                   // 透過指標 p 修改 num 的值
    printf("num = %d\n", num);
    
    return 0;
}
```

### 使用指標傳遞參數:
```
void swap(int *a, int *b) {  // 使用指標作為函式參數
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 10, y = 20;
    printf("x = %d, y = %d\n", x, y);
    swap(&x, &y);             // 將 x, y 的位址傳入 swap 函式
    printf("x = %d, y = %d\n", x, y);
    return 0;
}
```
### 使用指標來存取陣列元素作為陣列的索引:
```
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int *p = arr;    // 將 p 指向陣列的第一個元素
    
    for(int i = 0; i < 5; i++) {
        printf("%d ", *(p+i));  // 使用指標存取陣列元素
    }
    
    return 0;
}
```
### 使用 malloc 函式動態地配置記憶體，並將指標指向這塊記憶體，這樣可以在程式執行過程中動態地新增或刪除記憶體空間:
```
int main() {
    int n;
    printf("Enter the size of array: ");
    scanf("%d", &n);
    
    int *p = (int *)malloc(n * sizeof(int));   // 動態配置記憶體
    
    for(int i = 0; i < n; i++) {
        *(p+i) = i+1;                          // 使用指標存取陣列元素
    }
    
    for(int i = 0; i < n; i++) {
        printf("%d ", *(p+i));
    }
    
    free(p);   // 釋放記憶體空間
    
    return 0;
}
```
### 用指標來宣告函數指標:
```

int add(int a, int b) {
    return a + b;
}

int main() {
    int (*p)(int, int);   // 宣告一個指向函式的指標變數
    p = &add;             // 將指標指向 add 函式
    
    int sum = (*p)(10, 20);   // 使用指標呼叫函式
    
    printf("sum = %d\n", sum);
    
    return 0;
}
```

## gcc 語法:

```
 gcc hi.c -0 hi
 ./hi
```

## C4編譯器的主要元件及其功能:
### 詞法分析器（Lexer）、語法分析器（Parser）、代碼生成器（Code Generator）等
### 範例:

```
//計算兩個整數的和
#include <stdio.h>
int main() {
    int num1 = 5;
    int num2 = 10;
    int sum = num1 + num2;
    printf("The sum is: %d\n", sum);
    return 0;
}

```

## OpenAI API:
### 是由 OpenAI 提供的一個人工智慧應用程式介面，它可以讓開發者與 OpenAI 的強大語言模型進行互動。透過這個 API，開發者可以使用程式碼向模型提出問題或給予指令，並獲得模型的回答或生成的文本。






### A1-C語言/01-trap/pointer1.c:
```
int main() {
  char x = 'a';
  char *p = &x;
  *p='b';
  printf("*p=%c x=%c\n", *p, x);  #最後印出結果應該是p=b，x=b
}
```

### 此圖是分頁分段機制，先由CPU經過邏輯位置，這個邏輯位置會被分頁分段機制insert到實體位置，在這insert過程中，會把整個記憶體切成一小塊的，分配給現在所執行的程式，這每一塊上面有個屬性，該屬性會寫說現在是唯讀的還是可寫的，如果data段被放在唯讀區域，但卻自行修改，這時候就會引發作業系統的保護機制，因而引發中斷，導致程式整個掛掉，放在哪個區段是由編譯器跟作業系統來決定的
![](https://drive.google.com/uc?export=view&id=1pSPzdG4AYJa3YgL7U3EtOdfoptZWD64M)


### 02-軟體/02-編譯器/01-diy/00-gen/rlib.c:
```
int randInt(int n) {     #從0到n-1挑選一個出來
  return rand() % n;
}
int randChar(char *set) {   #從一串字裡面挑選一個字元出來
  int len = strlen(set);
  int i = rand()%len;
  return set[i];
}

// int randSelect(char* array, int size):隨機傳回 array 中的一個字串
// 用法:randSelect({"dog", "cat"}, 2) 會傳回二選一的字串
char *randSelect(char* array[], int size) {    #從array[]陣列裡面，隨機挑一個出來
  int i = rand()%size;
  return array[i];
}

void timeSeed() {
  long ltime = time(NULL); #呼叫時鐘函數
  srand(ltime); #用時鐘取得的時間設定亂數種子
}

```

### 02-軟體/02-編譯器/01-diy/00-gen/genExp.c:
```
int main(int argc, char * argv[]) {
    timeSeed();
    // E();
    int i;
    for (i=0; i<10; i++) {
        E(); #主程式每次產生10次E，10次運算式，並印出來
        printf("\n");
    }
}

// E=T ([+-] T)*  #可能是會繼續產生下去或是不會繼續產生下去
void E() {
    T();
    while (randInt(10) < 3) { #會繼續產生下去的機會是0.3，不繼續產生下去的機會是0.7
       printf("%c", randChar("+-")); #如果有產生下一個，便會從+-挑選一個出來
       T(); #繼續產生T()
    }
}

// T=F ([*/] F)?
void T() {
    F(); #產生F()或者F*/F，*/最多可一次
    if (randInt(10) < 7) {
        printf("%c", randChar("*/"));
        F();
    }
}

// F=[0-9] | (E)
void F() {
    if (randInt(10) < 8) {
        printf("%c", randChar("0123456789")); 可能會產生0123456789其中一個字
    } else {
        printf("("); 
        E();  #或是產生一個括號後面加 E()再接一個括號
        printf(")");
    }
}

```


## 如何去包含其他檔案:

```
#include <…> : 系統預設的函式庫資料夾
#include "…" : 自己目錄的資料夾
```


## MAC terminal 中文編碼問題解決:
### 修改终端的預設編碼、修改终端字體
### 使用UTF-8编码:
```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

```


## 02-軟體/07-系統程式/08-ipcchat/05-udp/chat2.c:


### 任何ID進來的封包都會接收
```
 saddr.sin_addr.s_addr = INADDR_ANY;
 
```

### 取得此結構的長度 ，sizeof在c語言中很常會運用到
```
 socklen_t rAddrLen = sizeof(struct sockaddr);
```

###  對方連線的請求

```
printf("receive: %s from client addr %s\n", msg, inet_ntoa(raddr.sin_addr));
```

### 不管server或client都會叫fork分裂成2個部分，一個負責接收訊息，一個負責送出訊息

### 這段是server和client一起共用的，sendto會送出訊息，recvfrom接收訊息

```
  if (fork() == 0) {
        // child: receive message and print
        while (1) {
            socklen_t rAddrLen = sizeof(struct sockaddr);
            recvfrom(sfd, msg, SMAX, 0, (struct sockaddr*) &raddr, &rAddrLen);
            printf("receive: %s", msg);
        }
    } else {
        // parent: readline and send msg
        while (1) {
            fgets(msg, SMAX, stdin);
            sendto(sfd, msg, strlen(msg)+1, 0, (struct sockaddr*) &raddr, sizeof(struct sockaddr));
        }
    }
```

## 02-軟體/07-系統程式/08-ipcchat/06-tcp/chat.c:

### TCP必須做listena這個動作，當對方的請求連線進來後，通過accept接受後，連線就開始建立，因為TCP是連線導向協定，直到斷線為止，此連線會一直存在，在client端方面，要用connect接受，在server端對應的是accept。

```
if (argc==1) { // server
        printf("I am server...\n");
        saddr.sin_addr.s_addr = INADDR_ANY;
        bind(sfd, (struct sockaddr*) &saddr, sizeof(struct sockaddr));
        listen(sfd, 1);
        socklen_t rAddrLen = sizeof(struct sockaddr);
        cfd = accept(sfd, (struct sockaddr*) &raddr, &rAddrLen);
        printf("accept: cfd=%d client addr %s\n", cfd, inet_ntoa(raddr.sin_addr));
        fd = cfd;
    } else { // client
        printf("I am client...\n");
        saddr.sin_addr.s_addr = inet_addr(argv[1]);
        connect(sfd, (struct sockaddr*) &saddr, sizeof(struct sockaddr));
        fd = sfd;
        printf("connect success: sfd=%d server addr=%s\n", sfd, inet_ntoa(saddr.sin_addr));
    }
```

### 這段與udp很相似，使用fork分裂成2個部分，一個接收一個送出，接收是使用recv，送出給receive
### 在TCP中使用 recv，而在UDP才是使用 recvfrom，不能混著使用，否則會接收不到訊息發生錯誤

```
if (fork() == 0) {
        // child: receive message and print
        while (1) {
            int n = recv(fd, msg, SMAX, 0);
            if (n <=0) break;
            printf("receive: %s", msg);
        }
    } else {
        // parent: readline and send msg
        while (1) {
            fgets(msg, SMAX, stdin);
            send(fd, msg, strlen(msg)+1, 0);
        }
    }
```
### TCP與UDP的差異:

![](https://drive.google.com/uc?export=view&id=11JsO1jg0-jVonzWSI-u0uC_WbxMY0SB7)


### 當Argc==1時，不用打參數，因為是為了要檢查
```
if(Argc==1) --> ./chat
if(Argc==2) -->./chat 127.0.0.1
```
### c語言缺點: 使用的套件常常不能掛平台，幾乎都是跟作業系統綁在一起，即使是sqlite普遍的套件也沒辦法直接掛在作業系統。
### c語言優點:可以使用作業系統上任何的函數，速度快。

## RISC-V指令集:
### RV32I: 基礎整數指令集(固定不變了)
### RV32M: 乘法和除法
### RV32F:單精度浮點操作(和RV32D:雙精度浮點操作)
### RV32A:原子操作
### RV32C:可選的壓縮擴展(對應32位元的RV32G)
### RV32B:基本擴展
### RV32V:向量擴展(SIMD)指令
### RV64G:RISC-V的64位地址版本

### RV32I 是必備的指令集，其他都可不支援。

### 以下是其指令與格式如下所式：
![](https://github.com/riscv2os/riscv2os/wiki/img/rv32i1.png)

## RISC-V 指令格式:
![](https://github.com/riscv2os/riscv2os/wiki/img/riscv_format32_2.png)
### 立即值的部分有時被分散成幾區，像是 S-Type 分為 imm[4:0]+imm[11:5]，而 B,J 等類型的指令，imm 被分為更多部分，這主要是為了相容與擴充性的考量，在用 Verilog 或 VHDL 設計電路時可以用 decoder 先將立即值組合成單一欄位，然後才開始執行該指令。


## hackcpu指令:

### A指令:功能為把一個數值傳送到cpu中的A暫存器，第一個為0就是A指令
### C指令:前面為111後面都是C指令

## 壓縮指令集:

### 為了提升RISC-V 處理器具有商業競爭力，指令集支援了壓縮模式，如果最後2碼aa 不是 11，那就是16位元的指令，反之，就是32位元以上指令。
![](https://github.com/riscv2os/riscv2os/wiki/img/riscv_format.png)

## 浮點指令集:

### 由第一行來決定是什麼指令，但有時候是第四行，所以1和4行要互相比較是否是一樣的

### 以下是單精度浮點指令 RV32F 的格式表:
![](https://github.com/riscv2os/riscv2os/wiki/img/rv32f.png)

### 雙精度 RV32D 的格式類似，如下表所示:
![](https://github.com/riscv2os/riscv2os/wiki/img/rv32d.png)


## 原子指令集:

### 作業系統為了讓 thread 或 process 能共享變數卻不會產生競爭情況，處理完再歸還回去，此時需要 RV32A《原子指令集》的支援。

### 其指令格式如下:

![](https://github.com/riscv2os/riscv2os/wiki/img/rv32a.png)
### 有時候編譯器為了速度起見，會調整一些指令的順序，這叫做錯序執行。但可能會造成問題，因此RISC-V 提供了 Fence.i 這樣的指令來避免錯誤產生。
### 如圖:
![](https://github.com/riscv2os/riscv2os/wiki/img/rvzext.png)


## 64 位元指令集:
### 對於 64 位元的架構，其基本指令和 32 位元相同，指令也仍然是 32 位元的架構，但是暫存器卻是 64 位元的。
## 如圖:
![](https://github.com/riscv2os/riscv2os/wiki/img/rv64isa.png)
### 上圖中的 word 代表 32 位元整數，doubleword 代表 64 位元整數。


## 假指令:
### 由於 RISC-V 的指令集相當精簡，因此其他處理器上具備的指令，在 RISC-V 不見得有對應的指令，就會有假指令的存在

### 如圖顯示，第一行是假指令，其中la rd=auipc rd，la其實是不存在，但必須用auipc rd來合成，需要假指令是因為進auipc rd這指令有效位元數不足，才會分成2個指令。

![](https://github.com/riscv2os/riscv2os/wiki/img/pseudo1.png)


### 如圖顯示， RISC-V 沒有移動 (mv) 之類的指令，mv是指暫存器的移動，使用 addi rs, rd, 0 這樣的指令可以做到mv移動，rd=rs+0，就等於移動。

![](https://github.com/riscv2os/riscv2os/wiki/img/pseudo2.png)







### mini-riscv-os/02-ContextSwitch/os.c:

```
#include "os.h"

#define STACK_SIZE 1024
reg_t task0_stack[STACK_SIZE];
#宣告2個結構並可保留2個內容
struct context ctx_os;
struct context ctx_task;

extern void sys_switch(); #宣告一個sys_switch()，連接到主程式

void user_task0(void)
{
	lib_puts("Task0: Context Switch Success !\n");
	while (1) {} // stop here.
}

int os_main(void)    #作業系統主程式
{
	lib_puts("OS start\n");
	ctx_task.ra = (reg_t) user_task0;
	ctx_task.sp = (reg_t) &task0_stack[STACK_SIZE-1];
	sys_switch(&ctx_os, &ctx_task);
	return 0;
}
```


### mini-riscv-os/02-ContextSwitch/start.s:
```
.equ STACK_SIZE, 8192

.global _start

_start:
    csrr a0, mhartid                # 讀取核心代號
    bnez a0, park                   # 若不是 0 號核心，跳到 park 停止
    la   sp, stacks + STACK_SIZE    # 0 號核心設定堆疊
    j    os_main                    # 0 號核心跳到主程式 os_main

park:
    wfi
    j park

stacks:
    .skip STACK_SIZE                # 分配堆疊空間
```

### mini-riscv-os/03-MultiTasking/sys.s:
```
sys_switch:
        ctx_save a0  # a0 => struct context *old  #a0指第0個參數，把目前CPU那些暫存器都存到a0(old)
        ctx_load a1  # a1 => struct context *new  #a1指第1個參數，把new載入，等於新的把整套換掉
        ret          # pc=ra; swtch to new task (new->ra) # ret會採取pc=ra此動作，前面2個動作把整套換掉，因此ra是新的，pc等於ra，會跳到新的之前返回位置去，就會切換過去
```



## 04-TimerInterrupt:
### Build & Run:
### 此程式是顯示出timer_handler(時間中斷)從1開始直接按下Ctrl-A and then X才會離開程式，每個間隔約0.1秒，以達到實現時間中斷的目的
### 主要目的為示範如何設定中斷向量，設定時間中斷使它固定時間發生。
```
$ make
riscv64-unknown-elf-gcc -nostdlib -fno-builtin -mcmodel=medany -march=rv32ima -mabi=ilp32 -T os.ld -o os.elf start.s sys.s lib.c timer.c os.c
$ make qemu
Press Ctrl-A and then X to exit QEMU
qemu-system-riscv32 -nographic -smp 4 -machine virt -bios none -kernel os.elf        
OS start
timer_handler: 1
timer_handler: 2
timer_handler: 3
timer_handler: 4
timer_handler: 5
QEMU: Terminated
```

### mini-riscv-os/04-TimerInterrupt/os.c:
### 此程式會產生無窮迴圈，一直顯示timer_handler:
### 這邊無窮迴圈什麼事情都沒做但會印出來，是因為有設定中斷函數、中斷時間，中斷時間到了會中斷一次，就會在設定下次的中斷時間，會不斷延續同樣的動作
```
#include "os.h"

int os_main(void)
{
	lib_puts("OS start\n");
	timer_init(); // 開始時間中斷
	while (1) {} //每次時間到就會觸發中斷
	return 0;
}

```

### mini-riscv-os/04-TimerInterrupt/timer.c:
### 有分三種模式，機器、使用者、特權等模式，此程式是執行在機器模式下，把機器模式裡的時間中斷向量改成sys_timer
```
#include "timer.h"

#define interval 10000000 // cycles; about 1 second in qemu.

void timer_init()
{
  // each CPU has a separate source of timer interrupts.
  int id = r_mhartid();

  // ask the CLINT for a timer interrupt.
  *(reg_t*)CLINT_MTIMECMP(id) = *(reg_t*)CLINT_MTIME + interval; #把下次中斷的時間設定好

  // set the machine-mode trap handler.
  w_mtvec((reg_t)sys_timer);   #下次中斷要做哪個函數設定好，設定好後，時間到就會中斷，就會把mepc儲存起來，再跳到sys_timer(組合語言那邊)。

  // enable machine-mode interrupts.
  w_mstatus(r_mstatus() | MSTATUS_MIE);

  // enable machine-mode timer interrupts.
  w_mie(r_mie() | MIE_MTIE);
}

static int timer_count = 0;  

reg_t timer_handler(reg_t epc, reg_t cause)  #時間中斷會透過sys_timer執行timer_handler
{

  reg_t return_pc = epc; #保存暫存器
  // disable machine-mode timer interrupts.
  w_mie(~((~r_mie()) | (1 << 7)));  #禁止中斷
  lib_printf("timer_handler: %d\n", ++timer_count);  #前面有設定 timer_count = 0 ，每次呼叫timer_handler時，timer_count就會加1，從1開始印
  #如果這行的程式碼是timer_count++，就會從0開始印，先取值在加
  int id = r_mhartid();
  *(reg_t *)CLINT_MTIMECMP(id) = *(reg_t *)CLINT_MTIME + interval; //設置下次中斷時間點，中斷時會呼叫sys_timer，繼續一樣的動作，這樣才會連續間隔時間印出timer_handler
  // enable machine-mode timer interrupts.
  w_mie(r_mie() | MIE_MTIE);   #允許中斷
  #至於為甚麼要禁止中斷再來允許中斷，此用意是不希望在處理中斷的時間之內又發生中斷，如果在處理中斷的時間又發生中斷，這種就做可從入式中斷，但在這程式是不允許的，因此要處理中斷的時候，一開始就要先禁止中斷，等到最後在允許中斷。
  return return_pc;
}
```
### mini-riscv-os/04-TimerInterrupt/sys.s:
### 原本是叫sys_switch，當時間中斷到時，會先讀取機器模式程式計數器備份和中斷原因，並呼叫timer_handler(c語言的函數)，再設定成mepc並還原，呼叫mret時會跳到原來的中斷
### 主要目的為保存暫存器，並呼叫c語言的timer_handler，在恢復暫存器，最後就返回，唯一有動作的地方是會在timer_handler這部分執行。
```
sys_timer:

	# call the C timer_handler(reg_t epc, reg_t cause)
	csrr	a0, mepc     #mepc=機器模式程式計數器備份，mepc是硬體發生中斷所產生的，但在哪裡發生中斷式不一定的
	csrr	a1, mcause   #mcause=機器中斷原因
	call	timer_handler  

	# timer_handler will return the return address via a0.
	csrw	mepc, a0    #設定成mepc，並還原

	mret # back to interrupt location (pc=mepc)   #當中斷時會自動儲存mepc，也就是呼叫mret時，pc=mepc，就會跳到原本被中斷的位置
```
### mini-riscv-os/04-TimerInterrupt/riscv.h:
```
static inline reg_t r_mhartid()
{
  reg_t x;
  asm volatile("csrr %0, mhartid" : "=r" (x) );  #asm指此括號裡面都是組合語言，volatile指這些組合語言可能會造成暫存器突然的改變，這些暫存器不能假設如果編譯器沒有動他就不會自己動，csrr函數指把內容讀取到x裡面
  return x;
}


static inline reg_t r_mstatus()  #r_mstatus指在讀取機器狀態
{
  reg_t x;
  asm volatile("csrr %0, mstatus" : "=r" (x) );
  return x;
}


static inline void w_mstatus(reg_t x)  # w_mstatus指在寫入機器狀態
{
  asm volatile("csrw mstatus, %0" : : "r" (x));  
}


static inline void w_mepc(reg_t x) #w_mepc指在寫入機器模式程式計數器備份，epc指當中斷時程式計數器會先丟給epc，等中斷完成後會把epc塞還給epc再跳回來
{
  asm volatile("csrw mepc, %0" : : "r" (x));
}


static inline reg_t r_mepc()  # r_mepc指在讀取機器模式程式計數器備份
{
  reg_t x;
  asm volatile("csrr %0, mepc" : "=r" (x));
  return x;
}

static inline void w_mscratch(reg_t x)  #mscratch指時間中斷臨時變數儲存的地方
{
  asm volatile("csrw mscratch, %0" : : "r" (x));
}


static inline void w_mtvec(reg_t x)  #mtvec指中斷向量，中斷向量儲存一些中斷位置
{
  asm volatile("csrw mtvec, %0" : : "r" (x));
}
剩下的部分都是為了暫存器的某些位元而使用的
```
## 此圖片在講自己的CPU本身有一套的暫存器，裡面有ra、sp...等，sys_switch所做的事情是把自己的CPU暫存器儲存到old裡，再把new新載入到自己的CPU裡。
![](https://drive.google.com/uc?export=view&id=1IvsigljeEKAmyJ7-amC4cSenbPgvwqW_)

### 電腦可以計時的原因，主要是因為主機板上會放石英振盪器來計時，其優點是很準時。
### mini-riscv-os/05-Preemptive0/timer.c:
```
#include "timer.h"
// a scratch area per CPU for machine-mode timer interrupts.
reg_t timer_scratch[NCPU][5];
#define interval 20000000 // cycles; about 2 second in qemu.
void timer_init()  #基本上跟04的部分差不多，只是有多一點暫存的功能
{
  int id = r_mhartid();
  *(reg_t *)CLINT_MTIMECMP(id) = *(reg_t *)CLINT_MTIME + interval;
  reg_t *scratch = &timer_scratch[id][0];
  scratch[3] = CLINT_MTIMECMP(id);
  scratch[4] = interval;
  w_mscratch((reg_t)scratch);
  // enable machine-mode timer interrupts.
  w_mie(r_mie() | MIE_MTIE);
}
static int timer_count = 0;
void timer_handler()
{
  lib_printf("timer_handler: %d\n", ++timer_count);
  int id = r_mhartid();
  *(reg_t *)CLINT_MTIMECMP(id) = *(reg_t *)CLINT_MTIME + interval;
}
```
### mini-riscv-os/05-Preemptive0/trap.c:
### 這邊的trap是指所有中斷但不包含軟體中斷

```
void trap_init()
{
  // set the machine-mode trap handler.
  w_mtvec((reg_t)trap_vector); #把trap_vector寫入並設定中斷向量

  // enable machine-mode interrupts.
  w_mstatus(r_mstatus() | MSTATUS_MIE);  #允許中斷
}

reg_t trap_handler(reg_t epc, reg_t cause)   #中斷一發生會呼叫trap_handle
{
  reg_t return_pc = epc;
  reg_t cause_code = cause & 0xfff;

  if (cause & 0x80000000)
  {
    /* Asynchronous trap - interrupt */
    switch (cause_code)
    {
    case 3:
      lib_puts("software interruption!\n"); #軟體中斷，但這邊不會處理
      break;
    case 7:  #設定好這些之後，當中斷發生時，就會呼叫trap_handler，會呼叫是因為有在trap_init設定了中斷發生時呼叫trap_handler，這跟時間中斷的設定是一樣的，把trap_vector設定上去。
    lib_puts("timer interruption!\n"); #時間中斷
      // disable machine-mode timer interrupts.  
      w_mie(~((~r_mie()) | (1 << 7))); #禁止時間中斷，為了避免重複中斷
      timer_handler(); #timer_handler呼叫後
      return_pc = (reg_t)&os_kernel; #至於這邊為什麼要把 return_pc設定成os_kernel，最後再傳回去，要看trap_handler那邊
      // enable machine-mode timer interrupts.
      w_mie(r_mie() | MIE_MTIE); #再來允許中斷，才不會有遞迴的重複中斷
      break;
    case 11:
      lib_puts("external interruption!\n"); #外部中斷
      break;
    default:
      lib_puts("unknown async exception!\n");
      break;
    }
  }

```
### mini-riscv-os/05-Preemptive0/user.c:
### 這邊沒甚麼改變，唯一就是不需要緩而已
```
lib_puts("Task1: Created!\n");
	while (1)
	{
		lib_puts("Task1: Running...\n");
		lib_delay(1000);
	}
```

### mini-riscv-os/05-Preemptive0/os.c:
### 其差異在於把時間中斷其中一部分改放在trap裡去執行，原本是只有時間中斷timer_init()，但為了可以模組化，且可以去支援除了時間中斷之外的中斷，因此就放入到trap
### 但實際上還是只有時間中斷，除了 timer interrupt以外都沒用，但此範例還是分成2個模組來使用
```
void os_start() #設定使用者形程、中斷向量、時間中斷等
{
	lib_puts("OS start\n");
	user_init();
	trap_init();
	timer_init(); // start timer interrupt ...
}
```
## 05-Preemptive :
### 最大改變是多一個trap模組，因為中斷不只有時間中斷，還有可能有其他中斷，例如:軟體中斷、外部中斷等，而外部中斷是指假設有個案例是按了鍵盤，因此要通知CPU說有人按了鍵盤要給予反硬，原因可能是有輸出入的中斷或是網路方面的中斷等，這些就是外部中斷，一開始提到了時間中斷比較偏向內部的，

### mini-riscv-os/05-Preemptive0/sys.s:
### 其重點是在trap_handler中，根據mcause才知道說是timer中斷還是其他中斷
### 進入到trap_handler 裡，會設定retrun_pc，接著又會設定到mepc，最後mret時，就會跳回給作業系統
```
trap_vector:  #中斷發生時，會先儲存暫存器，再呼叫trap_handler，最後再恢復
	# save context(registers).
	csrrw	t6, mscratch, t6	# swap t6 and mscratch
        reg_save t6
	csrw	mscratch, t6
	# call the C trap handler in trap.c
	csrr	a0, mepc
	csrr	a1, mcause
	call	trap_handler #會設定retrun_pc

	# trap_handler will return the return address via a0.
	csrw	mepc, a0 #回傳回去的retrun值會放在a0，然後又把a0寫成mepc，

	# load context(registers).
	csrr	t6, mscratch
	reg_load t6
	mret  #mret後會跳回mepc那邊，所以執行mret時，就會跳回kernel，也就完成把控制權交給kernel了
```



```
struct devsw devsw[NDEV];  #此結構在file.c裡面名叫NDEV
struct {
  struct spinlock lock;
  struct file file[NFILE];
} ftable;

//跟檔案表相關的函數都會集中在這裡，這邊也是作業系統進來必須執行的函數
void
fileinit(void)
{
  initlock(&ftable.lock, "ftable");  //要先設定一個鎖，避免之後會出現競爭的情況發生
}

// Allocate a file structure.
struct file*
filealloc(void)  //filealloc會分配檔案，會先從檔案表開頭執行到尾部，在執行過程中間如果看到有任何一個檔案表被引用的次數為0(表示無人使用)，就會設定成1(拿來使用)且回傳回來
{
  struct file *f;

  acquire(&ftable.lock);
  for(f = ftable.file; f < ftable.file + NFILE; f++){
    if(f->ref == 0){
      f->ref = 1;
      release(&ftable.lock);
      return f;
    }
  }
  release(&ftable.lock);
  return 0;
}
```


### 當我們呼叫 ``` write(1, buf, n) ``` 時，會執行下列組合語言指令
```
write:
 li a7, SYS_write
 ecall
 ret
```

### 並且呼叫後會放在以下syscalls的陣列
```
static uint64 (*syscalls[])(void) = {
[SYS_fork]    sys_fork,
[SYS_exit]    sys_exit,
[SYS_wait]    sys_wait,
[SYS_pipe]    sys_pipe,
[SYS_read]    sys_read,
[SYS_kill]    sys_kill,
[SYS_exec]    sys_exec,
[SYS_fstat]   sys_fstat,
[SYS_chdir]   sys_chdir,
[SYS_dup]     sys_dup,
[SYS_getpid]  sys_getpid,
[SYS_sbrk]    sys_sbrk,
[SYS_sleep]   sys_sleep,
[SYS_uptime]  sys_uptime,
[SYS_open]    sys_open,
[SYS_write]   sys_write,
[SYS_mknod]   sys_mknod,
[SYS_unlink]  sys_unlink,
[SYS_link]    sys_link,
[SYS_mkdir]   sys_mkdir,
[SYS_close]   sys_close,
};
```


### 一旦呼叫read函數就會跳到consoleread函數去執行
```
void
consoleinit(void)
{
  initlock(&cons.lock, "cons");

  uartinit();

  // connect read and write system calls
  // to consoleread and consolewrite.
  devsw[CONSOLE].read = consoleread; // CONSOLE 在 kernel/file.h 定義為 1
  devsw[CONSOLE].write = consolewrite;
}

```

### consolewrite() 會連續呼叫 n 次的 uartputc(c) 去輸出該字串

```
//
// user write()s to the console go here.
//
int
consolewrite(int user_src, uint64 src, int n)
{
  int i;

  for(i = 0; i < n; i++){
    char c;
    if(either_copyin(&c, user_src, src+i, 1) == -1)
      break;
    uartputc(c);
  }

  return i;
}
```

## 分頁表的優點:

### 1.簡化數據處理:能夠輕鬆處理大型數據集，而無需一次性加載所有數據
### 2.優化使用者體驗:通過將長列表分成多個頁面，使用者可以更輕鬆地瀏覽數據，並且頁面加載速度更快。
### 3.提高性能:處理大量數據時，將數據分成頁面可以減少頁面加載時間和服務器負載。

## xv6硬碟的分類:
### inode塊、數據塊
### 每個inode塊包含一個inode（索引節點），用於存儲文件的元數據，如文件類型、文件大小等。數據塊用於存儲文件的實際內容。

### 硬體將 logical address 轉成 physical address:
![image](https://github.com/byby9527/sp111b/assets/99935115/91a8c2a0-12f2-4d29-aea4-e89d656a2cb1)





