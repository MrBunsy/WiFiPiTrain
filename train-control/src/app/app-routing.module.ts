import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TrainDriverComponent } from './train-driver/train-driver.component';

const routes: Routes = [
  { path: '', redirectTo: 'drive', pathMatch: 'full' },
  { path: 'drive', component: TrainDriverComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
