var express = require('express');
var mongodb = require('mongodb');
var mongoClient = mongodb.MongoClient;

var app = express();
var bodyParser = require('body-parser');
var url = "mongodb://admin:myadminpassword@3.82.157.225:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false";

app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));
module.exports = {
    foo: function (searchStr) {
      console.log(searchStr);
      return;
    },

    logKeywords: function(searchStr){
        var obj = {};
        var arr = [];
        var fs = require('fs');

        fs.readFile('./json_files/log.json', 'utf8', function readFileCallback(err, data){
            if (err){
                console.log(err);
            } else {
            jsonObj = JSON.parse(data);
            
            var found = false;
            for (var index in jsonObj) {
                if (jsonObj[index].keyword == searchStr) {
                    jsonObj[index].timestamp.push(Date.now());
                    jsonObj[index].count += 1;
                    found = true;
                }
            }

            if (found == false){ 
                obj["keyword"] = searchStr;
                obj["count"] = 1;
                arr.push(Date.now());
                obj["timestamp"] = arr;

                jsonObj.push(obj);
            }

            jsonString = JSON.stringify(jsonObj);
            fs.writeFile('./json_files/log.json', jsonString, 'utf8', function (err) {
                if (err) throw err;
                console.log('keyword saved in the file');
            });
        }});
    },

    catalog: function(searchStr, result){
        console.log("catalog file");

        var fs = require('fs');

        fs.readFile('./json_files/catalog.json', 'utf8', function readFileCallback(err, data){
            if (err){
                console.log(err);
            } else {

            jsonObj = JSON.parse(data);

            jsonObj.push({keyword: searchStr, result: result});

            jsonString = JSON.stringify(jsonObj);
            fs.writeFile('./json_files/catalog.json', jsonString, 'utf8', function (err) {
                if (err) throw err;
                console.log('words saved in the file');
            });
        }});
    }
}

mongoClient.connect(url, {useNewUrlParser: true, useUnifiedTopology: true}, function(err,db) {
	if(err)
		throw err;
    console.log('Connected to MongoDB in EC2');
	db.close;
});

app.get('/search/:name', (req,res) => {
	mongoClient.connect(url, {useUnifiedTopology: true}, function(err,db) {
	if(err)
		throw err;
	
    var dbo = db.db("Books");

    dbo.collection("books").createIndex({author: "text", title: "text"});
    var searchStr = "\"".concat(req.params.name).concat("\"");

	dbo.collection("books").find({ $text : { $search : searchStr}}).toArray(function(err, result) {
        if (err) throw err;

        res.json(result);

        module.exports.logKeywords(req.params.name);

        if(result.length > 0) {
            module.exports.catalog(req.params.name, result);
        }

		db.close();
    });
	});
});


app.get('/retrieve/:name', (req,res) => {
    var fs = require('fs');
    obj = {};
    arr = [];

    fs.readFile('./json_files/notes.json', 'utf8', function readFileCallback(err, data){
        if (err){
            console.log(err);
        } else {

        jsonObj = JSON.parse(data);
        
        for (var key in jsonObj.notes) {
            if (jsonObj.notes.hasOwnProperty(key) && jsonObj.notes[key].keyword == req.params.name) {
                arr.push(jsonObj.notes[key]);
            }
        }
        res.json(arr);
    }});
});


app.post('/notes', (req,res) => {
    var fs = require('fs');

    fs.readFile('./json_files/notes.json', 'utf8', function readFileCallback(err, data){
        if (err){
            console.log(err);
        } else {

        jsonObj = JSON.parse(data);

        note = {};
        note['keyword'] = req.body['keyword']
        note['note'] = req.body['note']
        jsonObj.notes.push(note)

        jsonString = JSON.stringify(jsonObj);
        fs.writeFile('./json_files/notes.json', jsonString, 'utf8', function (err) {
            if (err) throw err;
            console.log('Notes saved');
        });
    }});

    res.json({status: 200});
})

app.listen('5000', () => {
    console.log('Server started on port 5000');
});