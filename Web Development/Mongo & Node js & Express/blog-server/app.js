var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017"
const assert = require('assert');

var indexRouter = require('./routes/index');
var blogRouter = require('./routes/blog');
var usersRouter = require('./routes/users');
var loginRouter = require('./routes/login');
var apiRouter = require('./routes/api');

var app = express();

var db;

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

//Mongo DB connection
MongoClient.connect(url, function (err, database) {
    assert.equal(null, err);
    db = database.db("BlogServer");
});


app.use(function(req, res, next) {
    console.log("Entering db reuse module...")
    req.db = db;
    next();
});
app.use('/', indexRouter);
app.use('/login', loginRouter);
app.use('/blog', blogRouter);
app.use('/users', usersRouter);
app.use('/api', apiRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
