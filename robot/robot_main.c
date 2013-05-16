#include "util.c"

//drive values
float dst_r;
float dst_l;
float vel_r;
float vel_l;

//const values
float cmd_dst;
float cmd_angle;
float max_a;
float max_v;

//last vals
float prev_t;
float prev_dst_r;
float prev_dst_l;
float prev_acc_r;
float prev_acc_l;

void reset(){
}
void run(){
	nMaxRegulatedSpeedNxt = 500;
	while(true){
		if(nMotorEncoder[motorA] > 360){
				right_dist += 1;
		}
		if(nMotorEncoder[motorB] > 360){
				left_dist += 1;
		}
		if(vel_r < max_vel){

		}
		if(vel_l < max_vel){

		}
		motor[motorA] = mtrSpeedReg;
		motor[motorB] = mtrSpeedReg;
		motor[motorA] = vel_r;
		motor[motorB] = vel_l;
		wait1Msec(1);
	}
}
task main()
{
	run();
}
