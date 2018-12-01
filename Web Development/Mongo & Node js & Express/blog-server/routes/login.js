var express = require('express');
var router = express.Router();
const bcrypt = require('bcrypt');
var jwt = require('jsonwebtoken');
const assert = require('assert');


/* GET home page. */

router.get('/', function(req, res, next) {
    if(req.query.redirect==null){
        res.render('login', {
            redirect: req.query.redirect
        });
    }
    else{
        res.render('login', {
            redirect: req.query.redirect
        });
    }
});

router.post('/', function(req, res, next) {
    var username = req.body.username;
    var password = req.body.password;
    var dbo = req.db;
    query = {"username": username};
    dbo.collection("Users").find(query).toArray(function (err, dbpassword) {
        assert.equal(null, err);
        if(dbpassword.length==1){
            bcrypt.compare(password, dbpassword[0].password, function(err, result){
                if(result==true){
                    var payload = {
                        "exp": Math.floor(Date.now() / 1000) + (2*60*60),
                        "usr": username
                    };
                    var secretKey = "C-UFRaksvPKhx1txJYFcut3QGxsafPmwCY6SCly3G6c";
                    var token = jwt.sign(payload, secretKey);
                    res.cookie('jwt', token);
                    if (typeof req.body.redirect == 'undefined'|| req.body.redirect == "") {
                        res.status(200).send("authentication succeed");
                    }
                    else {
                        res.redirect(req.body.redirect);
                    }
                }
                else{
                    console.log("password failed");
                    res.status(401);
                    res.render('login', {
                        redirect: req.body.redirect
                    });
                }
            })
        }
        else{
            res.status(401);
            res.render('login', {
                redirect: req.body.redirect
            });
        }
    });
});

module.exports = router;