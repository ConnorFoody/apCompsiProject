#include "drive_control.h"


void Lock();
void Unlock();
void Update();
// random utility values
float prev_t;
TSemaphore m_lock;

// old storage values
float prev_vel_r;
float prev_vel_l;
void Lock(){
	SemaphoreLock( m_lock );
}
void Unlock(){
	SemaphoreUnlock( m_lock );
}
void Update(){

}
task drv_main(){
	Update();
}
