#include "mylib233.h"

char DbgPrint_Buffer[1024] = {0};
uint8_t UART_Recieve_Buffer[2] = {0};
uint16_t *analogValue = (uint16_t*)UART_Recieve_Buffer;

extern TIM_HandleTypeDef htim1;

void myUART_RxHandler(UART_HandleTypeDef *huart)
{
    static int i = 0;
    UART_Recieve_Buffer[i] = huart->Instance->DR & 0xFF;
    //DbgPrint("Received: %x\r\n", UART_Recieve_Buffer[i]);
    if (i == 1) {
        //DbgPrint("Analog Value: %d/65535\r\n", *analogValue);
        // calc the PWM
        uint16_t pwmValue = (uint32_t)(*analogValue) * htim1.Instance->ARR / 65535;
        //DbgPrint("PWM Value: %d\r\n", pwmValue);
        Quick_Update_TIM_PWM_Pulse(&htim1, TIM_CHANNEL_1, *analogValue);
    }
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