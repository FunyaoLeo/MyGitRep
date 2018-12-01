import { Injectable } from '@angular/core';
import { Router, ActivatedRoute} from '@angular/router';

@Injectable({
  providedIn: 'root'
})

export class BlogService {
  private posts: Post[] = null;
  private maxID:number = -1;
  private username:string;
  callbackPost = null;
  callbackPosts = null;
  API_URL = "http://localhost:3000/api/"
  http: XMLHttpRequest = new XMLHttpRequest();

  constructor(private route: ActivatedRoute,
              private router: Router) {
    this.username = this.parseJWT();
    this.fetchPosts();
  }

  subscribePosts(callbackPosts)
  {
    this.callbackPosts = callbackPosts;
  }

  subscribePost(callbackPost){
    this.callbackPost = callbackPost;
  }


  parseJWT():string{
    let token = document.cookie.replace(/(?:(?:^|.*;\s*)jwt\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    let base64Url = token.split('.')[1];
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(atob(base64)).usr;
  }

  fetchPosts():void{
    this.http.open("GET", this.API_URL+this.username);
    this.http.onreadystatechange = (() => {
      console.log(this.http.readyState);
      // http request has not been sent yet.
      if (this.http.readyState != 4) return;

      this.posts = JSON.parse(this.http.responseText);
      this.maxID = 0;
      for (let post of this.posts) {
        this.maxID = Math.max(post.postid, this.maxID);
      }
      console.log(this.posts);
      console.log(this.maxID);
      // if this.callback has already been assigned a function,
      // then we can execute this function by passing posts into it
      if (this.callbackPosts) {
        this.callbackPosts(this.getPosts());
      }
      if (this.callbackPost) {
        this.callbackPost(this.getPosts());
      }
    });
    this.http.send();
  }

  getPosts():Post[]{
    return this.posts;
  }

  getPost(id:number):Post{
    if(this.posts==null)
      return null;
    else
      return this.posts.filter(post=>post.postid==id)[0];
  }

  newPost():Post{
    if(this.maxID==-1) return null;

    let post = new Post();
    post.postid = this.maxID+1;
    post.created = new Date();
    post.modified = new Date();
    post.title = '';
    post.body = '';

    this.http.open("POST", this.API_URL+this.username+'/'+post.postid);
    this.http.onreadystatechange = (() => {
      // http request has not been sent yet.
      if (this.http.readyState != 4) return;
      if(this.http.status!=201){
        alert("Error creating new post");
        this.router.navigate(['/']);
      }
      this.maxID = this.maxID+1;
    });
    this.http.setRequestHeader('Content-Type', 'application/json');
    this.http.send(JSON.stringify(post));
    return post;
  }

  updatePost(post:Post):void{
    let exist = false;
    for(let p of this.posts){
      if(p.postid==post.postid){
        exist = true;
        break;
      }
    }
    if(exist){
      this.http.open("PUT", this.API_URL+this.username+'/'+post.postid);
      this.http.onreadystatechange = (() => {
        // http request has not been sent yet.
        if (this.http.readyState != 4) return;
        if(this.http.status!=200) {
          alert("Error saving post, try it again later");
          this.router.navigate(['/edit/', post.postid]);
        }
      });
      this.http.setRequestHeader("Content-type", "application/json");
      this.http.send(JSON.stringify((post)));
    }
    else{
      alert("no such post!");
    }
  }

  deletePost(postid:number):void{
    let index = 0;
    for(let post of this.posts){
      if(post.postid == postid) break;
      index = index+1;
    }
    if(index<this.posts.length){
      this.posts.splice(index,1);
      if(this.posts.length!=0)
        this.maxID = this.posts[this.posts.length-1].postid;
      else
        this.maxID = 0;
      this.http.open("DELETE", this.API_URL+this.username+'/'+postid);
      this.http.onreadystatechange = (() => {
        // http request has not been sent yet.
        if (this.http.readyState != 4) return;
        if (this.http.status!=204) {
          alert("Error Deleting the post!");
          this.router.navigate(['/']);
        }
      });
      this.http.send();
    }
  }
}

export class Post {
  postid: number;
  created: Date;
  modified: Date;
  title: string;
  body: string;
}
