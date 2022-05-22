import { Component, Input, OnInit } from '@angular/core';
import { Anime } from '../anime.model';

@Component({
  selector: 'app-anime-detail',
  templateUrl: './anime-detail.component.html',
  styleUrls: ['./anime-detail.component.scss']
})
export class AnimeDetailComponent implements OnInit {

  @Input() anime: any;

  constructor() {}

  ngOnInit(): void {
  }

}
