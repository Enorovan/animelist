import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-assistant-page',
  templateUrl: './assistant-page.component.html',
  styleUrls: ['./assistant-page.component.scss']
})
export class AssistantPageComponent implements OnInit {

  sentence = "";
  response: string | any = null;
  lastSentence = "";
  newResponse = "";
  lastSubject = "";
  newSubject = "";
  isLoading = false;
  subjects: string[] = [];
  controlSubjects = new FormControl();
  changeTextMonAssistant: Boolean = false;

  constructor(private api: ApiServiceService, private sn: MatSnackBar) { }

  ngOnInit(): void {
    this.api.getSubjects().subscribe((value: any) => {
      this.subjects = value.data;
    });
    this.controlSubjects.valueChanges.subscribe(value => {
      this.newSubject = value;
    })
  }

  sendSentence(){
    this.isLoading = true;
    this.api.sendSentence(this.sentence)
            .subscribe(value => {
              this.isLoading = false;
              this.lastSentence = this.sentence;
              this.lastSubject = value.subject;
              this.sentence = "";
              this.response = value.data;
            });
  }

  editSubject(){
    this.isLoading = true;
    this.api.editSubject(this.lastSentence, this.lastSubject, this.newSubject)
            .subscribe(value => {
              this.isLoading = false;
              this.sn.open("Vous avez modifié le sujet !");
            });
  }

  editResponse(){
    this.isLoading = true;
    this.api.editResponse(this.lastSentence, this.response, this.newResponse)
            .subscribe(value => {
              this.isLoading = false;
              this.sn.open("Vous avez modifié la réponse !");
              this.newResponse = "";
            },err => console.log(err)
            );
  }

  isResponseAnArray(){
    return typeof this.response == "object";
  }

}
