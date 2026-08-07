#include <stdio.h>
#include "datetime.h"

int main(void)
{
    printCurrentTime();
    printFormattedTime("%Y-%m-%d %H:%M:%S");
    
    return 0;
}
