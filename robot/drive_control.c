#include "drive_control.h"

/**********************************
 * 	CHANGE THESE CONSTANTS:
 **********************************/
 float x; //Declare your variables
 float y; //Declare your variables Brett
/***********************************
 * 
 ***********************************/
task drive(){
        long prev_val = 0;
        long curr_val = 0;

        float spd = 0;
        nMotorEncoder[motorA] = 0;
        nMotorEncoder[motorB] = 0;
	
	float kP = .5;
        float kI = .001;
        float kD = .05;
        float err_i = 0.0;
        float prev = 0.0;
        float c_x = 0;
        float c_y = 0;
        
        kT = 0.0;
        float wheel_d = 0;
        float robot_r = 0;
        
        while( c_x < x * .75){ // go three quarters of the way to the target, then turn onto the target
        	c_x = nMotorEncoder[motorA] + nMotorEncoder[motorB];
        	c_x = c_x / 2.0; // find the straight dist
        	
        	float err = (x * .75) - c_x; 
        	if(fabs(err_i * kI) > 100){
        		// limit windup
        		err_i = (fabs(err_i) / err_i) * 100 / kI; 
        	}
        	float out = kP*(err) + kI*(err_i) kD*(err- prev);
        	perv = err; 
        	err_i += err;
        	float diff = nMotorEncoder[motorA] - nMotorEncoder[motorB];
        	diff = diff / robot_r; 
        	
        	motor[motorA] = out + kT*(diff); 
        	motor[motorB] = out - kT*(diff);
        }
        kP = 0.0;
        kI = 0.0;
        kD = 0.0;
        err_i = 0; 
        prev = 0;
        nMotorEncoder[motorA] = 0;
        nMotorEncoder[motorB] = 0;
        
        float theta_goal = atan( y / (x - c_x));
        float theta = 0;
        while(theta < theta_goal){
        	theta = (nMotorEncoder[motorA] - nMotorEncoder[motorB]) / r;
        	float err = (x * .75) - c_x; 
        	if(fabs(err_i * kI) > 100){
        		// limit windup
        		err_i = (fabs(err_i) / err_i) * 100 / kI; 
        	}
        	float err = theta_goal - theta; 
        	float out = kP*(err) + kI*(err_i) kD*(err- prev);
        	prev = err; 
        	err_i += err;
        	motor[motorA] = out; 
        	motor[motorB] = -out; 
        }
        
        kP = 0.0;
        kI = 0.0;
        kD = 0.0;
        err_i = 0; 
        prev = 0;
        nMotorEncoder[motorA] = 0;
        nMotorEncoder[motorB] = 0;
        
        float dist_left = pow(x - c_x, 2) + pow(y, 2); 
        dist_left = sqrt(dist_left);
        c_x = 0.0;
        while(c_x < dist_left){
        	c_x = nMotorEncoder[motorA] + nMotorEncoder[motorB];
        	c_x = c_x / 2.0; // find the straight dist
        	
        	float err = (x * .75) - c_x; 
        	if(fabs(err_i * kI) > 100){
        		// limit windup
        		err_i = (fabs(err_i) / err_i) * 100 / kI; 
        	}
        	float out = kP*(err) + kI*(err_i) kD*(err- prev);
        	perv = err; 
        	err_i += err;
        	float diff = nMotorEncoder[motorA] - nMotorEncoder[motorB];
        	diff = diff / robot_r; 
        	
        	motor[motorA] = out + kT*(diff); 
        	motor[motorB] = out - kT*(diff);
        }
        motor[motorA] = 0;
        motor[motorB] = 0;
}
void initDrive(){
        bFloatDuringInactiveMotorPWM =false;
        nMaxRegulatedSpeedNxt = 750;
        nMotorPIDSpeedCtrl[motorA] = mtrSpeedReg;
        mMotorPIDSpeedCtrl[motorB] = mtrSpeedReg;
        bMotorReflected[motorB] = true;
}
task main(){
        initDrive();
        StartTask(drive);
}
