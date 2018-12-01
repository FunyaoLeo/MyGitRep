import { Component, OnInit } from '@angular/core';
import { BlogService, Post} from '../blog.service';
import { Router, ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})

export class ListComponent implements OnInit {
  posts : Post[];
  selectedPost:Post;

  constructor(private route: ActivatedRoute,
              private router: Router,
              private blogService: BlogService) {
    route.paramMap.subscribe(
      () =>{
        this.posts = this.blogService.getPosts();
      }
    );
  }

  ngOnInit() {
    this.getPosts();
  }

  getPosts(): void {
    this.blogService.subscribePosts(
      // Here we are passing a callback function into subscribe
      posts => this.posts = posts);
    let postsTemp = this.blogService.getPosts();
    if(postsTemp!=null)
      this.posts = postsTemp;
  }

  onNew():void{
    let newPost = this.blogService.newPost();
    this.posts.push(newPost);
    this.router.navigate(['/edit/', newPost.postid]);
  }
}
