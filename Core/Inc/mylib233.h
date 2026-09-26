#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stm32f1xx_hal.h"

extern UART_HandleTypeDef huart1;

extern char DbgPrint_Buffer[];
extern char UART_Recieve_Buffer[];

#define DbgPrint(...) \
  sprintf(DbgPrint_Buffer, __VA_ARGS__); \
  HAL_UART_Transmit(&huart1, (uint8_t*)DbgPrint_Buffer, strlen(DbgPrint_Buffer), 1000)

#define Quick_Update_TIM_PWM_Pulse(htim, Channel, Pulse) \
  __HAL_TIM_SET_COMPARE(htim, Channel, Pulse)

#define Quick_Read_GPIO_Pin(GPIOx, Pin) \
  ((GPIOx->IDR & Pin) == Pin)

#define Quick_Write_GPIO_Pin(GPIOx, Pin, Value) \
  GPIOx->BSRR = (uint32_t)(Pin * Value) | ((uint32_t)((~(Pin * Value)) & Pin) << 16)

void myUART_RxHandler(UART_HandleTypeDef *huart);
void softmoe_update_pwm();

extern TIM_HandleTypeDef htim1;
extern TIM_HandleTypeDef htim2;