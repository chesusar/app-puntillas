#ifndef VECTOR3_H
#define VECTOR3_H

class Vector3
{
public:
    float x;
    float y;
    float z;

    Vector3(float _x, float _y, float _z);
    float getAngleX();
    float getAngleY();

private:
    int cuadrante(float x, float y);
};

#endif