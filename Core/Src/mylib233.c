#include "mylib233.h"

char DbgPrint_Buffer[1024] = {0};
uint8_t UART_Recieve_Buffer[2] = {0};

void myUART_RxHandler(UART_HandleTypeDef *huart)
{
    static int i = 0;
    UART_Recieve_Buffer[i] = huart->Instance->DR & 0xFF;
    DbgPrint("Received: %d\r\n", UART_Recieve_Buffer[i]);
    i = (i + 1) % sizeof(UART_Recieve_Buffer);
}

void HAL_Delay(uint32_t Delay)
{
    uint32_t tickstart = uwTick;

    /* Add a freq to guarantee minimum wait */
    if (Delay < HAL_MAX_DELAY) Delay += (uint32_t)(uwTickFreq);

    while ((uwTick - tickstart) < Delay)
        asm volatile ("wfi");
}