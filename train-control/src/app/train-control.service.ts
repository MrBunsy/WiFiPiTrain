import { Injectable } from '@angular/core';
import { HttpClient } from 'selenium-webdriver/http';
import { BehaviorSubject, Observable, combineLatest } from 'rxjs';
import { switchMap } from 'rxjs/operators';

export class Train {
  public speed: number;
  //todo lights
}

@Injectable({
  providedIn: 'root'
})
export class TrainControlService {

  /**
   * We need to go and fetch new motor state
   */
  private trainUpdated: BehaviorSubject<boolean>
  private trainState: Observable<Train>;

  constructor(private http: HttpClient) {

    this.trainUpdated = new BehaviorSubject<boolean>(true);

    this.trainState = this.trainUpdated.asObservable().pipe(
      switchMap(updated => this.getTrainState())
    )


  }

  public getTrainState(): Observable<Train> {
    return this.trainState;
  }


  /**
   * perform HTTP request to get latest train state
   */
  private fetchTrainState(): Observable<Train> {

  }
}
