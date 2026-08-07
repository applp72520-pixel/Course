#include <stdio.h>
#include "division.h"


float divide(float a, float b) {
    if (b != 0) {
        return a / b;
    } else {
        printf("Error:Division is displayed as  0\n");
        return 0;
    }
}
