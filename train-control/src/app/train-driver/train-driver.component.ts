import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Train, TrainControlService } from '../train-control.service';
import { map } from 'rxjs/operators';
import { MatSliderChange } from '@angular/material';

/**
 * Component to provide a throttle and other controls
 */
@Component({
  selector: 'train-driver',
  templateUrl: './train-driver.component.html',
  styleUrls: ['./train-driver.component.css']
})
export class TrainDriverComponent implements OnInit {
  public train: Observable<Train>
  public currentSpeed$: Observable<number>

  constructor(private trainControl: TrainControlService) {
    this.train = this.trainControl.getTrainState();

    this.currentSpeed$ = this.train.pipe(
      map(train => Math.round(100 * train.speed) / 100)
    )

  }

  public sliderChanged(event: MatSliderChange) {
    console.log(event)
    this.trainControl.setTrainSpeed(event.value);
  }

  public changeSpeed(changeBy: number) {
    this.trainControl.changeSpeed(changeBy);
  }
  public stop() {
    this.trainControl.setTrainSpeed(0);
  }

  public mouseWheelUpFunc(event) {
    console.log(event)
    this.trainControl.changeSpeed(+0.02)

  }
  public mouseWheelDownFunc(event) {
    this.trainControl.changeSpeed(-0.02)
  }

  ngOnInit() {
  }

}
