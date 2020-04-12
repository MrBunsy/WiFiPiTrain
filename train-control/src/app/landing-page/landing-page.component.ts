import { Component, OnInit } from '@angular/core';
import { PointControlService } from '../point-control.service';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {

  constructor(private points: PointControlService) { }

  ngOnInit() {
  }

}
