import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainCamWebrtcComponent } from './train-cam-webrtc.component';

describe('TrainCamComponent', () => {
  let component: TrainCamWebrtcComponent;
  let fixture: ComponentFixture<TrainCamWebrtcComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrainCamWebrtcComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrainCamWebrtcComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
