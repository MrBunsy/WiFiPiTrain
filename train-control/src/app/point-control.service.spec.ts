import { TestBed } from '@angular/core/testing';

import { PointControlService } from './point-control.service';

describe('PointControlService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: PointControlService = TestBed.get(PointControlService);
    expect(service).toBeTruthy();
  });
});
