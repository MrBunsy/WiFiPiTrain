import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { TrainDriverComponent } from './train-driver/train-driver.component';
import { TrainControlService } from './train-control.service';
import { AppComponent } from './app.component';
import { TrainCamComponent } from './train-cam/train-cam.component';
import { TrainCabComponent } from './train-cab/train-cab.component';

@NgModule({
  declarations: [
    TrainDriverComponent,
    AppComponent,
    TrainCamComponent,
    TrainCabComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule

  ],
  providers: [TrainControlService],
  bootstrap: [AppComponent]
})
export class AppModule { }
