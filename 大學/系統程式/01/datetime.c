#include "datetime.h"
#include <time.h>

void printCurrentTime() {
    time_t currentTime = time(NULL);//取得當前時間戳
    printf("Current time: %s", ctime(&currentTime));//顯示出現在的時間
}

void printFormattedTime(const char* format) {
    // 宣告一個 time_t 型態的變數 currentTime，並將其初始化為當前時間的時間戳
    time_t currentTime = time(NULL);
    
    //將 currentTime(當前時間) 的值轉換為本地時間的結構，並將結果儲存在 timeIn 指標所指向的記憶體位置
    struct tm* timeIn = localtime(&currentTime);

    char buffer[100];
    
    // 使用 strftime 函式將時間按照指定的 format 格式轉換並存儲到 buffer 陣列中
    strftime(buffer, sizeof(buffer), format, timeIn);
    
    printf("Formatted time: %s\n", buffer);
}
