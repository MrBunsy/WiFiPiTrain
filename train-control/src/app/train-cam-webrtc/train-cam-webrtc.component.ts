import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';

// declare class WebSocketSignalingChannel: any;
declare var WebSocketSignalingChannel: any;
/***
 * Component to display a webrtc camera stream from the pi camera
 */
@Component({
  selector: 'train-cam-webrtc',
  templateUrl: './train-cam-webrtc.component.html',
  styleUrls: ['./train-cam-webrtc.component.css']
})
export class TrainCamWebrtcComponent implements OnInit, AfterViewInit {

  private websocketSig: any;
  private video: HTMLVideoElement;

  @ViewChild("remoteVideo") videoElement: ElementRef;
  @ViewChild("connectButton") connectButton: ElementRef;
  @ViewChild("disconnectButton") disconnectButton: ElementRef;

  constructor() { }

  ngOnInit() {
  }

  ngAfterViewInit(): void {

    this.video = this.videoElement.nativeElement;

    this.websocketSig = new WebSocketSignalingChannel(this.connectButton.nativeElement, this.disconnectButton.nativeElement, this.video)

    if (this.video.hasAttribute("controls")) {
      this.video.removeAttribute("controls")
    }
  }

}
