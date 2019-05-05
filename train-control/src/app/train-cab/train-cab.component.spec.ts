import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainCabComponent } from './train-cab.component';

describe('TrainCabComponent', () => {
  let component: TrainCabComponent;
  let fixture: ComponentFixture<TrainCabComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrainCabComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrainCabComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
