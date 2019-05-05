import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Train, TrainControlService } from '../train-control.service';

/**
 * Component to provide a throttle and other controls
 */
@Component({
  selector: 'train-driver',
  templateUrl: './train-driver.component.html',
  styleUrls: ['./train-driver.component.css']
})
export class TrainDriverComponent implements OnInit {

  constructor(private trainControl: TrainControlService) {
    this.train = this.trainControl.getTrainState();

  }

  public train: Observable<Train>

  public changeSpeed(changeBy: number) {
    this.trainControl.changeSpeed(changeBy);
  }

  ngOnInit() {
  }

}
