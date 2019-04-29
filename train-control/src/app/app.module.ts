import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { TrainDriverComponent } from './train-driver/train-driver.component';
import { TrainControlService } from './train-control.service';

@NgModule({
  declarations: [
    TrainDriverComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule

  ],
  providers: [TrainControlService],
  bootstrap: [TrainDriverComponent]
})
export class AppModule { }
