import { Component, OnInit, Input } from '@angular/core';
import { PointControlService, Point } from '../point-control.service';

@Component({
  selector: 'point-lever',
  templateUrl: './point-lever.component.html',
  styleUrls: ['./point-lever.component.css']
})
export class PointLeverComponent implements OnInit {

  @Input() point: Point;


  constructor(private points: PointControlService) { }

  ngOnInit() {
  }

  public setPosition(position: number){
    this.points.setPointPosition(this.point.index, position);
  }

}
