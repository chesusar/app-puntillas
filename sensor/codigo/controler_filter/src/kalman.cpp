#include "kalman.h"

kalman::kalman(double _sampleTime)
{
    sampleTime = _sampleTime;
    p[0][0] = 0;
    p[0][1] = 0;
    p[1][0] = 0;
    p[1][1] = 0;
    angulo = 0.0;
    rate = 0.0;
}

double kalman::process(double inRate, double inAngulo)
{
    // A priori
    angulo += sampleTime * (inRate - rate);
    // Covarianza del error
    p[0][0] += sampleTime * (sampleTime * p[1][1] - p[0][1] - p[1][0] + q_angulo);
    p[0][1] -= sampleTime * p[1][1];
    p[1][0] -= sampleTime * p[1][1];
    p[1][1] += sampleTime * q_rate;
    // Innovación
    y = inAngulo - angulo;
    s = p[0][0] + r_medida;
    // Ganancia de Kalman
    if (s != 0.0)
    {
        k[0] = p[0][0] / s;
        k[1] = p[1][0] / s;
    }
    // A posteriori
    angulo += k[0] * y;
    rate += k[1] * y;
    // A posteriori Covarianza del error
    double p00 = p[0][0];
    double p01 = p[0][1];

    p[0][0] -= k[0] * p00;
    p[0][1] -= k[0] * p01;
    p[1][0] -= k[1] * p00;
    p[1][1] -= k[1] * p01;

    return angulo;
}