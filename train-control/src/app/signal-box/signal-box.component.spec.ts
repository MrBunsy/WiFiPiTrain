import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SignalBoxComponent } from './signal-box.component';

describe('SignalBoxComponent', () => {
  let component: SignalBoxComponent;
  let fixture: ComponentFixture<SignalBoxComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SignalBoxComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SignalBoxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
