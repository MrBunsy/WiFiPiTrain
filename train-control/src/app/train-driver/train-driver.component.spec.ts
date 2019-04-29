import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainDriverComponent } from './train-driver.component';

describe('TrainDriverComponent', () => {
  let component: TrainDriverComponent;
  let fixture: ComponentFixture<TrainDriverComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrainDriverComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrainDriverComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
