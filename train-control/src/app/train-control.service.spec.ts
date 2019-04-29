import { TestBed } from '@angular/core/testing';

import { TrainControlService } from './train-control.service';

describe('TrainControlService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TrainControlService = TestBed.get(TrainControlService);
    expect(service).toBeTruthy();
  });
});
