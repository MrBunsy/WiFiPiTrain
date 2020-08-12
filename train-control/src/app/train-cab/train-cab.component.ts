import { Component, OnInit } from '@angular/core';
import { TrainControlService } from '../train-control.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

/**
 * component to combine a throttle (TrainDriver) with a TrainCam
 */
@Component({
  selector: 'train-cab',
  templateUrl: './train-cab.component.html',
  styleUrls: ['./train-cab.component.css']
})
export class TrainCabComponent implements OnInit {

  public hasCamera$: Observable<boolean>;

  constructor(private train: TrainControlService) {

    this.hasCamera$ = this.train.getTrainState().pipe(
      map(train => train.hasCamera)
    );

  }

  ngOnInit() {
  }

}
