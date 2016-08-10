# Copyright (C) 2012 Kristian Lauszus, TKJ Electronics. All rights reserved.
# This software may be distributed and modified under the terms of the GNU
# General Public License version 2 (GPL2) as published by the Free Software
# Foundation and appearing in the file GPL2.TXT included in the packaging of
# this file. Please note that GPL2 Section 2[b] requires that all works based
# on this software must also be made publicly available under the terms of
# the GPL2 ("Copyleft").
# Contact information
# -------------------
# Kristian Lauszus, TKJ Electronics
# Web      :  http://www.tkjelectronics.com
# e-mail   :  kristianl@tkjelectronics.com
 

#

class kalmanFilter():
    # We will set the variables like so, these can also be tuned by the user */
    Q_angle = 0.0
    Q_bias = 0.0
    R_measure = 0.0

    angle = 0.0 # Reset the angle
    bias = 0.0 # Reset bias

    P00 = 0.0  # Since we assume that the bias is 0 and we know the starting angle (use setAngle), the error covariance matrix is set like so - see: http://en.wikipedia.org/wiki/Kalman_filter#Example_application.2C_technical
    P01 = 0.0
    P10 = 0.0
    P11 = 0.0
    rate = 0.0
    def __init__(self,  initAngle = 0.001,  initBias = 0.003,  initR_measure = 0.03):
        self.Q_angle = initAngle
        self.Q_bias = initBias
        self.R_measure = initR_measure

        self.angle = 0.0 # Reset the angle
        self.bias = 0.0 # Reset bias

        self.P00 = 0.0 # Since we assume that the bias is 0 and we know the starting angle (use setAngle), the error covariance matrix is set like so - see: http://en.wikipedia.org/wiki/Kalman_filter#Example_application.2C_technical
        self.P01 = 0.0
        self.P10  = 0.0
        self.P11 = 0.0

        self.rate = 0.0

    # The angle should be in degrees and the rate should be in degrees per second and the delta time in seconds
    def getAngle(self,  newAngle,  newRate,  dt):
        # KasBot V2  -  Kalman filter module - http://www.x-firm.com/?page_id=145
        # Modified by Kristian Lauszus
        # See my blog post for more information: http://blog.tkjelectronics.dk/2012/09/a-practical-approach-to-kalman-filter-and-how-to-implement-it

        # Discrete Kalman filter time update equations - Time Update ("Predict")
        # Update xhat - Project the state ahead
        # Step 1 */
        self.rate = newRate - self.bias
        self.angle += dt * self.rate

        # Update estimation error covariance - Project the error covariance ahead
        #sttep 2 */
        self.P00 += dt * (dt*self.P11 - self.P01 - self.P10 + self.Q_angle)
        self.P01 -= dt * self.P11
        self.P10 -= dt * self.P11
        self.P11 += self.Q_bias * dt

        # Discrete Kalman filter measurement update equations - Measurement Update ("Correct")
        # Calculate Kalman gain - Compute the Kalman gain
        # Step 4 */
        S = self.P00 + self.R_measure # Estimate error
        # Step 5 */
        # Kalman gain - This is a 2x1 vector
        K0 = self.P00 / S
        K1 = self.P10 / S

        # Calculate angle and bias - Update estimate with measurement zk (newAngle)
        # Step 3 */
        y = newAngle - self.angle # Angle difference
        # Step 6 */
        self.angle += K0 * y
        self.bias += K1 * y

        # Calculate estimation error covariance - Update the error covariance
        # Step 7 */
        P00_temp = self.P00
        P01_temp = self.P01

        self.P00 -= K0 * P00_temp;
        self.P01 -= K0 * P01_temp;
        self.P10 -= K1 * P00_temp;
        self.P11 -= K1 * P01_temp;

        return self.angle;
        
        
    def setAngle(self, newAngle) :
        self.angle = newAngle # Used to set angle, this should be set as the starting angle
    def getRate(self) :
        return self.rate # Return the unbiased rate

# These are used to tune the Kalman filter */
    def setQangle(self,  newQ_angle):
        self.Q_angle = newQ_angle
    def setQbias(self,  newQ_bias):
        self.Q_bias = newQ_bias
    def setRmeasure(self, newR_measure):
        self.R_measure = newR_measure

    def getQangle(self):
        return self.Q_angle
    def getQbias(self):
        return self.Q_bias
    def getRmeasure(self):
       return self.R_measure
