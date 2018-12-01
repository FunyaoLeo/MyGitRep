var express = require('express');
var router = express.Router();
var commonmark = require('commonmark');
var reader = new commonmark.Parser();
var writer = new commonmark.HtmlRenderer();
const assert = require('assert');

router.get('/:username', function(req, res, next) {
    console.log(req.params);
    var dbo = req.db;
    var nextId = 0;
    var query;
    if (req.query.start == null) {
        query = {"username": req.params.username};
        dbo.collection("Posts").find(query).toArray(function (err, posts) {
            assert.equal(null, err);
            if(posts.length==0){
                res.status(404).send("no such user");
            }
            else {
                if (posts.length > 5) {
                    posts = posts.slice(0, 5);
                    nextId = 6;
                }
                console.log("Below are the query result for /username");
                console.log(posts);
                for (post of posts) {
                    post.title = writer.render(reader.parse(post.title));
                    post.body = writer.render(reader.parse(post.body));
                }
                res.render('blog', {
                    posts: posts,
                    nextId: nextId
                });
            }
        });
    }
    else {
        query = {
            $and: [{"username": req.params.username},
                {"postid": {$gte: parseInt(req.query.start)}}]
        };
        dbo.collection("Posts").find(query).toArray(function (err, posts) {
            assert.equal(null, err);
            if(posts.length==0){
                res.status(404).send("no such user");
            }
            else {
                if (posts.length > 5) {
                    posts = posts.slice(0, 5);
                    nextId = 5 + parseInt(req.query.start);
                }
                console.log("Below are the query result for /username")
                console.log(posts);
                for (post of posts) {
                    post.title = writer.render(reader.parse(post.title));
                    post.body = writer.render(reader.parse(post.body));
                }
                res.render('blog', {
                    posts: posts,
                    nextId: nextId
                });
            }
        });

    }

});


router.get('/:username/:postid', function(req, res, next){
    var dbo = req.db;
    var query = {$and:[{"username":req.params.username},
            {"postid": parseInt(req.params.postid)}]};
    dbo.collection("Posts").find(query).toArray(function(err, posts){
        assert.equal(null, err);
        if(posts.length==0){
            res.status(404).send("no such user");
        }
        else {
            console.log("below are the query results for /username/postid")
            console.log(posts);
            var post = posts[0];
            var title = writer.render(reader.parse(post.title));
            var body = writer.render(reader.parse(post.body));
            res.render('view', {
                title: title,
                body: body,
                username: req.params.username,
                postid: req.params.postid
            });
        }
    });
});


module.exports = router;