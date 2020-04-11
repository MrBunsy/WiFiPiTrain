import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PointLeverComponent } from './point-lever.component';

describe('PointLeverComponent', () => {
  let component: PointLeverComponent;
  let fixture: ComponentFixture<PointLeverComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PointLeverComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PointLeverComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
