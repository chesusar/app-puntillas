#ifndef KALMAN_H
#define KALMAN_H

class kalman
{
private:
    double sampleTime;
    double p[2][2];
    double y;
    double s;
    double k[2];

public:
    double angulo;
    double rate;

    double q_angulo = 0.001;
    double q_rate = 0.003;
    double r_medida = 0.003;

    kalman(double sampleTime);
    double process(double inRate, double inAngulo);
};

#endif