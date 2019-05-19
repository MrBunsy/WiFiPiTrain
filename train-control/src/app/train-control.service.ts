import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, combineLatest, interval, merge, Subject } from 'rxjs';
import { switchMap, tap, first } from 'rxjs/operators';

export class Train {
  public speed: number;
  //todo lights
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class TrainControlService {

  /**
   * We need to go and fetch new motor state
   */
  private trainUpdated: Subject<Train>
  private trainState: Observable<Train>;
  private trainUrl: string;



  constructor(private http: HttpClient) {

    this.trainUrl = "/train/";

    this.trainUpdated = new Subject<Train>();

    let checkForUpdates = interval(1000);

    let updatingTrain = checkForUpdates.pipe(
      switchMap(now => this.fetchTrainState())
    )

    this.trainState = merge(this.trainUpdated.asObservable(), updatingTrain);


  }

  public getTrainState(): Observable<Train> {
    return this.trainState;
  }

  public setTrainSpeed(speed: number) {
    this.setTrainSpeedRequest(speed).pipe(first()).toPromise().then();
  }

  private setTrainSpeedRequest(speed: number): Observable<Train> {
    let request = this.http.post<Train>(this.trainUrl, { speed: speed }, httpOptions).pipe(
      // tap((newHero: Hero) => this.log(`added hero w/ id=${newHero.id}`)),
      // catchError(this.handleError<Hero>('addHero'))
      tap(train => this.trainUpdated.next(train))
    );

    return request;

  }

  public changeSpeed(changeBy: number) {
    let request = this.fetchTrainState().pipe(
      tap(train => console.log("current train speed: " + train.speed + " request change of " + changeBy)),
      switchMap(train => this.setTrainSpeedRequest(train.speed + changeBy)),

    ).pipe(first()).toPromise().then();
  }


  /**
   * perform HTTP request to get latest train state
   */
  private fetchTrainState(): Observable<Train> {
    let trainHTTP = this.http.get<Train>(
      this.trainUrl)

    return trainHTTP;

  }

}
