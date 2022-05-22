import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {

  URL_BASE = "http://localhost:5000";
  constructor(private http: HttpClient) { }

  sendSentence(sentence: string): Observable<any>{
    const url = `${this.URL_BASE}/sentence?text=${sentence}`;
    // console.log(url);
    return this.http.get(url);
  }

  editResponse(sentence: string, response: string, newResponse: string){
    const body = {sentence,response,newResponse};
    const url = `${this.URL_BASE}/sentence`;
    return this.http.post(url,body);
  }

  editSubject(sentence: string, subject: string, newSubject: string){
    const body = {sentence, subject, newSubject};
    const url = `${this.URL_BASE}/sentence`;
    return this.http.put(url, body);
  }

  getSubjects(){
    return this.http.get(`${this.URL_BASE}/subject`);
  }

}
