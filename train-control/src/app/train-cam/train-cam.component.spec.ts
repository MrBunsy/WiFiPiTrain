import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainCamComponent } from './train-cam.component';

describe('TrainCamComponent', () => {
  let component: TrainCamComponent;
  let fixture: ComponentFixture<TrainCamComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrainCamComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrainCamComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
