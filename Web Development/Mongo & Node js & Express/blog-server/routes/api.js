var express = require('express');
var router = express.Router();
var jwt = require('jsonwebtoken');
const assert = require('assert');


/* GET users listing. */
router.all('/:username', function(req, res, next) {
    console.log("checking cookie");
    console.log(req.cookies);
    if(req.cookies.jwt == null){
        res.status(401);
        res.render('unauthenticated');
    }
    else{
        try {
            var token = jwt.verify(req.cookies.jwt, "C-UFRaksvPKhx1txJYFcut3QGxsafPmwCY6SCly3G6c");
            var username = token.usr;
            var exp = token.exp * 1000;
            if (username == req.params.username && exp > Date.now()) {
                next();
            }
            else {
                res.status(401);
                res.render('unauthenticated');
            }
        }catch(err){
            res.status(401).send(err);
        }
    }
});

/* GET users listing. */
router.all('/:username/:password', function(req, res, next) {
    console.log("checking cookie");
    console.log(req.cookies);
    if(req.cookies.jwt == null){
        res.status(401);
        res.render('unauthenticated');
    }
    else{
        try {
            var token = jwt.verify(req.cookies.jwt, "C-UFRaksvPKhx1txJYFcut3QGxsafPmwCY6SCly3G6c");
            var username = token.usr;
            var exp = token.exp * 1000;
            if (username == req.params.username && exp > Date.now()) {
                next();
            }
            else {
                res.status(401);
                res.render('unauthenticated');
            }
        }catch(err){
            res.status(401).send(err);
        }
    }
});

router.get('/:username', function(req, res, next) {
    var dbo = req.db;
    var query = {"username": req.params.username};
    dbo.collection("Posts").find(query).toArray(function (err, posts) {
        assert.equal(null, err);
        console.log("below are the query results for /username/postid")
        console.log(posts);
        res.status(200).json(posts);
    });
});

router.get('/:username/:postid', function(req, res, next) {
    var dbo = req.db;
    var query = {$and:[{"username":req.params.username},
            {"postid": parseInt(req.params.postid)}]};
    dbo.collection("Posts").find(query).toArray(function(err, posts){
        assert.equal(null, err);
        console.log("below are the query results for /username/postid")
        console.log(posts);
        if(posts.length==0){
            res.status(404).json(posts);
        }
        else{
            res.status(200).json(posts);
        }
    });
});

router.post('/:username/:postid', function(req, res, next) {
    console.log("entering post");
    if(req.body.title==null||req.body.body==null){
        res.status(400).json();
    }
    else{
        var dbo = req.db;
        var query = {$and:[{"username":req.params.username},
                {"postid": parseInt(req.params.postid)}]};
        dbo.collection("Posts").find(query).toArray(function (err, posts) {
            assert.equal(null, err);
            console.log("below are the query results for /username/postid")
            console.log(posts);
            if(posts.length!=0){
                res.status(400).json();
            }
            else{
                // Insert a single document
                var doc = {
                    username: req.params.username,
                    postid: parseInt(req.params.postid),
                    title: req.body.title,
                    body: req.body.body,
                    created: Date.now(),
                    modified: Date.now()};
                console.log(doc);
                dbo.collection('Posts').insertOne(doc, function(err, r) {
                    assert.equal(null, err);
                    assert.equal(1, r.insertedCount);
                    res.status(201).json();
                });
            }
        });
    }

});

router.put('/:username/:postid', function(req, res, next) {
    if(req.body.title==null||req.body.body==null){
        res.status(400).json();
    }
    else{
        var dbo = req.db;
        var query = {$and:[{"username":req.params.username},
                {"postid": parseInt(req.params.postid)}]};
        dbo.collection("Posts").find(query).toArray(function (err, posts) {
            assert.equal(null, err);
            console.log("below are the query results for /username/postid")
            console.log(posts);
            if(posts.length==0){
                res.status(400).json();
            }
            else{
                // Update a single document
                var doc = { $set:{
                    title: req.body.title,
                        body: req.body.body,
                        modified: Date.now()}};
                dbo.collection('Posts').updateOne(query, doc, function(err, r) {
                    assert.equal(null, err);
                    res.status(200).json();
                });
            }
        });
    }
});

router.delete('/:username/:postid', function(req, res, next) {
    var dbo = req.db;
    var query = {$and:[{"username":req.params.username},
            {"postid": parseInt(req.params.postid)}]};
    dbo.collection("Posts").find(query).toArray(function (err, posts) {
        assert.equal(null, err);
        console.log("below are the query results for /username/postid")
        console.log(posts);
        if(posts.length==0){
            res.status(400).json();
        }
        else{
            // Delete a single post
            dbo.collection('Posts').deleteOne(query,  function(err, r) {
                assert.equal(null, err);
                res.status(204).json();
            });
        }
    });
});


module.exports = router;