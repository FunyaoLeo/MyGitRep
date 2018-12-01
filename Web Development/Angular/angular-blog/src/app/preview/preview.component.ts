import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute} from '@angular/router';
import { Location } from '@angular/common';
import { Parser, HtmlRenderer } from 'commonmark';
import {Post, BlogService} from '../blog.service';

@Component({
  selector: 'app-preview',
  templateUrl: './preview.component.html',
  styleUrls: ['./preview.component.css']
})

export class PreviewComponent implements OnInit {
  post:Post;
  postid:number;
  renderedTitle:string;
  renderedBody:string;
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private location: Location,
    private blogService:BlogService
  ) {
    route.paramMap.subscribe(
      () =>{
        this.postid = +this.route.snapshot.paramMap.get('id');
        this.getPost();
      }
    );
  }

  ngOnInit() {
  }

  getPost():void{
    let reader = new Parser();
    let writer = new HtmlRenderer();
    this.blogService.subscribePost(
      posts => {
        this.post = posts.filter(post=>post.postid==this.postid)[0];
        this.renderedTitle = writer.render(reader.parse(this.post.title));
        this.renderedBody = writer.render(reader.parse(this.post.body));
      }
    );
    this.post = this.blogService.getPost(this.postid);
    this.renderedTitle = writer.render(reader.parse(this.post.title));
    this.renderedBody = writer.render(reader.parse(this.post.body));
  }

  goBack():void{
    this.location.back();
  }
}
