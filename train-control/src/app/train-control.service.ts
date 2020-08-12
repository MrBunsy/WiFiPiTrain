import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject, Observable, combineLatest, interval, merge, Subject, throwError, of } from 'rxjs';
import { switchMap, tap, first, catchError, retry, share, map } from 'rxjs/operators';
import { ServerResponse } from './point-control.service';

export class Train {
  public speed: number = 0;
  public deadZone: number = 0;
  public reverse: boolean = false;
  public headlights: boolean = false;
  public hasHeadlights: boolean = false;
  public hasCamera: boolean = false;
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

    this.trainState = merge(this.trainUpdated.asObservable(), updatingTrain).pipe(
      share()
    );


  }

  public getTrainState(): Observable<Train> {
    return this.trainState;
  }

  public setTrainSpeed(speed: number) {

    this.setTrainSpeedRequest(speed).pipe(first()).toPromise().then();
  }

  public setReverse(reverse: boolean) {
    this.setTrainReverseRequest(reverse).pipe(first()).subscribe();
  }

  public setHeadlights(headlights: boolean) {
    this.setTrainHeadlightsRequest(headlights).pipe(first()).subscribe();
  }

  private setTrainReverseRequest(reverse: boolean): Observable<Train> {
    return this.http.post<ServerResponse>(this.trainUrl, { reverse: reverse }, httpOptions).pipe(
      //since we get the current train state in reply to any change request, make use of it
      map(response => response.train),
      tap(train => this.trainUpdated.next(train))
    );
  }

  private setTrainHeadlightsRequest(headlights: boolean): Observable<Train> {
    return this.http.post<ServerResponse>(this.trainUrl, { headlights: headlights }, httpOptions).pipe(
      //since we get the current train state in reply to any change request, make use of it
      map(response => response.train),
      tap(train => this.trainUpdated.next(train))
    );
  }

  private setTrainSpeedRequest(speed: number): Observable<Train> {
    let request = this.http.post<ServerResponse>(this.trainUrl, { speed: speed }, httpOptions).pipe(
      //since we get the current train state in reply to any change request, make use of it
      map(response => response.train),
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
   * Direct from angular docs
   * @param error 
   */
  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // return an observable with a user-facing error message
    return throwError(
      'Something bad happened; please try again later.');
  };

  /**
   * perform HTTP request to get latest train state
   */
  private fetchTrainState(): Observable<Train> {

    let trainHTTP: Observable<ServerResponse> = this.http.get<ServerResponse>(
      this.trainUrl)
      .pipe(
        retry(3),
        catchError(this.handleError)
      );

    let train = trainHTTP.pipe(
      map(serverResponse => serverResponse.train),
    );
    return train;

  }

}
