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
  private wsavc: WsAvcPlayer = null;
  private playing = false;

  @ViewChild("canvasElement") canvasElement: ElementRef;

  constructor() { }

  ngOnInit() {
  }


  public startStream() {
    this.wsavc.playStream();
    this.playing = true;
  }

  public stopStream() {
    if (this.playing) {
      this.wsavc.stopStream();
      this.playing = false;
    }
  }


  public restartStream() {
    if (this.playing) {
      this.wsavc.stopStream();
    }
    this.wsavc.playStream();
    this.playing = true;
  }

  ngAfterViewInit(): void {

    this.canvas = this.canvasElement.nativeElement;
    this.wsavc = new WsAvcPlayer(this.canvas, "webgl", 1, 35);
    this.wsavc.connect("ws://" + document.location.host + "/ws");
    let self = this;
    //TODO wait for websocket to be ready
    //can't decide if I want to auto-connect or not. Ideally should fix multiple viewers first (works, but not threaded carefully enough)
    // setTimeout(function () { self.startStream(); }, 3000);

  }

}
