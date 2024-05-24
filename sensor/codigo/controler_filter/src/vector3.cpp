#include "vector3.h"
#include <Arduino.h>

Vector3::Vector3(float _x, float _y, float _z)
{
    x = _x;
    y = _y;
    z = _z;
}

float Vector3::getAngleX()
{
    float accelX = y;
    float accelY = z;
    int c = cuadrante(accelX, accelY);
    if (c == 1)
        return atan(accelY / accelX) * 360.0 / (2.0 * 3.1416);
    if (c == 2)
        return atan(accelY / accelX) * 360.0 / (2.0 * 3.1416) + 180;
    if (c == 3)
        return atan(accelY / accelX) * 360.0 / (2.0 * 3.1416) + 180;
    else
        return atan(accelY / accelX) * 360.0 / (2.0 * 3.1416) + 360;
}

float Vector3::getAngleY()
{
    float accelX = x;
    float accelY = z;
    int c = cuadrante(accelX, accelY);
    if (c == 1)
        return atan(accelY / accelX) * 360.0 / (2.0 * 3.1416);
    if (c == 2)
        return atan(accelY / accelX) * 360.0 / (2.0 * 3.1416) + 180;
    if (c == 3)
        return atan(accelY / accelX) * 360.0 / (2.0 * 3.1416) + 180;
    else
        return atan(accelY / accelX) * 360.0 / (2.0 * 3.1416) + 360;
}

int Vector3::cuadrante(float x, float y)
{
    if (x > 0)
    {
        if (y > 0)
            return 1;
        else
            return 4;
    }
    else
    {
        if (y > 0)
            return 2;
        else
            return 3;
    }
}