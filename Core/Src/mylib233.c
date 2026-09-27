#include "mylib233.h"

char DbgPrint_Buffer[1024] = {0};
uint8_t Buffer_A[1024] = {0};
uint8_t Buffer_B[1024] = {0};
uint8_t play_buf_id = 0;
uint16_t *analogValue = (uint16_t *)Buffer_A;

extern TIM_HandleTypeDef htim1;

void myUART_RxHandler(UART_HandleTypeDef *huart)
{
    static int i = 0;
    if (play_buf_id == 0) // we are writing to Buffer_B while playing from Buffer_A
    {
        Buffer_B[i] = huart->Instance->DR & 0xFF;
        if (i == sizeof(Buffer_B) - 1) // Buffer_B is full, now play
        {
            play_buf_id = 1;
            analogValue = (uint16_t *)Buffer_B;
        }
    }
    else // we are writing to Buffer_A while playing from Buffer_B
    {
        Buffer_A[i] = huart->Instance->DR & 0xFF;
        if (i == sizeof(Buffer_A) - 1) // Buffer_A is full, now play
        {
            play_buf_id = 0;
            analogValue = (uint16_t *)Buffer_A;
        }
    }
    i = (i + 1) % sizeof(Buffer_A);
}

void HAL_Delay(uint32_t Delay)
{
    uint32_t tickstart = uwTick;

    /* Add a freq to guarantee minimum wait */
    if (Delay < HAL_MAX_DELAY) Delay += (uint32_t)(uwTickFreq);

    while ((uwTick - tickstart) < Delay)
        asm volatile ("wfi");
}

void play_tick()
{
    static int i = 0;
    Quick_Update_TIM_PWM_Pulse(&htim1, TIM_CHANNEL_1, analogValue[i]);
    i = (i + 1) % 512;
}