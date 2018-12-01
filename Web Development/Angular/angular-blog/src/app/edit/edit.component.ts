import { Component, OnInit, HostListener } from '@angular/core';
import { Router, ActivatedRoute} from '@angular/router';
import { Post, BlogService} from '../blog.service';


@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})

export class EditComponent implements OnInit {
  post:Post = null;
  postid:number;
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private blogService:BlogService) {
    route.paramMap.subscribe(
      () =>{
        if(this.post!=null)
          this.onSave();
        this.postid = +this.route.snapshot.paramMap.get('id');
        this.getPost();
      }
    );
  }

  ngOnInit() {
  }

  getPost():void{
    this.blogService.subscribePost(
      posts => {
        this.post = posts.filter(post=>post.postid==this.postid)[0];
      }
    );
    this.post = this.blogService.getPost(this.postid);
  }

  onDelete():void{
    this.blogService.deletePost(this.postid);
    this.router.navigate(['/']);
  }

  onPreview():void{
    this.onSave();
    this.router.navigate(['/preview/', this.postid]);
  }

  @HostListener('window:beforeunload')
  onSave():void{
    this.blogService.updatePost(this.post);
    this.post.modified = new Date();
  }

}
