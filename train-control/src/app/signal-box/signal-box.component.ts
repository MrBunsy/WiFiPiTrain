import { Component, OnInit } from '@angular/core';
import { Point, PointControlService } from '../point-control.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'signal-box',
  templateUrl: './signal-box.component.html',
  styleUrls: ['./signal-box.component.css']
})
export class SignalBoxComponent implements OnInit {

  public points$: Observable<Point[]>

  constructor(private points: PointControlService) {
    this.points$ = this.points.getPoints();
   }

  ngOnInit() {
  }

}
