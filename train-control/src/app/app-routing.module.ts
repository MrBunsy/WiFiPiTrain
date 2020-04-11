import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TrainDriverComponent } from './train-driver/train-driver.component';
import { TrainCabComponent } from './train-cab/train-cab.component';
import { SignalBoxComponent } from './signal-box/signal-box.component';

const routes: Routes = [
  { path: '', redirectTo: 'cab', pathMatch: 'full' },
  { path: 'cab', component: TrainCabComponent },
  { path: 'drive', component: TrainDriverComponent },
  { path: 'signalbox', component: SignalBoxComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
