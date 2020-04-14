import { Injectable } from '@angular/core';
import { Subject, Observable, interval, merge, throwError } from 'rxjs';
import { switchMap, share, retry, catchError, map, first, tap } from 'rxjs/operators';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Train } from './train-control.service';

export class Point {

  public changing: boolean;

  constructor(public index: number, public position: number) { }
}

export class ServerResponse {
  public type: string;
  public points?: Point[];
  public train?: Train;
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class PointControlService {

  private pointsUpdated: Subject<Point[]> = new Subject<Point[]>();
  private pointsState: Observable<Point[]>;
  private trainUrl: string;

  constructor(private http: HttpClient) {

    this.trainUrl = "/train/"

    let checkForUpdates = interval(1000);

    let updatingTrain = checkForUpdates.pipe(
      switchMap(now => this.fetchPointsState())
    )

    this.pointsState = merge(this.pointsUpdated.asObservable(), updatingTrain).pipe(
      share()
    );

  }

  // public isThisDeviceAPointsServer(): Observable<boolean>{
    
  // }

  public getPoints():Observable<Point[]>{
    return this.pointsState;
  }

  private addIndexToPoints(pointsWithoutIndex:Point[]) : Point[]{
    for(let i = 0; i< pointsWithoutIndex.length; i++){
      pointsWithoutIndex[i].index = i;
    }
    return pointsWithoutIndex;
  }

  public setPointPosition(index: number, position: number) {
    this.setPointPositionRequest(index, position).pipe(first()).subscribe();
  }

  private setPointPositionRequest(index: number, position: number): Observable<Point[]> {
    let request = this.http.post<ServerResponse>(this.trainUrl, { point_index: index, position: position}, httpOptions).pipe(
      //since we get the current train state in reply to any change request, make use of it
      map(ServerResponse => ServerResponse.points),
      map(pointsWithoutIndex => this.addIndexToPoints(pointsWithoutIndex)),
      tap(points => this.pointsUpdated.next(points))
    );

    return request;
  }


  private fetchPointsState(): Observable<Point[]> {
    let trainHTTP: Observable<ServerResponse> = this.http.get<ServerResponse>(
      this.trainUrl)
      .pipe(
        retry(3),
        catchError(this.handleError)
      );

    let points = trainHTTP.pipe(
      map(serverResponse => serverResponse.points),
      map(pointsWithoutIndex => this.addIndexToPoints(pointsWithoutIndex)),
    );

    return points;
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
}
