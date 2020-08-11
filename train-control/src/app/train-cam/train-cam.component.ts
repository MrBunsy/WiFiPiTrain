import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';

import * as WsAvcPlayer from 'h264-live-player';
/***
 * Component to display a webrtc camera stream from the pi camera
 */
@Component({
  selector: 'train-cam',
  templateUrl: './train-cam.component.html',
  styleUrls: ['./train-cam.component.css']
})
export class TrainCamComponent implements OnInit, AfterViewInit {

  private canvas: HTMLCanvasElement;
  private wsavc: WsAvcPlayer;

  @ViewChild("canvasElement") canvasElement: ElementRef;

  constructor() { }

  ngOnInit() {
  }

  public playStream() {
    this.wsavc.playStream();

  }
  public stopStream() {
    this.wsavc.stopStream();
  }
  public disconnect() {
    this.wsavc.disconnect();
  }

  ngAfterViewInit(): void {

    this.canvas = this.canvasElement.nativeElement;
    this.wsavc = new WsAvcPlayer(this.canvas, "webgl", 1, 35);
    this.wsavc.connect("ws://" + document.location.host + "/ws");
  }

}
